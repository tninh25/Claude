# api/v1/ai.py
"""
    Các endpoints sử dụng API LuminAI:
        - Lọc tin tức liên quan đến từ khóa
        - Gợi ý tiêu đề bài viết dựa trên từ khóa
        - Viết bài 
"""

import logging
from fastapi import APIRouter

from services.llm.news_filtering_service import NewsFilteringService
from services.llm.title_generation_service import TitleGenerationService
from services.llm.content_generation_service import ContentGenerationService

from models.llm.news_filtering_schemas import NewsFilteringRequest, NewsFilteringResponse
from models.llm.title_generation_schemas import TitleSuggestionRequest, TitleSuggestionResponse
from models.llm.content_generation_schemas import ContentConfig, ContentRequest, ContentResponse, InternalContentRequest

logger = logging.getLogger(__name__)

# Khai báo router
router = APIRouter()

news_filtering_service = NewsFilteringService()
title_generation_service = TitleGenerationService()
content_generation_service = ContentGenerationService()

@router.post("/news-filterings", response_model=NewsFilteringResponse, description="Lọc tin tức phù hợp sử dụng LuminAI")
async def analyze_news(request: NewsFilteringRequest):
    # try:
        logger.info(f"Analyze endpoint called with {len(request.articles)} articles")
        return await news_filtering_service.filtering_news(request)
    # except Exception as e:
    #     logger.error(f"Analyze endpoint error: {str(e)}")
    #     return NewsFilteringResponse(
    #         success=False,
    #         selected_news=[],
    #         total_analyzed=len(request.articles),
    #         message=f"Analysis failed: {str(e)}"
    #     )

@router.post("/titles", response_model=TitleSuggestionResponse, description="Gợi ý tiêu đề bài viết dựa trên từ khóa")
async def suggest_titles(request: TitleSuggestionRequest):
    try:
        logger.info(f"Title suggestion endpoint called with keyword: {request.main_keyword}")
        return await title_generation_service.suggest_titles(request)
    except Exception as e:
        logger.error(f"Title suggestion error: {str(e)}")
        return TitleSuggestionResponse(
            success=False,
            message=f"Title suggestion failed: {str(e)}"
        )
    
@router.post("/contents", response_model=ContentResponse, description="Tạo bài viết")
async def generate_content(request: ContentRequest):
    try:
        logger.info(f"Generate content endpoint called for {len(request.top_news)} news items")
        logger.info(f"Request config: {request.config}")
        logger.info(f"Top news count: {len(request.top_news)}")

        return await content_generation_service.generate_seo_content(request)

    except Exception as e:
        logger.error(f"Generate content endpoint error: {str(e)}")

        return ContentResponse(
            success=False,
            article=None,
            message=f"Content generation failed: {str(e)}"
        )


@router.post("/contents/internal", response_model=ContentResponse, description="Tạo bài viết từ nội dung nội bộ")
async def generate_internal_content(request: InternalContentRequest):
    try:
        logger.info(f"Internal reference length: {len(request.internal_reference or '')} chars")
        
        return await content_generation_service.generate_internal_content(request)
        
    except Exception as e:
        logger.error(f"Generate internal content error: {str(e)}", exc_info=True)
        return ContentResponse(
            success=False,
            message=f"Internal content generation failed: {str(e)}"
        )
     
