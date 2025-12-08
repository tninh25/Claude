# app/models/content_schemas.py

from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from models.llm.utils_schemas import NewsItem
from .utils_schemas import ArticleContent, NewsItem, OutlineConfig, OutlineItem

class ContentConfig(BaseModel):
    """Config mẫu cho bài viết"""
    bot_id: str = Field(default="GPT-4.1", description="ID của bot")
    article_length: str = Field(default="1500-1800", description="Độ dài bài viết")
    tone: str = Field(default="Chuyên Nghiệp", description="Tone giọng")
    article_type: str = Field(default="Blog", description="Loại bài viết")
    language: str = Field(default="Tiếng Việt", description="Ngôn ngữ")
    custom_instructions: Optional[str] = Field(default=None, description="Hướng dẫn tùy chỉnh")

class ArticleBlock(BaseModel):
    id: str              # ví dụ: h1-1, p-3, h2-2
    tag: str             # h1 | h2 | h3 | p | li
    text: str
    word_count: Optional[int] = None

class SEOArticle(BaseModel):
    title: str
    meta_description: str
    blocks: Optional[List[ArticleBlock]] = None
    html_content: Optional[str] = None
    keywords: List[str]
    references: List[Dict[str, str]]
    images: List[str] = []
    generation_config: Optional[ContentConfig] = Field(
        None,
        description="Config dùng để generate bài viết này"
    )

class ContentRequest(BaseModel):
    """Viết bài với dữ liệu trên Internet"""
    top_news: List[NewsItem] = []
    target_language: str = "Tiếng Việt"
    config: Optional[ContentConfig] = None
    
    title: Optional[str] = Field(
        default=None, 
        description="Tiêu đề bài viết (nếu có từ bước filtering)"
    )

    outline: Optional[List[OutlineItem]] = Field(
        default=None,
        description="Outline structured của bài viết (đã có thể có config)"
    )
    main_keyword: Optional[str] = Field(
        default=None,
        description="Từ khóa chính cho bài viết"
    )
    secondary_keywords: Optional[List[str]] = Field(
        default=None,
        description="Danh sách từ khóa phụ"
    )

class InternalContentRequest(BaseModel):
    """Request cho viết bài nội bộ"""
    internal_reference: Optional[str] = Field(
        default=None, 
        description="Nội dung nội bộ tham khảo (nếu có)"
    )
    config: Optional[ContentConfig] = None

    title: Optional[str] = Field(
        default=None, 
        description="Tiêu đề bài viết (nếu có từ bước filtering)"
    )
    # ===== THAY ĐỔI: outline giờ là List[OutlineItem] =====
    outline: Optional[List[OutlineItem]] = Field(
        default=None,
        description="Outline structured của bài viết (đã có thể có config)"
    )
    main_keyword: Optional[str] = Field(
        default=None,
        description="Từ khóa chính cho bài viết"
    )
    secondary_keywords: Optional[List[str]] = Field(
        default=None,
        description="Danh sách từ khóa phụ"
    ) 

class ContentResponse(BaseModel):
    success: bool
    article: Optional[SEOArticle] = None
    article_id: Optional[int] = None
    message: Optional[str] = None  # Thêm message field để báo lỗi