"""
Technical SEO Analyzer Module
Author: Senior Python Engineer & SEO Expert
Version: 2.0
"""

from typing import Tuple, List
import logging
from ..scoring.recommendation import Issue, IssueSeverity

logger = logging.getLogger(__name__)


class TechnicalSEOAnalyzer:
    """Phân tích technical SEO"""
    
    def __init__(self, parser, config_manager, title: str, meta_description: str):
        self.parser = parser
        self.config = config_manager
        self.title = title
        self.meta = meta_description
    
    def analyze(self) -> Tuple[float, List[Issue]]:
        """Phân tích technical SEO"""
        thresholds = self.config.get_thresholds()
        # SỬA: Lấy từ config_manager.get_scoring_weights()
        weights = self.config.get_scoring_weights()
        max_score = weights.get('technical_seo', 15)  # Sửa dòng này
        score = max_score
        issues = []
        
        # Kiểm tra title length
        title_len = len(self.title)
        # SỬA: Thêm .get() với giá trị mặc định
        title_config = thresholds.get('title', {})
        
        if title_len < title_config.get('min_chars', 30):
            score -= 5
            issues.append(Issue(
                type="title_too_short",
                detail=f"Title chỉ có {title_len} ký tự",
                severity=IssueSeverity.CRITICAL,
                penalty=5,
                recommendation=f"Nên có {title_config.get('optimal_min', 50)}-{title_config.get('optimal_max', 60)} ký tự"
            ))
        elif title_len > title_config.get('max_chars', 60):
            score -= 5
            issues.append(Issue(
                type="title_too_long",
                detail=f"Title có {title_len} ký tự - sẽ bị cắt",
                severity=IssueSeverity.CRITICAL,
                penalty=5,
                recommendation=f"Rút ngắn xuống {title_config.get('max_chars', 60)} ký tự"
            ))
        
        # Kiểm tra meta description
        meta_len = len(self.meta)
        # SỬA: Thêm .get() với giá trị mặc định
        meta_config = thresholds.get('meta_description', {})
        
        if meta_len < meta_config.get('min_chars', 120):
            score -= 3
            issues.append(Issue(
                type="meta_too_short",
                detail=f"Meta description chỉ có {meta_len} ký tự",
                severity=IssueSeverity.WARNING,
                penalty=3,
                recommendation=f"Nên có {meta_config.get('min_chars', 120)}-{meta_config.get('max_chars', 160)} ký tự"
            ))
        
        # Kiểm tra images alt text
        images = self.parser.get_images()
        missing_alt = [img for img in images if not img['has_alt']]
        
        if missing_alt:
            penalty = len(missing_alt) * 1
            score -= penalty
            issues.append(Issue(
                type="missing_alt_text",
                detail=f"{len(missing_alt)}/{len(images)} ảnh thiếu alt text",
                severity=IssueSeverity.INFO,
                penalty=penalty,
                recommendation="Thêm mô tả alt cho tất cả ảnh"
            ))
        
        # Kiểm tra links
        links = self.parser.get_links()
        if not links['internal']:
            score -= 3
            issues.append(Issue(
                type="no_internal_links",
                detail="Không có internal links",
                severity=IssueSeverity.WARNING,
                penalty=3,
                recommendation="Thêm 3-5 internal links liên quan"
            ))
        
        return max(0, min(score, max_score)), issues