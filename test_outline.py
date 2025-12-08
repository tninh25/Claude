# FIle để bạn tham khảo

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import uvicorn

app = FastAPI(title="SEO Outline API")

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# PYDANTIC MODELS - CONFIG LÀ OPTIONAL
# ==========================================

class OutlineConfig(BaseModel):
    word_count: Optional[int] = Field(None, ge=50, le=5000, description="Số lượng từ")
    keywords: Optional[List[str]] = Field(None, description="Danh sách từ khóa")
    tone: Optional[str] = Field(None, description="Tone giọng viết")
    internal_link: Optional[str] = Field(None, description="Link nội bộ")

class OutlineItem(BaseModel):
    id: str = Field(..., description="ID duy nhất của heading")
    level: int = Field(..., ge=1, le=6, description="Cấp độ heading (1-6)")
    title: str = Field(..., min_length=1, description="Tiêu đề heading")
    order: int = Field(..., ge=1, description="Thứ tự hiển thị")
    config: Optional[OutlineConfig] = Field(None, description="Cấu hình optional")

class OutlineRequest(BaseModel):
    article_id: int = Field(..., description="ID bài viết")
    article_outline: List[OutlineItem] = Field(..., min_items=1)

# ==========================================
# LƯU TẠM TRONG RAM
# ==========================================
outline_storage: Optional[OutlineRequest] = None

# ==========================================
# API ENDPOINTS
# ==========================================

@app.get("/")
def root():
    return {
        "message": "SEO Outline API", 
        "endpoints": [
            "POST /api/outline/generate - Sinh outline không có config",
            "POST /api/outline/save - Lưu outline (config optional)",
            "GET /api/outline/current - Lấy outline đã lưu",
            "DELETE /api/outline/current - Xóa outline"
        ]
    }

@app.post("/api/outline/generate")
def generate_outline():
    """
    Sinh outline mẫu - CHỈ có id, level, title, order
    KHÔNG có field config
    """
    sample_outline = {
        "article_id": 123,
        "article_outline": [
            {
                "id": "h1-1",
                "level": 1,
                "title": "Thiết kế website 2025: Xu hướng và Công nghệ mới",
                "order": 1
            },
            {
                "id": "h2-1",
                "level": 2,
                "title": "Tại sao cần thiết kế website chuyên nghiệp?",
                "order": 2
            },
            {
                "id": "h2-2",
                "level": 2,
                "title": "Các bước thiết kế website hiệu quả",
                "order": 3
            },
            {
                "id": "h3-1",
                "level": 3,
                "title": "Bước 1: Phân tích và lên kế hoạch",
                "order": 4
            },
            {
                "id": "h3-2",
                "level": 3,
                "title": "Bước 2: Thiết kế giao diện UI/UX",
                "order": 5
            },
            {
                "id": "h3-3",
                "level": 3,
                "title": "Bước 3: Phát triển và coding",
                "order": 6
            },
            {
                "id": "h2-3",
                "level": 2,
                "title": "Chi phí thiết kế website",
                "order": 7
            },
            {
                "id": "h2-4",
                "level": 2,
                "title": "Kết luận",
                "order": 8
            }
        ]
    }
    
    return {
        "success": True,
        "data": sample_outline,
        "message": "Đã sinh outline mẫu (không có config)"
    }

@app.post("/api/outline/save")
def save_outline(outline: OutlineRequest):
    """
    Lưu outline - chấp nhận config là optional
    Một số heading có config, một số không có đều được chấp nhận
    """
    global outline_storage
    
    # Validate thứ tự không bị trùng
    orders = [item.order for item in outline.article_outline]
    if len(orders) != len(set(orders)):
        raise HTTPException(
            status_code=400, 
            detail="Thứ tự các heading bị trùng lặp"
        )
    
    # Validate ID không bị trùng
    ids = [item.id for item in outline.article_outline]
    if len(ids) != len(set(ids)):
        raise HTTPException(
            status_code=400, 
            detail="ID các heading bị trùng lặp"
        )
    
    # Đếm số heading có config và không có config
    with_config = sum(1 for item in outline.article_outline if item.config is not None)
    without_config = len(outline.article_outline) - with_config
    
    # Lưu vào RAM
    outline_storage = outline
    
    return {
        "success": True,
        "message": f"Đã lưu outline cho bài viết ID {outline.article_id}",
        "total_headings": len(outline.article_outline),
        "headings_with_config": with_config,
        "headings_without_config": without_config,
        "detail": f"{with_config} heading có cấu hình, {without_config} heading chưa cấu hình"
    }

@app.get("/api/outline/current")
def get_current_outline():
    """
    Lấy outline đang được lưu trong RAM
    """
    if outline_storage is None:
        raise HTTPException(
            status_code=404,
            detail="Chưa có outline nào được lưu"
        )
    
    # Đếm số heading có/không có config
    with_config = sum(1 for item in outline_storage.article_outline if item.config is not None)
    without_config = len(outline_storage.article_outline) - with_config
    
    return {
        "success": True,
        "data": outline_storage.dict(exclude_none=True),
        "stats": {
            "total_headings": len(outline_storage.article_outline),
            "with_config": with_config,
            "without_config": without_config
        }
    }

@app.delete("/api/outline/current")
def clear_outline():
    """
    Xóa outline trong RAM
    """
    global outline_storage
    outline_storage = None
    return {
        "success": True,
        "message": "Đã xóa outline trong bộ nhớ"
    }

# ==========================================
# CHẠY SERVER
# ==========================================
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)