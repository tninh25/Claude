# models/seo_checker/block_schemas.py
"""
Schema cho block-based SEO analysis
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class ArticleBlock(BaseModel):
    """Block cơ bản trong bài viết"""
    id: str = Field(..., description="ID duy nhất của block (ví dụ: h1-1, p-3)")
    tag: str = Field(..., description="Loại tag: h1 | h2 | h3 | p | li")
    text: str = Field(..., description="Nội dung text của block")
    word_count: Optional[int] = Field(None, description="Số từ trong block")

