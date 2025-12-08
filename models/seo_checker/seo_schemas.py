"""
Schema cho SEO Checker API
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from enum import Enum


class IssueSeverity(str, Enum):
    """Mức độ nghiêm trọng của issue"""
    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"


class IssueSchema(BaseModel):
    """Schema cho issue"""
    type: str = Field(..., description="Loại issue")
    detail: str = Field(..., description="Chi tiết issue")
    severity: IssueSeverity = Field(..., description="Mức độ nghiêm trọng")
    penalty: int = Field(0, description="Điểm phạt")
    recommendation: str = Field("", description="Khuyến nghị khắc phục")


class ScoreBreakdownSchema(BaseModel):
    """Schema cho breakdown điểm số"""
    structure: float = Field(0, description="Điểm cấu trúc")
    keyword_optimization: float = Field(0, description="Điểm tối ưu từ khóa")
    readability: float = Field(0, description="Điểm khả năng đọc")
    technical_seo: float = Field(0, description="Điểm technical SEO")
    content_quality: float = Field(0, description="Điểm chất lượng nội dung")
    bonus: float = Field(0, description="Điểm thưởng")
    total: float = Field(0, description="Tổng điểm")
    grade: str = Field("F", description="Xếp loại")


class BonusSchema(BaseModel):
    """Schema cho điểm thưởng"""
    type: str = Field(..., description="Loại bonus")
    points: int = Field(0, description="Số điểm")


class StatsSchema(BaseModel):
    """Schema cho thống kê"""
    word_count: int = Field(0, description="Số từ")
    title_length: int = Field(0, description="Độ dài tiêu đề")
    meta_length: int = Field(0, description="Độ dài meta description")
    headings: Dict[str, List[str]] = Field(default_factory=dict, description="Danh sách headings")
    images_count: int = Field(0, description="Số lượng ảnh")
    links: Dict[str, int] = Field(default_factory=dict, description="Số lượng link")


class SEOCheckerRequest(BaseModel):
    """Request schema cho SEO Checker"""
    title: str = Field(..., description="Tiêu đề bài viết")
    meta_description: str = Field(..., description="Meta description")
    content: str = Field(..., description="Nội dung HTML")
    keywords: List[str] = Field(default_factory=list, description="Danh sách từ khóa")
    industry: Optional[str] = Field(None, description="Ngành áp dụng (optional)")


class SEOCheckerResponse(BaseModel):
    """Response schema cho SEO Checker"""
    score_breakdown: ScoreBreakdownSchema = Field(..., description="Breakdown điểm số")
    issues: Dict[str, List[IssueSchema]] = Field(..., description="Issues theo mức độ")
    bonuses: List[BonusSchema] = Field(default_factory=list, description="Danh sách bonus")
    stats: StatsSchema = Field(..., description="Thống kê")
    config_used: Dict[str, Any] = Field(default_factory=dict, description="Cấu hình sử dụng")
    success: bool = Field(True, description="Trạng thái thành công")
    message: str = Field("", description="Thông báo")