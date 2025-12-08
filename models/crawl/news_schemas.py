# models/news_schemas.py
from pydantic import BaseModel
from typing import List, Optional

class SearchRequest(BaseModel):
    query: str
    max_results: int = 10

class SearchResult(BaseModel):
    url: str
    title: str
    snippet: str

class SearchResponse(BaseModel):
    success: bool
    query: str
    total_results: int
    results: List[SearchResult]  
    message: Optional[str] = None