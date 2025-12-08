# models/image_schemas.py

from pydantic import BaseModel
from typing import List, Optional

class ImageItem(BaseModel):
    """Thông tin hình ảnh"""
    url: str
    thumbnail: str
    title: str
    source: str
    size: str

class ImageSearchRequest(BaseModel):
    """Request tìm kiếm hình ảnh"""
    query: str
    num_results: int = 10

class ImageSearchResponse(BaseModel):
    """Response tìm kiếm hình ảnh"""
    success: bool
    query: str
    total_results: int
    images: List[ImageItem]
    message: Optional[str] = None