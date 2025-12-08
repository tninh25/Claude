"""
Score Calculator Module
Author: Senior Python Engineer & SEO Expert
Version: 2.0
"""

from typing import List, Tuple, Dict, Any, Optional
import logging
from .recommendation import ScoreBreakdown, Issue

logger = logging.getLogger(__name__)


class AdvancedSEOAnalyzer:
    """Analyzer chuyên nghiệp với cấu hình từ file"""
    
    def __init__(
        self, 
        parser,
        title: str,
        meta_description: str,
        keywords: List[str],
        config_manager,
        industry: Optional[str] = None
    ):
        self.parser = parser
        self.title = title
        self.meta = meta_description
        self.keywords = keywords
        self.config = config_manager
        self.thresholds = config_manager.get_thresholds(industry)
        self.clean_text = parser.get_clean_text()
        self.word_count = len(self.clean_text.split())
        
        self.issues: List[Issue] = []
        self.bonuses: List[Tuple[str, int]] = []
        
        # Khởi tạo các analyzer
        self._init_analyzers()
    
    def _init_analyzers(self):
        """Khởi tạo các analyzer"""
        # Import tại đây để tránh circular imports
        from ..analyzers.structure_analyzer import StructureAnalyzer
        from ..analyzers.keyword_analyzer import KeywordAnalyzer
        from ..analyzers.readability_analyzer import ReadabilityAnalyzer
        from ..analyzers.technical_analyzer import TechnicalSEOAnalyzer
        from ..analyzers.content_quality_analyzer import ContentQualityAnalyzer
        
        self.structure_analyzer = StructureAnalyzer(self.parser, self.config)
        self.keyword_analyzer = KeywordAnalyzer(
            self.parser, self.config, self.title, self.meta, 
            self.keywords, self.clean_text, self.word_count
        )
        self.readability_analyzer = ReadabilityAnalyzer(
            self.parser, self.config, self.clean_text
        )
        self.technical_analyzer = TechnicalSEOAnalyzer(
            self.parser, self.config, self.title, self.meta
        )
        self.content_analyzer = ContentQualityAnalyzer(
            self.config, self.word_count
        )
    
    def calculate_total_score(self) -> ScoreBreakdown:
        """Tính tổng điểm"""
        # Import Issue và IssueSeverity
        from .recommendation import Issue, IssueSeverity
        
        # Gọi các analyzer
        structure_score, structure_issues = self.structure_analyzer.analyze()
        keyword_score, keyword_issues = self.keyword_analyzer.analyze()
        readability_score, readability_issues = self.readability_analyzer.analyze()
        technical_score, technical_issues = self.technical_analyzer.analyze()
        content_score, content_issues = self.content_analyzer.analyze()
        
        # Tổng hợp issues
        self.issues = (structure_issues + keyword_issues + readability_issues + 
                      technical_issues + content_issues)
        
        # Tính điểm bonus
        self._calculate_bonuses()
        bonus_total = sum(bonus[1] for bonus in self.bonuses)
        
        # Tổng điểm
        total = (structure_score + keyword_score + readability_score + 
                technical_score + content_score + bonus_total)
        
        # Xếp loại
        grade = self._calculate_grade(total)
        
        return ScoreBreakdown(
            structure_score=round(structure_score, 1),
            keyword_score=round(keyword_score, 1),
            readability_score=round(readability_score, 1),
            technical_score=round(technical_score, 1),
            content_quality_score=round(content_score, 1),
            bonus_points=round(bonus_total, 1),
            total_score=round(total, 1),
            grade=grade
        )
    
    def _calculate_bonuses(self):
        """Tính điểm thưởng"""
        # Bonus: Cấu trúc tốt
        headings = self.parser.get_headings()
        h1_count = len(headings['h1'])
        h2_count = len(headings['h2'])
        h2_min = self.thresholds.get('headings', {}).get('h2_min', 3)
        
        if h1_count == 1 and h2_count >= h2_min:
            bonus = self.config.get_bonus('good_heading_structure')
            if bonus:
                self.bonuses.append(('good_heading_structure', bonus))
        
        # Bonus: Keyword ở đoạn đầu
        first_para = self.parser.get_first_paragraph().lower()
        for keyword in self.keywords:
            kw_lower = keyword.lower()
            if kw_lower in first_para:
                bonus = self.config.get_bonus('keyword_in_first_paragraph')
                if bonus:
                    self.bonuses.append((f'keyword_in_first_para_{keyword}', bonus))
        
        # Bonus: Tất cả ảnh có alt text
        images = self.parser.get_images()
        missing_alt = [img for img in images if not img['has_alt']]
        if images and not missing_alt:
            bonus = self.config.get_bonus('all_images_have_alt')
            if bonus:
                self.bonuses.append(('all_images_have_alt', bonus))
        
        # Bonus: Word count tối ưu
        wc_config = self.thresholds.get('word_count', {})
        optimal_min = wc_config.get('optimal_min', 1500)
        optimal_max = wc_config.get('optimal_max', 3000)
        
        if optimal_min <= self.word_count <= optimal_max:
            bonus = self.config.get_bonus('optimal_word_count')
            if bonus:
                self.bonuses.append(('optimal_word_count', bonus))
    
    def _calculate_grade(self, total_score: float) -> str:
        """Tính xếp loại"""
        if total_score >= 90:
            return "A+"
        elif total_score >= 80:
            return "A"
        elif total_score >= 70:
            return "B"
        elif total_score >= 60:
            return "C"
        elif total_score >= 50:
            return "D"
        else:
            return "F"