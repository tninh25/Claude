# models/seo_checker/fix_schemas.py
"""
Schema cho hệ thống auto-fix SEO
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Literal
from enum import Enum

class FixTaskSeverity(str, Enum):
    """Mức độ ưu tiên của fix task"""
    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"

class FixScope(str, Enum):
    """Phạm vi sửa chữa"""
    BLOCK = "block"        # Sửa 1 block cụ thể
    META = "meta"          # Sửa meta field (title, description)
    STRUCTURAL = "structural"  # Sửa cấu trúc (thêm block mới)

class FixTarget(BaseModel):
    """Mục tiêu sửa chữa"""
    scope: FixScope = Field(..., description="Phạm vi sửa")
    block_id: Optional[str] = Field(None, description="ID block cần sửa (nếu scope=block)")
    field_name: Optional[str] = Field(None, description="Tên field (nếu scope=meta)")
    
    class Config:
        schema_extra = {
            "example": {
                "scope": "block",
                "block_id": "p-1"
            }
        }

class FixTask(BaseModel):
    """Task sửa chữa 1 lỗi SEO"""
    task_id: str = Field(..., description="ID duy nhất của task")
    type: str = Field(..., description="Loại lỗi SEO (keyword_not_in_first_paragraph, ...)")
    target: FixTarget = Field(..., description="Mục tiêu sửa chữa")
    payload: Dict[str, Any] = Field(default_factory=dict, description="Dữ liệu cần thiết để sửa")
    current_text: Optional[str] = Field(None, description="Nội dung hiện tại")
    recommendation: str = Field(..., description="Khuyến nghị sửa chữa")
    severity: FixTaskSeverity = Field(..., description="Mức độ ưu tiên")
    status: str = Field("pending", description="Trạng thái: pending, processing, completed, skipped")
    
    class Config:
        schema_extra = {
            "example": {
                "task_id": "fix-001",
                "type": "keyword_not_in_first_paragraph",
                "target": {
                    "scope": "block",
                    "block_id": "p-1"
                },
                "payload": {
                    "keyword": "nâng cấp chatgpt 5.0"
                },
                "current_text": "Trong bối cảnh công nghệ hiện đại...",
                "recommendation": "Chèn keyword 'nâng cấp chatgpt 5.0' vào đoạn mở đầu",
                "severity": "info",
                "status": "pending"
            }
        }

class PatchOperation(BaseModel):
    """Operation patch cho 1 block hoặc field"""
    operation_id: str = Field(..., description="ID của operation")
    task_id: str = Field(..., description="ID task tương ứng")
    scope: FixScope = Field(..., description="Phạm vi áp dụng")
    
    # Chỉ 1 trong các field dưới đây được set
    block_patch: Optional[Dict[str, Any]] = Field(None, description="Patch cho block")
    meta_patch: Optional[Dict[str, Any]] = Field(None, description="Patch cho meta field")
    structural_patch: Optional[Dict[str, Any]] = Field(None, description="Patch cấu trúc")
    
    description: str = Field(..., description="Mô tả patch")
    applied: bool = Field(False, description="Đã áp dụng chưa")

class AutoFixRequest(BaseModel):
    """Request cho API auto-fix"""
    article: Dict[str, Any] = Field(..., description="Bài viết cần sửa")
    score_result: Dict[str, Any] = Field(..., description="Kết quả chấm điểm SEO")

class AutoFixResponse(BaseModel):
    """Response cho API auto-fix"""
    patched_article: Dict[str, Any] = Field(..., description="Bài viết đã sửa")
    applied_tasks: List[FixTask] = Field(default_factory=list, description="Các task đã áp dụng")
    skipped_tasks: List[FixTask] = Field(default_factory=list, description="Các task bị bỏ qua")
    new_score: Optional[Dict[str, Any]] = Field(None, description="Điểm số mới")
    success: bool = Field(True, description="Thành công hay không")
    message: str = Field("", description="Thông báo")


