# api/v1/prompt.py
"""
    Các endpoints cho phép cập nhật prompt chatbot:
        - Cập nhật prompt theo cấu hình trên web (độ dài, tone, phong cách, dạng bài...)
        - Load cấu hình hiện tại để cung cấp cho chatbot
"""

import logging
from fastapi import APIRouter, HTTPException

from models.llm.prompt_schemas import PromptUpdateRequest, PromptUpdateResponse
from models.llm.content_generation_schemas import ContentConfig
from services.prompt.prompt_service import PromptService

logger = logging.getLogger(__name__)

# Khai báo router
router = APIRouter()

prompt_service = PromptService()

@router.put("/content-config", response_model=PromptUpdateResponse, description="Cập nhật cấu hình prompt cho content generation")
async def update_prompt_config(request: PromptUpdateRequest):
    try:
        logger.info(f"Update prompt config: {request.dict()}")
        return await prompt_service.update_prompt_config(request)
    except Exception as e:
        logger.error(f"Prompt update error: {str(e)}")
        return PromptUpdateResponse(
            success=False,
            message=f"Failed to update prompt: {str(e)}"
        )

@router.get("/content-config", response_model=ContentConfig, description="Lấy cấu hình prompt hiện tại")
async def get_current_config():
    try:
        return await prompt_service.get_current_config()
    except Exception as e:
        logger.error(f"Get config error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get current config")