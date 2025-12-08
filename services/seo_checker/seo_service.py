"""
Service chính cho SEO Checker
"""

import os
import json
import logging
from typing import Dict, Any
from pathlib import Path

from .parser.html_parser import EnhancedArticleParser
from .scoring.score_calculator import AdvancedSEOAnalyzer
from .config.config_manager import ConfigManager

logger = logging.getLogger(__name__)


class SEOCheckerService:
    """Service chính để phân tích SEO"""
    
    def __init__(self, config_dir: str = None):
        """
        Khởi tạo service với config
        
        Args:
            config_dir: Thư mục chứa config (mặc định: core/score_yaml)
        """
        if config_dir is None:
            # Xác định đường dẫn config mặc định
            base_dir = Path(__file__).parent.parent.parent.parent
            self.config_dir = base_dir / "core" / "score_yaml"
        else:
            self.config_dir = Path(config_dir)
        
        logger.info(f"SEOCheckerService khởi tạo với config_dir: {self.config_dir}")
    
    def analyze_seo(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Phân tích SEO từ request data
        
        Args:
            request_data: Dict chứa các field cần thiết
            
        Returns:
            Dict chứa kết quả phân tích
        """
        try:
            # Trích xuất dữ liệu từ request
            title = request_data.get('title', '')
            meta_description = request_data.get('meta_description', '')
            content = request_data.get('content', '')
            keywords = request_data.get('keywords', [])
            industry = request_data.get('industry')
            
            # Validate dữ liệu cơ bản
            if not content:
                raise ValueError("Nội dung không được để trống")
            
            # Parse HTML
            parser = EnhancedArticleParser(content)
            
            # Load config
            config_manager = ConfigManager(str(self.config_dir))
            
            # Tạo analyzer
            analyzer = AdvancedSEOAnalyzer(
                parser=parser,
                title=title,
                meta_description=meta_description,
                keywords=keywords,
                config_manager=config_manager,
                industry=industry
            )
            
            # Tính điểm
            score_breakdown = analyzer.calculate_total_score()
            
            # Format kết quả theo schema mới
            result = self._format_result(analyzer, parser, score_breakdown, config_manager, industry)
            
            return result
            
        except Exception as e:
            logger.error(f"Lỗi phân tích SEO: {str(e)}")
            raise
    
    def _format_result(self, analyzer, parser, score_breakdown, config_manager, industry) -> Dict[str, Any]:
        """
        Format kết quả theo schema chuẩn
        
        Args:
            analyzer: AdvancedSEOAnalyzer instance
            parser: EnhancedArticleParser instance
            score_breakdown: ScoreBreakdown object
            config_manager: ConfigManager instance
            industry: Ngành áp dụng
            
        Returns:
            Dict định dạng kết quả
        """
        # Chuyển đổi issues theo mức độ
        issues_by_severity = {
            "critical": [],
            "warning": [],
            "info": []
        }
        
        for issue in analyzer.issues:
            issue_dict = {
                "type": issue.type,
                "detail": issue.detail,
                "severity": issue.severity.value,
                "penalty": issue.penalty,
                "recommendation": issue.recommendation
            }
            issues_by_severity[issue.severity.value].append(issue_dict)
        
        # Format bonuses
        bonuses = []
        for bonus_type, bonus_points in analyzer.bonuses:
            bonuses.append({
                "type": bonus_type,
                "points": bonus_points
            })
        
        # Lấy thống kê
        headings = parser.get_headings()
        links = parser.get_links()
        
        stats = {
            "word_count": analyzer.word_count,
            "title_length": len(analyzer.title),
            "meta_length": len(analyzer.meta),
            "headings": {
                "h1": headings.get('h1', []),
                "h2": headings.get('h2', []),
                "h3": headings.get('h3', []),
                "h4": headings.get('h4', [])
            },
            "images_count": len(parser.get_images()),
            "links": {
                "internal": len(links.get('internal', [])),
                "external": len(links.get('external', []))
            }
        }
        
        # Format score breakdown
        breakdown = {
            "structure": score_breakdown.structure_score,
            "keyword_optimization": score_breakdown.keyword_score,
            "readability": score_breakdown.readability_score,
            "technical_seo": score_breakdown.technical_score,
            "content_quality": score_breakdown.content_quality_score,
            "bonus": score_breakdown.bonus_points,
            "total": score_breakdown.total_score,
            "grade": score_breakdown.grade
        }
        
        # Config đã sử dụng
        config_used = {
            "industry": industry,
            "thresholds": config_manager.get_thresholds(industry)
        }
        
        return {
            "score_breakdown": breakdown,
            "issues": issues_by_severity,
            "bonuses": bonuses,
            "stats": stats,
            "config_used": config_used,
            "success": True,
            "message": "Phân tích SEO thành công"
        }

    def analyze_seo_with_blocks(self, seo_article) -> Dict[str, Any]:
        """
        Phân tích SEO với SEOArticle có blocks
        
        Args:
            seo_article: SEOArticle object có blocks
            
        Returns:
            Kết quả phân tích với block issues
        """
        try:
            # Sử dụng UnifiedArticleParser
            from .parser.unified_parser import UnifiedArticleParser
            parser = UnifiedArticleParser(seo_article)
            
            # Load config
            config_manager = ConfigManager(str(self.config_dir))
            
            # Tạo BLOCK-BASED analyzer
            from .scoring.block_score_calculator import BlockSEOAnalyzer
            analyzer = BlockSEOAnalyzer(
                parser=parser,
                title=seo_article.title,
                meta_description=seo_article.meta_description,
                keywords=seo_article.keywords,
                config_manager=config_manager,
                industry=seo_article.industry if hasattr(seo_article, 'industry') else None
            )
            
            # Tính điểm với block issues
            score_breakdown = analyzer.calculate_total_score()
            
            # Format kết quả theo block format
            result = self._format_block_result(
                analyzer, parser, score_breakdown, config_manager
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Lỗi phân tích SEO với blocks: {str(e)}")
            raise
    
    def _format_block_result(self, analyzer, parser, score_breakdown, config_manager) -> Dict[str, Any]:
        """Format kết quả theo block-aware format"""
        # Phân loại issues theo severity và có block_id
        issues_by_severity = {
            "critical": [],
            "warning": [],
            "info": []
        }
        
        for issue in score_breakdown.issues:
            issue_dict = issue.to_dict()
            issues_by_severity[issue.severity.value].append(issue_dict)
        
        # Format bonuses
        bonuses = []
        for bonus_type, bonus_points in analyzer.bonuses:
            bonuses.append({
                "type": bonus_type,
                "points": bonus_points
            })
        
        # Lấy thống kê từ parser
        stats = {
            "word_count": analyzer.word_count,
            "title_length": len(analyzer.title),
            "meta_length": len(analyzer.meta),
            "parser_type": parser.get_parser_type(),
            "block_count": len(parser.article.blocks) if hasattr(parser.article, 'blocks') else 0
        }
        
        # Format score breakdown
        breakdown = {
            "structure": score_breakdown.structure_score,
            "keyword_optimization": score_breakdown.keyword_score,
            "readability": score_breakdown.readability_score,
            "technical_seo": score_breakdown.technical_score,
            "content_quality": score_breakdown.content_quality_score,
            "bonus": score_breakdown.bonus_points,
            "total": score_breakdown.total_score,
            "grade": score_breakdown.grade
        }
        
        return {
            "score_breakdown": breakdown,
            "issues": issues_by_severity,
            "bonuses": bonuses,
            "stats": stats,
            "success": True,
            "message": "Phân tích SEO với blocks thành công"
        }
    
    def save_result(self, result: Dict[str, Any], output_dir: str = None) -> str:
        """
        Lưu kết quả ra file JSON
        
        Args:
            result: Kết quả phân tích
            output_dir: Thư mục output (mặc định: results)
            
        Returns:
            Đường dẫn file đã lưu
        """
        if output_dir is None:
            base_dir = Path(__file__).parent.parent.parent.parent
            output_dir = base_dir / "results"
        
        # Tạo thư mục nếu chưa tồn tại
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Tạo tên file
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"seo_analysis_{timestamp}.json"
        filepath = output_path / filename
        
        # Lưu file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False, default=str)
        
        logger.info(f"Đã lưu kết quả vào: {filepath}")
        return str(filepath)