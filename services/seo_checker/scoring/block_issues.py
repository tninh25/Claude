# services/seo_checker/scoring/block_issues.py
"""
Issue với block_id cho block-based analysis
"""
from dataclasses import dataclass
from enum import Enum
from typing import List

class BlockIssueSeverity(Enum):
    """Mức nghiêm trọng của issue"""
    CRITICAL = "critical"
    WARNING  = "warning"
    INFO     = "info"

@dataclass
class BlockIssue:
    """Issue gắn với block cụ thể"""
    type: str                    # Loại issue (snake_case)
    block_id: str                # ID của block gây lỗi
    severity: BlockIssueSeverity # Mức độ nghiêm trọng
    penalty: int = 0             # Điểm phạt
    detail: str = ""             # Chi tiết lỗi
    recommendation: str = ""     # Khuyến nghị sửa cụ thể
    
    def to_dict(self) -> dict:
        """Chuyển thành dict format chuẩn"""
        return {
            "type": self.type,
            "block_id": self.block_id,
            "severity": self.severity.value,
            "penalty": self.penalty,
            "detail": self.detail,
            "recommendation": self.recommendation
        }

@dataclass
class BlockScoreBreakdown:
    """Chi tiết điểm số cho block-based"""
    structure_score: float = 0
    keyword_score: float = 0
    readability_score: float = 0
    technical_score: float = 0
    content_quality_score: float = 0
    bonus_points: float = 0
    total_score: float = 0
    grade: str = "F"
    issues: List[BlockIssue] = None  # Thay thế issues cũ bằng BlockIssue
    
    def __post_init__(self):
        if self.issues is None:
            self.issues = []