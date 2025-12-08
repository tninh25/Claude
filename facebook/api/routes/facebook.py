from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from services.facebook_service import FacebookService
from api.dependencies import facebook_service_dependency
from models.facebook import (
    FacebookPostCreate, 
    FacebookPostUpdate, 
    FacebookPostResponse, 
    FacebookPostListResponse,
    FacebookPostDeleteResponse
)

router = APIRouter(prefix="/facebook", tags=["facebook"])

@router.post("/posts", response_model=FacebookPostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    post_data: FacebookPostCreate,
    facebook_service: FacebookService = Depends(facebook_service_dependency)
):
    """
    Tạo bài viết mới trên Facebook Page
    """
    try:
        result = facebook_service.create_post(post_data)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Lỗi khi tạo bài viết: {str(e)}"
        )

@router.get("/posts/{post_id}", response_model=FacebookPostResponse)
async def get_post(
    post_id: str,
    facebook_service: FacebookService = Depends(facebook_service_dependency)
):
    """
    Lấy thông tin chi tiết của một bài viết
    """
    try:
        result = facebook_service.get_post(post_id)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy bài viết: {str(e)}"
        )

@router.put("/posts/{post_id}", response_model=FacebookPostResponse)
async def update_post(
    post_id: str,
    update_data: FacebookPostUpdate,
    facebook_service: FacebookService = Depends(facebook_service_dependency)
):
    """
    Cập nhật nội dung bài viết
    """
    try:
        result = facebook_service.update_post(post_id, update_data)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Lỗi khi cập nhật bài viết: {str(e)}"
        )

@router.delete("/posts/{post_id}", response_model=FacebookPostDeleteResponse)
async def delete_post(
    post_id: str,
    facebook_service: FacebookService = Depends(facebook_service_dependency)
):
    """
    Xóa bài viết
    """
    try:
        result = facebook_service.delete_post(post_id)
        return FacebookPostDeleteResponse(**result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Lỗi khi xóa bài viết: {str(e)}"
        )

@router.get("/posts", response_model=FacebookPostListResponse)
async def get_posts(
    limit: int = 10,
    facebook_service: FacebookService = Depends(facebook_service_dependency)
):
    """
    Lấy danh sách bài viết từ page
    """
    try:
        result = facebook_service.get_posts(limit)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Lỗi khi lấy danh sách bài viết: {str(e)}"
        )