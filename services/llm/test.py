# services/llm/news_filtering_service.py

import json
import re
from typing import List
import logging

from clients.ai_client import UniPipcAIClient
from core.ai_prompt.news_filtering_prompt import REFERENCE_TEMPLATE, PROMPT_TEMPLATES, QUESTION_TEMPLATES
from models.llm.news_filtering_schemas import NewsFilteringRequest, NewsFilteringResponse
from models.llm.utils_schemas import NewsItem, ArticleContent

logger = logging.getLogger(__name__)

class NewsFilteringService:
    """Phân tích nội dung các tin tức -> chọn nội dung phù hợp và tạo outline"""
    
    def __init__(self):
        self.ai_client = UniPipcAIClient()
    
    def _prepare_news_data(self, articles: List[ArticleContent]) -> str:
        """Chuẩn hóa dữ liệu tin tức - rút gọn để tiết kiệm token"""
        news_data = []
        for idx, article in enumerate(articles, 1):
            # Rút gọn content preview
            content_preview = article.content_preview[:300] if article.content_preview else ""
            
            ref = REFERENCE_TEMPLATE.format(
                idx=idx,
                title=article.title[:80],  # Rút gọn tiêu đề
                url=article.url,
                content_preview=content_preview
            )
            news_data.append(ref)
        
        return "\n".join(news_data)
    
    def _clean_ai_response(self, content: str) -> str:
        """Làm sạch response từ AI để parse JSON"""
        if not content:
            return ""
            
        # Loại bỏ markdown code blocks
        content = content.strip()
        
        # Loại bỏ ```json và ```
        if content.startswith("```json"):
            content = content[7:]
        elif content.startswith("```"):
            content = content[3:]
        
        if content.endswith("```"):
            content = content[:-3]
        
        content = content.strip()
        
        # Loại bỏ các ký tự đặc biệt ở đầu (như \n)
        if content.startswith('\n'):
            content = content[1:]
            
        return content
    
    async def filtering_news(self, request: NewsFilteringRequest) -> NewsFilteringResponse:
        """Thực hiện lọc tin và tạo outline bài viết"""
        logger.info(f"Starting news filtering for article: {request.article_title}")
        
        if not request.articles:
            return NewsFilteringResponse(
                success=False,
                selected_news=[],
                article_outline=None,
                total_analyzed=0
            )
        
        # Format prompt với thông tin mới
        system_prompt = PROMPT_TEMPLATES.format(
            article_title=request.article_title,
            main_keyword=request.main_keyword
        )
        
        news_text = self._prepare_news_data(request.articles)
        question_input = QUESTION_TEMPLATES.format(
            article_title=request.article_title,
            main_keyword=request.main_keyword,
            secondary_keywords=", ".join(request.secondary_keywords) if request.secondary_keywords else "Không có",
            news_text=news_text,
        )

        logger.debug(f"System prompt length: {len(system_prompt)}")
        logger.debug(f"Question input length: {len(question_input)}")
        
        # Gọi AI
        ai_response = self.ai_client.ask_question_with_prompt(
            prompt=system_prompt,
            question=question_input
        )
        
        if not ai_response:
            logger.error("AI response is empty or None")
            return NewsFilteringResponse(
                success=False,
                selected_news=[],
                article_outline=None,
                total_analyzed=len(request.articles)
            )
        
        try:
            # Xử lý response - THEO CÁCH CŨ CỦA BẠN
            data = ai_response.get("data", {})
            content = data.get("answer", "") or data.get("QAMsg", "")
            
            if not content:
                logger.error("No content in AI response")
                return NewsFilteringResponse(
                    success=False,
                    selected_news=[],
                    article_outline=None,
                    total_analyzed=len(request.articles)
                )
            
            # Log raw response để debug
            logger.debug(f"Raw AI response (first 500 chars): {content[:500]}")
            
            # Clean response
            content = self._clean_ai_response(content)
            logger.debug(f"Cleaned content (first 500 chars): {content[:500]}")
            
            # Parse JSON
            result = json.loads(content)
            logger.info(f"Successfully parsed JSON, found {len(result.get('selected_news', []))} news items")
            
            # Lấy selected news và outline từ response
            filtered_news = result.get("selected_news", [])
            article_outline = result.get("article_outline", "")
            
            # Mapping để lấy thông tin gốc
            url_to_content = {article.url: article.content_preview for article in request.articles}
            
            # Chuẩn bị selected news
            selected_news = []
            for news_item in filtered_news[:request.top_k]:
                news_url = news_item.get("url", "")
                
                # Lấy hình ảnh từ AI response
                ai_images = news_item.get("images", [])
                
                # Lấy content_preview từ article gốc
                content_preview = url_to_content.get(news_url, "")
                
                selected_news.append(NewsItem(
                    rank=news_item.get("rank", 0),
                    title=news_item.get("title", ""),
                    url=news_url,
                    images=ai_images,
                    content_preview=content_preview
                ))
            
            logger.info(f"Successfully filtered {len(selected_news)} news items")
            
            return NewsFilteringResponse(
                success=True,
                selected_news=selected_news,
                article_outline=article_outline,
                total_analyzed=len(request.articles)
            )
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON Parse Error: {e}")
            if 'content' in locals():
                logger.error(f"Problematic content (first 1000 chars): {content[:1000]}")
                # Thử tìm JSON trong content
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    logger.info(f"Found potential JSON match: {json_match.group()[:200]}")
            return NewsFilteringResponse(
                success=False,
                selected_news=[],
                article_outline=None,
                total_analyzed=len(request.articles)
            )
        except Exception as e:
            logger.error(f"Unexpected Error: {e}", exc_info=True)
            return NewsFilteringResponse(
                success=False,
                selected_news=[],
                article_outline=None,
                total_analyzed=len(request.articles)
            )