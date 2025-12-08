"""
Readability Analyzer Module
"""

from typing import Tuple, List
import re
import logging
from ..scoring.recommendation import Issue, IssueSeverity

logger = logging.getLogger(__name__)


class ReadabilityAnalyzer:
    """Phân tích khả năng đọc"""
    
    def __init__(self, parser, config_manager, clean_text: str):
        self.parser = parser
        self.config = config_manager
        self.clean_text = clean_text
    
    def analyze(self) -> Tuple[float, List[Issue]]:
        """Phân tích khả năng đọc"""
        thresholds = self.config.get_thresholds()
        # SỬA: Lấy từ config_manager.get_scoring_weights()
        weights = self.config.get_scoring_weights()
        max_score = weights.get('readability', 20)  # Sửa dòng này
        score = max_score
        issues = []
        
        # Kiểm tra độ dài đoạn văn
        para_stats = self.parser.get_paragraphs_stats()
        # SỬA: Thêm .get() với giá trị mặc định
        max_para_words = thresholds.get('paragraph', {}).get('max_words', 150)
        
        long_paragraphs = [p for p in para_stats if p['word_count'] > max_para_words]
        for para in long_paragraphs[:3]:  # Chỉ báo 3 đoạn đầu
            penalty = self.config.get_penalty('paragraph_too_long')
            score -= penalty
            issues.append(Issue(
                type="paragraph_too_long",
                detail=f"Đoạn #{para['index']} có {para['word_count']} từ",
                severity=IssueSeverity.WARNING,
                penalty=penalty,
                recommendation=f"Chia nhỏ đoạn văn, tối đa {max_para_words} từ/đoạn"
            ))
        
        # Kiểm tra độ dài câu
        sentences = re.split(r'[.!?]+', self.clean_text)
        # SỬA: Thêm .get() với giá trị mặc định
        max_sentence_words = thresholds.get('sentence', {}).get('max_words', 25)
        
        long_sentences = [s for s in sentences if len(s.strip().split()) > max_sentence_words]
        if len(long_sentences) > 5:
            score -= 5
            issues.append(Issue(
                type="many_long_sentences",
                detail=f"Có {len(long_sentences)} câu dài hơn {max_sentence_words} từ",
                severity=IssueSeverity.WARNING,
                penalty=5,
                recommendation="Viết câu ngắn gọn hơn để dễ đọc"
            ))
        
        return max(0, min(score, max_score)), issues