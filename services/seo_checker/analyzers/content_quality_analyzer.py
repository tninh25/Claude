"""
Content Quality Analyzer Module
"""

from typing import Tuple, List
import logging
from ..scoring.recommendation import Issue, IssueSeverity

logger = logging.getLogger(__name__)


class ContentQualityAnalyzer:
    """Phân tích chất lượng nội dung"""
    
    def __init__(self, config_manager, word_count: int):
        self.config = config_manager
        self.word_count = word_count
    
    def analyze(self) -> Tuple[float, List[Issue]]:
        """Phân tích chất lượng nội dung"""
        thresholds = self.config.get_thresholds()
        weights = self.config.get_scoring_weights()
        max_score = weights.get('content_quality', 20) 
        score = max_score
        issues = []

        wc_config = thresholds.get('word_count', {})
        
        if self.word_count < wc_config.get('min', 900):
            score -= 10
            issues.append(Issue(
                type="content_too_short",
                detail=f"Chỉ có {self.word_count} từ",
                severity=IssueSeverity.CRITICAL,
                penalty=10,
                recommendation=f"Nên có ít nhất {wc_config.get('optimal_min', 1500)} từ"
            ))
        
        return max(0, min(score, max_score)), issues