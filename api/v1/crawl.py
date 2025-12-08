# api/v1/crawl.py
"""
    Enndpoints thực hiện các nhiệm vụ:
        - Lấy tin tức từ google theo từ khóa
        - Lấy nội dung của các tin tức được trả về
"""

import logging
from fastapi import APIRouter

from services.crawl.news_search_service import NewsService
from services.crawl.images_search_service import ImagesSearchService
from services.crawl.article_crawler_service import CrawlService

from models.crawl.crawler_schemas import CrawlRequest, CrawlResponse
from models.crawl.news_schemas import SearchRequest, SearchResponse
from models.crawl.images_schemas import ImageSearchRequest, ImageSearchResponse

logger = logging.getLogger(__name__)

# Khai báo router
router = APIRouter()

news_service  = NewsService()
crawl_service = CrawlService()
images_service = ImagesSearchService()

@router.post("/news", response_model=SearchResponse, description="Tìm kiếm tin tức trên google theo từ khóa")
async def search_news(request: SearchRequest):
    try:
        logger.info(f"Search endpoint called with query: {request.query}")
        return await news_service.news_searching(request)
    except Exception as e:
        logger.error(f"Search endpoint error: {str(e)}")
        return SearchResponse(
            success=False,
            query=request.query,
            total_results=0,
            results=[],
            message=f"Search failed: {str(e)}"
        )

@router.post("/images", response_model=ImageSearchResponse, description="Tìm kiếm hình ảnh trên google theo từ khóa")
async def search_images(request: ImageSearchRequest):
    try:
        logger.info(f"Search images endpoint called with query: {request.query}")
        return await images_service.search_images(request)
    except Exception as e:
        logger.error(f"Search images endpoint error: {str(e)}")
        return ImageSearchResponse(
            success=False,
            query=request.query,
            total_results=0,
            images=[], 
            message=f"Search failed: {str(e)}"
        )
    
@router.post("/crawl", response_model=CrawlResponse, description="Lấy nội dung chi tiết bài viết")
async def crawl_articles(request: CrawlRequest):
    try:
        logger.info(f"Crawl endpoint called with: {len(request.articles)} articles")
        return await crawl_service.crawl_multiple_articles(request)
    except Exception as e:
        logger.error(f"Crawl endpoint error: {str(e)}")
        return CrawlResponse(
            success=False,
            processed_count=0,
            failed_count=len(request.articles),
            articles=[],
            message=f"Crawl failed: {str(e)}"
        )
