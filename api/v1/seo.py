"""
API endpoint cho SEO Checker
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import logging
import os
from pathlib import Path

from models.seo_checker.seo_schemas import (
    SEOCheckerRequest,
    SEOCheckerResponse
)
from models.seo_checker.fix_schemas import AutoFixRequest, AutoFixResponse

from services.seo_checker.seo_service import SEOCheckerService
from models.llm.content_generation_schemas import SEOArticle
from services.seo_checker.seo_auto_fix_service import SEOAutoFixService

logger = logging.getLogger(__name__)

# Tạo router
router = APIRouter()


BASE_DIR = Path(__file__).parent.parent.parent
CONFIG_DIR = BASE_DIR / "core" / "score_yaml"

# In ra để debug
print(f"BASE_DIR từ seo.py: {BASE_DIR}")
print(f"CONFIG_DIR từ seo.py: {CONFIG_DIR}")

# Tạo service
seo_service = SEOCheckerService(config_dir=str(CONFIG_DIR))
seo_auto_fix_service = SEOAutoFixService(config_dir=str(CONFIG_DIR))

@router.post("/analyze-blocks", response_model=SEOCheckerResponse)
async def analyze_seo_with_blocks(article: SEOArticle) -> SEOCheckerResponse:
    """
    Phân tích SEO với cấu trúc blocks
    
    Args:
        article: SEOArticle với blocks
        
    Returns:
        Kết quả phân tích SEO với block issues
    """
    try:
        logger.info(f"Bắt đầu phân tích SEO với blocks: {article.title[:50]}...")
        logger.info(f"Số lượng blocks: {len(article.blocks) if article.blocks else 0}")
        
        # Gọi service phân tích với blocks
        result = seo_service.analyze_seo_with_blocks(article)
        
        # Lưu kết quả
        seo_service.save_result(result)
        
        logger.info(f"Phân tích SEO với blocks thành công, điểm: {result['score_breakdown']['total']}")
        logger.info(f"Số issues tìm thấy: {sum(len(issues) for issues in result['issues'].values())}")
        
        # Hiển thị ví dụ về block issues
        if result['issues']:
            for severity, issues in result['issues'].items():
                for issue in issues[:2]:  # Hiển thị 2 issue đầu mỗi loại
                    logger.info(f"Issue mẫu - {severity}: {issue.get('type')} tại block {issue.get('block_id')}")
        
        return SEOCheckerResponse(**result)
        
    except Exception as e:
        logger.error(f"Lỗi phân tích SEO với blocks: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Lỗi phân tích SEO với blocks: {str(e)}")
    
@router.post("/analyze", response_model=SEOCheckerResponse)
async def analyze_seo(request: SEOCheckerRequest) -> SEOCheckerResponse:
    """
    Phân tích SEO cho bài viết
    
    Args:
        request: Dữ liệu bài viết cần phân tích
        
    Returns:
        Kết quả phân tích SEO chi tiết
    """
    try:
        logger.info(f"Bắt đầu phân tích SEO: {request.title[:50]}...")
        
        # Chuyển request thành dict
        request_data = {
            "title": request.title,
            "meta_description": request.meta_description,
            "content": request.content,
            "keywords": request.keywords,
            "industry": request.industry
        }
        
        # Gọi service phân tích
        result = seo_service.analyze_seo(request_data)
        
        # Lưu kết quả
        seo_service.save_result(result)
        
        logger.info(f"Phân tích SEO thành công, điểm: {result['score_breakdown']['total']}")
        
        # Trả về response
        return SEOCheckerResponse(**result)
        
    except ValueError as e:
        logger.error(f"Lỗi validate: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Lỗi server: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Lỗi phân tích SEO: {str(e)}")


@router.post("/analyze-html", response_model=SEOCheckerResponse)
async def analyze_seo_html(
    title: str,
    meta_description: str,
    html_content: str,
    keywords: str = "",
    industry: str = None
) -> SEOCheckerResponse:
    """
    Phân tích SEO từ các tham số riêng lẻ (cho API cũ)
    
    Args:
        title: Tiêu đề bài viết
        meta_description: Meta description
        html_content: Nội dung HTML
        keywords: Từ khóa (phân cách bằng dấu phẩy)
        industry: Ngành (optional)
        
    Returns:
        Kết quả phân tích SEO
    """
    try:
        logger.info(f"Bắt đầu phân tích SEO từ HTML: {title[:50]}...")
        
        # Parse keywords
        keyword_list = [k.strip() for k in keywords.split(",") if k.strip()] if keywords else []
        
        # Tạo request data
        request_data = {
            "title": title,
            "meta_description": meta_description,
            "content": html_content,
            "keywords": keyword_list,
            "industry": industry
        }
        
        # Gọi service
        result = seo_service.analyze_seo(request_data)
        
        # Lưu kết quả
        seo_service.save_result(result)
        
        return SEOCheckerResponse(**result)
        
    except Exception as e:
        logger.error(f"Lỗi: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/auto-fix", response_model=AutoFixResponse)
async def auto_fix_seo(request: AutoFixRequest) -> AutoFixResponse:
    """
    Tự động sửa SEO cho bài viết - UPDATED
    """
    try:
        logger.info(f"Starting auto-fix for article: {request.article.get('title', '')[:50]}...")
        
        # Chuyển đổi article dict sang SEOArticle
        article = SEOArticle(**request.article)
        
        # Thực hiện auto-fix
        result = await seo_auto_fix_service.auto_fix_seo(article, request.score_result)
        
        logger.info(f"Auto-fix completed. Applied {len(result.applied_tasks)} tasks.")
        
        return result
        
    except Exception as e:
        logger.error(f"Auto-fix failed: {e}")
        raise HTTPException(status_code=500, detail=f"Lỗi auto-fix: {str(e)}")
    
@router.post("/auto-fix-iterative")
async def auto_fix_seo_iterative(request: AutoFixRequest) -> Dict[str, Any]:
    """
    Tự động sửa SEO với vòng lặp cho đến khi đạt điểm tối thiểu
    
    Args:
        request: Chứa article và score_result
        
    Returns:
        Kết quả với lịch sử các lần fix
    """
    try:
        logger.info(f"Starting iterative auto-fix for article: {request.article.get('title', '')[:50]}...")
        
        # Chuyển đổi article dict sang SEOArticle
        article = SEOArticle(**request.article)
        
        # Thực hiện auto-fix với iteration
        result = await seo_auto_fix_service.auto_fix_with_iteration(
            article, 
            initial_score=request.score_result
        )
        
        logger.info(f"Iterative auto-fix completed. Total iterations: {result['total_iterations']}")
        logger.info(f"Score improvement: {result['score_improvement']} points")
        
        return result
        
    except Exception as e:
        logger.error(f"Iterative auto-fix failed: {e}")
        raise HTTPException(status_code=500, detail=f"Lỗi iterative auto-fix: {str(e)}")