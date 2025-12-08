# models/wordpress/post.py

from pydantic import BaseModel
from typing import List, Optional, Union, Literal

class ArticleCreate(BaseModel):
    """Cấu trúc models đăng bài lên wordpress"""
    title: str
    content: str
    status: str = "draft"
    slug: Optional[str] = None
    categories: Optional[Union[List[str], str]] = None
    tags: Optional[Union[List[str], str]] = None
    featured_image_url: Optional[str] = None
    excerpt: Optional[str] = None