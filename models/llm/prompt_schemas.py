# app/models/llm/prompt_schemas.py

from pydantic import BaseModel
from typing import List, Optional
from models.llm.content_generation_schemas import ContentConfig

class PromptUpdateRequest(BaseModel):
    article_length: Optional[str] = None
    tone: Optional[str] = None
    article_type: Optional[str] = None
    language: Optional[str] = None
    custome_instructions: Optional[str] = None

class PromptUpdateResponse(BaseModel):
    success: bool
    message: str
    current_config: Optional[ContentConfig] = None