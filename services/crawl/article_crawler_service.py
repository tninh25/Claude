# services/crawl/article_crawler_service.py

import asyncio
import logging
from typing import List

from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

from models.crawl.crawler_schemas import CrawlRequest, CrawlResponse, ArticleContent
from utils.config_loader import config  

from .crawler_config import CrawlConfig
from .image_cleaner import clean_image_urls

logger = logging.getLogger(__name__)


class CrawlService:
    """
    Lấy nội dung tin tức từ URL
    - crawl_article_content: lấy 1 bài
    - crawl_multiple_articles: lấy nhiều bài bằng asyncio.gather
    Ý tưởng & flow giữ nguyên hoàn toàn so với code gốc.
    """

    def __init__(self):
        crawler_cfg = config.get('crawler', {})
        cfg = CrawlConfig.from_settings(crawler_cfg)
        # nếu crawl4ai có CacheMode, lấy mặc định BYPASS nếu không set
        self.cache_mode = CacheMode.BYPASS if getattr(cfg, 'cache_mode', None) is None else cfg.cache_mode
        self.content_threshold = cfg.content_threshold
        self.max_content_length = cfg.max_content_length
        self.max_images = cfg.max_images

    async def crawl_article_content(self, url: str, title: str, snippet: str) -> ArticleContent:
        """Lấy nội dung với chiến thuật markdown — giữ đúng flow gốc"""
        markdown_generator = DefaultMarkdownGenerator(
            content_filter=PruningContentFilter(
                threshold=self.content_threshold,
                threshold_type="fixed"
            )
        )

        run_config = CrawlerRunConfig(
            cache_mode=self.cache_mode,
            markdown_generator=markdown_generator
        )

        try:
            async with AsyncWebCrawler() as crawler:
                result = await crawler.arun(url=url, config=run_config)

                if result and getattr(result, "success", False):
                    # Thu thập hình ảnh theo 2 nguồn media/images giống gốc
                    image_urls: List[str] = []

                    if hasattr(result, 'media') and result.media:
                        if isinstance(result.media, dict) and 'images' in result.media:
                            for img in result.media['images'][: self.max_images * 4]:
                                if isinstance(img, dict) and 'src' in img:
                                    image_urls.append(img['src'])
                                elif isinstance(img, str):
                                    image_urls.append(img)

                    if hasattr(result, 'images') and result.images:
                        if isinstance(result.images, list):
                            for img in result.images[: self.max_images * 4]:
                                if isinstance(img, dict) and 'src' in img:
                                    image_urls.append(img['src'])
                                elif isinstance(img, str):
                                    image_urls.append(img)

                    # Clean & select best images (giữ nguyên ý tưởng)
                    cleaned_images = clean_image_urls(image_urls, max_images=self.max_images)

                    content_preview = ""
                    try:
                        content_preview = result.markdown.fit_markdown[: self.max_content_length]
                    except Exception:
                        content_preview = ""

                    return ArticleContent(
                        url=url,
                        title=title,
                        snippet=snippet,
                        content_preview=content_preview,
                        images=cleaned_images,
                        success=True
                    )
                else:
                    return ArticleContent(
                        url=url,
                        title=title,
                        snippet=snippet,
                        content_preview="",
                        images=[],
                        success=False,
                        error=(result.error_message if result else "Unknown error")
                    )
        except Exception as e:
            # giữ nguyên behavior: capture exception và trả về ArticleContent success=False
            logger.exception("Crawler exception for url %s: %s", url, e)
            return ArticleContent(
                url=url,
                title=title,
                snippet=snippet,
                content_preview="",
                images=[],
                success=False,
                error=str(e)
            )

    async def crawl_multiple_articles(self, request: CrawlRequest) -> CrawlResponse:
        """Lấy nội dung từ nhiều URL cùng lúc — giữ nguyên logging & behavior ban đầu"""
        logger.info(f"Articles to crawl: {[(article.url, article.title) for article in request.articles]}")

        tasks = []
        for article in request.articles:
            tasks.append(self.crawl_article_content(
                url=article.url,
                title=article.title,
                snippet=article.snippet
            ))

        results = await asyncio.gather(*tasks, return_exceptions=True)

        processed_articles = []
        failed_count = 0

        for res in results:
            if isinstance(res, Exception):
                logger.error(f"Crawl task failed with exception: {res}")
                failed_count += 1
                continue

            processed_articles.append(res)
            if not res.success:
                logger.warning(f"Crawl failed for {res.url}: {res.error}")
                failed_count += 1
            else:
                logger.info(f"Crawl successful for {res.url}")

        return CrawlResponse(
            success=len(processed_articles) > 0,
            processed_count=len(processed_articles),
            failed_count=failed_count,
            articles=processed_articles
        )
