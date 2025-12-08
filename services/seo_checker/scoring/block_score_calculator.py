# services/seo_checker/scoring/block_score_calculator.py
"""
BlockScoreCalculator - Phiên bản block-based của AdvancedSEOAnalyzer
"""
from typing import List, Tuple, Dict, Any, Optional
import logging
from .block_issues import BlockScoreBreakdown, BlockIssue

logger = logging.getLogger(__name__)

class BlockSEOAnalyzer:
    """Analyzer block-based chuyên nghiệp"""
    
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
        self.word_count = parser.get_total_word_count()
        
        self.issues: List[BlockIssue] = []
        self.bonuses: List[Tuple[str, int]] = []
        
        # Khởi tạo các BLOCK-BASED analyzer
        self._init_analyzers()
    
    def _init_analyzers(self):
        """Khởi tạo các block-based analyzer"""
        parser_type = self.parser.get_parser_type()
        
        if parser_type == "block":
            # Dùng block-based analyzers
            from ..analyzers.block_based.structure_analyzer import BlockStructureAnalyzer
            from ..analyzers.block_based.keyword_analyzer import BlockKeywordAnalyzer
            from ..analyzers.block_based.readability_analyzer import BlockReadabilityAnalyzer
            from ..analyzers.technical_analyzer import TechnicalSEOAnalyzer
            from ..analyzers.content_quality_analyzer import ContentQualityAnalyzer
            
            self.structure_analyzer = BlockStructureAnalyzer(self.parser, self.config)
            self.keyword_analyzer = BlockKeywordAnalyzer(
                self.parser, self.config, self.title, self.meta, 
                self.keywords, self.clean_text, self.word_count
            )
            self.readability_analyzer = BlockReadabilityAnalyzer(
                self.parser, self.config, self.clean_text
            )
        else:
            # Dùng analyzers cũ cho HTML fallback
            from ..analyzers.structure_analyzer import StructureAnalyzer
            from ..analyzers.keyword_analyzer import KeywordAnalyzer
            from ..analyzers.readability_analyzer import ReadabilityAnalyzer
        
        # Technical và Content analyzer giữ nguyên (cần update sau)
        from ..analyzers.technical_analyzer import TechnicalSEOAnalyzer
        from ..analyzers.content_quality_analyzer import ContentQualityAnalyzer
        
        self.technical_analyzer = TechnicalSEOAnalyzer(
            self.parser, self.config, self.title, self.meta
        )
        self.content_analyzer = ContentQualityAnalyzer(
            self.config, self.word_count
        )
    
    def calculate_total_score(self) -> BlockScoreBreakdown:
        """Tính tổng điểm với BLOCK ISSUES"""
        # Gọi các analyzer
        structure_score, structure_issues = self.structure_analyzer.analyze()
        keyword_score, keyword_issues = self.keyword_analyzer.analyze()
        readability_score, readability_issues = self.readability_analyzer.analyze()
        technical_score, technical_issues = self.technical_analyzer.analyze()
        content_score, content_issues = self.content_analyzer.analyze()
        
        # Tổng hợp tất cả issues (đã là BlockIssue)
        self.issues = (structure_issues + keyword_issues + readability_issues + 
                      self._convert_to_block_issues(technical_issues) + 
                      self._convert_to_block_issues(content_issues))
        
        # Tính bonus
        self._calculate_bonuses()
        bonus_total = sum(bonus[1] for bonus in self.bonuses)
        
        # Tổng điểm
        total = (structure_score + keyword_score + readability_score + 
                technical_score + content_score + bonus_total)
        
        # Xếp loại
        grade = self._calculate_grade(total)
        
        return BlockScoreBreakdown(
            structure_score=round(structure_score, 1),
            keyword_score=round(keyword_score, 1),
            readability_score=round(readability_score, 1),
            technical_score=round(technical_score, 1),
            content_quality_score=round(content_score, 1),
            bonus_points=round(bonus_total, 1),
            total_score=round(total, 1),
            grade=grade,
            issues=self.issues
        )
    
    def _convert_to_block_issues(self, old_issues) -> List[BlockIssue]:
        """Chuyển đổi issues cũ sang BlockIssue format"""
        block_issues = []
        for issue in old_issues:
            # Chuyển đổi severity
            from .block_issues import BlockIssueSeverity
            severity_map = {
                "critical": BlockIssueSeverity.CRITICAL,
                "warning": BlockIssueSeverity.WARNING,
                "info": BlockIssueSeverity.INFO
            }
            
            block_issues.append(BlockIssue(
                type=issue.type,
                block_id="",  # Không có block_id cụ thể cho technical/content issues
                severity=severity_map.get(issue.severity.value, BlockIssueSeverity.INFO),
                penalty=issue.penalty,
                detail=issue.detail,
                recommendation=issue.recommendation
            ))
        return block_issues
    
    def _calculate_bonuses(self):
        """Tính điểm thưởng (giữ nguyên logic)"""
        headings = self.parser.get_headings()
        h1_count = len(headings.get('h1', []))
        h2_count = len(headings.get('h2', []))
        h2_min = self.thresholds.get('headings', {}).get('h2_min', 3)
        
        if h1_count == 1 and h2_count >= h2_min:
            bonus = self.config.get_bonus('good_heading_structure')
            if bonus:
                self.bonuses.append(('good_heading_structure', bonus))
    
    def _calculate_grade(self, total_score: float) -> str:
        """Tính xếp loại (giữ nguyên logic)"""
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