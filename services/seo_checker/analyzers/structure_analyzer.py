# services/seo_checker/analyzers/structure_analyzer.py

"""
Structure Analyzer Module:
    - H1 vừa đủ
    - Đủ H2
    - Không quá nhiều H3
"""

from typing import Tuple, List
import logging
from ..scoring.recommendation import Issue, IssueSeverity

logger = logging.getLogger(__name__)


class StructureAnalyzer:
    """Phân tích cấu trúc bài viết"""
    
    def __init__(self, parser, config_manager):
        self.parser = parser
        self.config = config_manager
    
    def analyze(self) -> Tuple[float, List[Issue]]:
        """Phân tích cấu trúc - trả về điểm và issues"""
        thresholds = self.config.get_thresholds()
        weights = self.config.get_scoring_weights()
        max_score = weights.get('structure', 20)  # Lấy từ config file
        score = max_score
        issues = []
        
        headings = self.parser.get_headings()
        h1_count = len(headings['h1'])
        h2_count = len(headings['h2'])
        h3_count = len(headings['h3'])
        
        # Kiểm tra H1
        if h1_count == 0:
            penalty = self.config.get_penalty('missing_h1')
            score -= penalty
            issues.append(Issue(
                type="missing_h1",
                detail="Bài viết thiếu thẻ H1 - Cực kỳ quan trọng cho SEO",
                severity=IssueSeverity.CRITICAL,
                penalty=penalty,
                recommendation="Thêm 1 thẻ H1 duy nhất chứa keyword chính"
            ))
        elif h1_count > 1:
            penalty = self.config.get_penalty('multiple_h1')
            score -= penalty
            issues.append(Issue(
                type="multiple_h1",
                detail=f"Có {h1_count} thẻ H1 - Chỉ nên có 1",
                severity=IssueSeverity.CRITICAL,
                penalty=penalty,
                recommendation="Giữ lại 1 H1 chính, chuyển các H1 khác thành H2"
            ))
        
        # Kiểm tra H2
        h2_min = thresholds.get('headings', {}).get('h2_min', 3)
        if h2_count < h2_min:
            penalty = self.config.get_penalty('few_h2')
            score -= penalty
            issues.append(Issue(
                type="few_h2",
                detail=f"Chỉ có {h2_count} thẻ H2, nên có ít nhất {h2_min}",
                severity=IssueSeverity.WARNING,
                penalty=penalty,
                recommendation=f"Thêm {h2_min - h2_count} thẻ H2 để cấu trúc rõ ràng hơn"
            ))
        
        # Kiểm tra H3
        h3_max = thresholds.get('headings', {}).get('h3_max', 15)
        if h3_count > h3_max:
            issues.append(Issue(
                type="too_many_h3",
                detail=f"Có {h3_count} thẻ H3 - quá nhiều",
                severity=IssueSeverity.INFO,
                penalty=2,
                recommendation="Xem xét nhóm các H3 lại hoặc giảm bớt"
            ))
            score -= 2
        
        return max(0, min(score, max_score)), issues

if __name__ == '__main__':
    pass