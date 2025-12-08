# services/seo_checker/scoring/recommendation.py

"""
    Recommendation and Issue Management Module
"""

from dataclasses import dataclass
from enum import Enum

class IssueSeverity(Enum):
    """Mức nghiêm trọng của issue"""
    CRITICAL = "critical"
    WARNING  = "warning"
    INFO     = "info"

@dataclass
class Issue:
    """Issue với mức nghiêm trọng và điểm phạt"""
    type: str
    detail: str
    severity: IssueSeverity
    penalty: int = 0
    recommendation: str = ""

@dataclass
class ScoreBreakdown:
    """Chi tiết điểm số từng phần"""
    structure_score: float = 0
    keyword_score: float = 0
    readability_score: float = 0
    technical_score: float = 0
    content_quality_score: float = 0
    bonus_points: float = 0
    total_score: float = 0
    grade: str = "F"        # A+, A, B, C, D, F