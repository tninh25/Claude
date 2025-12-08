# models/llm/news_filtering_schemas.py

from pydantic import BaseModel, Field
from typing import List, Optional
from .utils_schemas import ArticleContent, NewsItem, OutlineConfig, OutlineItem

class NewsFilteringRequest(BaseModel):
    """
    Input cho use-case: LLM lọc tin tức phù hợp với user query
    """
    articles: List[ArticleContent]
    main_keyword: str
    secondary_keywords: List[str] = []
    article_title: str
    top_k: int = 3


class NewsFilteringResponse(BaseModel):
    """
    Output: danh sách tin đã được LLM chọn lọc và outline bài viết (JSON)
    """
    success: bool
    selected_news: List[NewsItem]
    article_outline: Optional[List[OutlineItem]] = None 

    article_title: Optional[str] = None
    main_keyword: Optional[str] = None
    secondary_keywords: Optional[List[str]] = None
    total_analyzed: int = 0