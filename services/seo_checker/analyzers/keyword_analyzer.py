# services/seo_checker/analyzers/keyword_analyzer.py

"""
Keyword Analyzer Module
"""

from typing import Tuple, List
import logging
from ..scoring.recommendation import Issue, IssueSeverity

logger = logging.getLogger(__name__)

class KeywordAnalyzer:
    """Phân tích keyword optimization"""
    def __init__(self, parser, config_manager, title: str, meta_description: str, 
                 keywords: List[str], clean_text: str, word_count: int):
        self.parser = parser
        self.config = config_manager
        self.title = title
        self.meta = meta_description
        self.keywords = keywords
        self.clean_text = clean_text
        self.word_count = word_count
    
    def analyze(self) -> Tuple[float, List[Issue]]:
        """Phân tích keyword optimization"""
        thresholds = self.config.get_thresholds()
        weights = self.config.get_scoring_weights()
        max_score = weights.get('keyword_optimization', 25)
        score = max_score
        issues = []

        # Chuẩn hóa text để so sánh
        text_lower = self.clean_text.lower()
        title_lower = self.title.lower()
        meta_lower = self.meta.lower()
        first_para = self.parser.get_first_paragraph().lower()

        # Lấy headings để kiểm tra
        headings = self.parser.get_headings()
        h1_text = ' '.join(headings['h1']).lower()
        h2_text = ' '.join(headings['h2']).lower()

        for keyword in self.keywords:
            kw_lower = keyword.lower()
            
            # 1. Đếm xuất hiện và tính mật độ
            count = text_lower.count(kw_lower)
            density = (count / max(1, self.word_count)) * 100
            
            # 2. Kiểm tra keyword stuffing
            stuffing_threshold = thresholds.get('keyword_density', {}).get('stuffing_threshold', 4.0)
            if density > stuffing_threshold:
                penalty = self.config.get_penalty('keyword_stuffing')
                score -= penalty
                issues.append(Issue(
                    type="keyword_stuffing",
                    detail=f"Keyword '{keyword}' xuất hiện quá nhiều ({density:.2f}%) - vượt ngưỡng {stuffing_threshold}%",
                    severity=IssueSeverity.CRITICAL,
                    penalty=penalty,
                    recommendation=f"Giảm mật độ xuống dưới {stuffing_threshold}%, tập trung vào chất lượng nội dung"
                ))

            # 3. Kiểm tra density tối ưu
            keyword_density_config = thresholds.get('keyword_density', {})
            optimal_density = keyword_density_config.get('optimal', 1.5)
            min_density = keyword_density_config.get('min', 0.5)
            
            if density < min_density:
                issues.append(Issue(
                    type="keyword_density_too_low",
                    detail=f"Keyword '{keyword}' xuất hiện quá ít ({density:.2f}%) - dưới ngưỡng tối thiểu {min_density}%",
                    severity=IssueSeverity.WARNING,
                    penalty=3,
                    recommendation=f"Tăng tần suất xuất hiện lên khoảng {optimal_density}%, đảm bảo keyword xuất hiện tự nhiên"
                ))
                score -= 3

            # 4. Kiểm tra keyword trong TITLE (quan trọng nhất)
            if kw_lower not in title_lower:
                issues.append(Issue(
                    type="keyword_not_in_title",
                    detail=f"Keyword '{keyword}' không có trong tiêu đề bài viết",
                    severity=IssueSeverity.WARNING,
                    penalty=5,
                    recommendation="Thêm keyword chính vào title tag, ưu tiên đứng đầu title"
                ))
                score -= 5
            
            # 5. Kiểm tra keyword trong META DESCRIPTION
            if kw_lower not in meta_lower:
                issues.append(Issue(
                    type="keyword_not_in_meta",
                    detail=f"Keyword '{keyword}' không có trong meta description",
                    severity=IssueSeverity.WARNING,
                    penalty=3,
                    recommendation="Thêm keyword vào meta description để tăng CTR từ kết quả tìm kiếm"
                ))
                score -= 3
            
            # 6. Kiểm tra keyword trong ĐOẠN ĐẦU (first paragraph)
            if kw_lower not in first_para:
                issues.append(Issue(
                    type="keyword_not_in_first_paragraph",
                    detail=f"Keyword '{keyword}' không xuất hiện trong đoạn văn đầu tiên",
                    severity=IssueSeverity.INFO,
                    penalty=2,
                    recommendation="Nhắc đến keyword chính trong 100 từ đầu tiên để Google hiểu chủ đề nhanh"
                ))
                score -= 2
            
            # 7. Kiểm tra keyword trong H1 (nếu có H1)
            if h1_text and kw_lower not in h1_text:
                issues.append(Issue(
                    type="keyword_not_in_h1",
                    detail=f"Keyword '{keyword}' không có trong thẻ H1 chính",
                    severity=IssueSeverity.WARNING,
                    penalty=3,
                    recommendation="Đảm bảo keyword chính xuất hiện trong H1 của bài viết"
                ))
                score -= 3
            
            # 8. Kiểm tra keyword trong ít nhất 1 H2
            if h2_text and kw_lower not in h2_text:
                issues.append(Issue(
                    type="keyword_not_in_h2",
                    detail=f"Keyword '{keyword}' không xuất hiện trong bất kỳ thẻ H2 nào",
                    severity=IssueSeverity.INFO,
                    penalty=1,
                    recommendation="Sử dụng keyword trong ít nhất 1 tiêu đề phụ (H2) để củng cố chủ đề"
                ))
                score -= 1
        
        return max(0, min(score, max_score)), issues