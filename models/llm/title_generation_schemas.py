# models/title_generation_schemas.py

from pydantic import BaseModel, Field
from typing import List, Optional

class TitleSuggestionRequest(BaseModel):
    """
    Input cho use-case: Gợi ý tiêu đề theo từ khóa (xem xét mở rộng theo nội dung)
    """
    main_keyword: str
    secondary_keywords: Optional[List[str]] = []
    language: str = Field(default="Tiếng Việt", description="Ngôn ngữ")

class TitleSuggestionResponse(BaseModel):
    """
    Output: Danh sách tiêu đề được LLM tạo
    """
    success: bool
    titles: Optional[List[str]] = []
    total_suggestions: Optional[int] = 0
    message: Optional[str] = None