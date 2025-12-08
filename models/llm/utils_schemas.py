# models/llm/utils_schemas.py

from pydantic import BaseModel, Field
from typing import List, Optional

class ArticleContent(BaseModel):
    url: str
    title: str
    snippet: str
    content_preview: str
    images: List[str]  # Original images
    success: bool
    error: Optional[str] = None

class NewsItem(BaseModel):
    rank: int
    title: str
    url: str
    images: List[str] 
    content_preview: str

class OutlineConfig(BaseModel):
    """Config cho từng heading trong outline"""
    word_count: Optional[int] = Field(None, ge=50, le=5000, description="Số lượng từ")
    keywords: Optional[List[str]] = Field(None, description="Danh sách từ khóa")
    tone: Optional[str] = Field(None, description="Tone giọng viết")
    internal_link: Optional[str] = Field(None, description="Link nội bộ")

class OutlineItem(BaseModel):
    """
    Một heading trong outline
    Ban đầu LLM sinh ra KHÔNG CÓ config
    Config sẽ được user thêm sau qua giao diện PHP
    """
    id: str = Field(..., description="ID duy nhất của heading")
    level: int = Field(..., ge=1, le=6, description="Cấp độ heading (1-6)")
    title: str = Field(..., min_length=1, description="Tiêu đề heading")
    order: int = Field(..., ge=1, description="Thứ tự hiển thị")
    config: Optional[OutlineConfig] = Field(None, description="Cấu hình optional - user thêm sau")