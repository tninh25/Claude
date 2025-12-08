# models/crawler_schemas.py

from pydantic import BaseModel
from typing import List
from ..llm.utils_schemas import ArticleContent

class ArticleToCrawl(BaseModel):
    url: str
    title: str
    snippet: str

class CrawlRequest(BaseModel):
    articles: List[ArticleToCrawl] 

class CrawlResponse(BaseModel):
    success: bool
    processed_count: int
    failed_count: int
    articles: List[ArticleContent]