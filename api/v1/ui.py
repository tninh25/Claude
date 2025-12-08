# api/v1/ui.py
"""
    Endpoints thực hiện lấy cấu hình để UI hiển thị
"""

import logging
from fastapi import APIRouter
from services.ui_config.config_service import ConfigService
from models.ui.ui_config import ContentKeysResponse

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/content-types", response_model=ContentKeysResponse)
async def get_content_type_keys():
    logger.info("Fetching content types for UI")
    keys = ConfigService.get_all_content_type_names()
    return ContentKeysResponse(keys=keys)

@router.get("/writing-tones", response_model=ContentKeysResponse)
async def get_writing_tone_keys():
    logger.info("Fetching writing tones for UI")
    keys = ConfigService.get_all_tone_names()
    return ContentKeysResponse(keys=keys)

@router.get("/languages", response_model=ContentKeysResponse)
async def get_language_keys():
    logger.info("Fetching languages for UI")
    keys = ConfigService.get_all_language_names()
    return ContentKeysResponse(keys=keys)

@router.get("/bots", response_model=ContentKeysResponse)
async def get_bot_keys():
    logger.info("Fetching bots for UI")
    keys = ConfigService.get_all_bot_names()
    return ContentKeysResponse(keys=keys)

@router.get("/configs")
async def get_all_configs():
    logger.info("Fetching all UI configurations")
    return {
        "content_types": ConfigService.get_all_content_type_names(),
        "writing_tones": ConfigService.get_all_tone_names(),
        "languages": ConfigService.get_all_language_names(),
        "bots": ConfigService.get_all_bot_names()
    }