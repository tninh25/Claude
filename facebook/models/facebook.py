from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class PostType(str, Enum):
    TEXT = "text"
    PHOTO = "photo"
    VIDEO = "video"
    LINK = "link"

class FacebookPostCreate(BaseModel):
    message: Optional[str] = Field(None, description="Nội dung bài viết")
    link: Optional[str] = Field(None, description="URL nếu đăng link")
    scheduled_publish_time: Optional[int] = Field(None, description="Thời gian lên lịch (timestamp)")

class FacebookPostUpdate(BaseModel):
    message: Optional[str] = Field(None, description="Nội dung cập nhật")

class FacebookPostResponse(BaseModel):
    id: str
    message: Optional[str]
    created_time: Optional[str]
    updated_time: Optional[str]
    permalink_url: Optional[str]
    
    class Config:
        from_attributes = True

class FacebookPostListResponse(BaseModel):
    posts: List[FacebookPostResponse]
    total: int

class FacebookPostDeleteResponse(BaseModel):
    success: bool
    post_id: str
    message: str