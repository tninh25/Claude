from functools import lru_cache
from typing import Generator
from services.facebook_service import FacebookService
import os

@lru_cache()
def get_facebook_service() -> FacebookService:
    """
    Khởi tạo Facebook Service với token và page_id từ environment variables
    """
    page_access_token = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN")
    page_id = os.getenv("FACEBOOK_PAGE_ID")
    
    if not page_access_token or not page_id:
        raise ValueError("Facebook Page Access Token và Page ID phải được cấu hình trong environment variables")
    
    return FacebookService(page_access_token, page_id)

def facebook_service_dependency() -> Generator[FacebookService, None, None]:
    """
    Dependency injection cho Facebook Service
    """
    service = get_facebook_service()
    try:
        yield service
    finally:
        # Cleanup nếu cần
        pass