# services/seo_checker/parser/unified_parser.py
"""
UnifiedArticleParser - Lớp trung gian tự chọn parser phù hợp
"""
from typing import Dict, List, Tuple, Optional, Any, Union
import logging
from models.llm.content_generation_schemas import SEOArticle

# Import các parser
from .block_parser import BlockArticleParser
from .html_parser import EnhancedArticleParser  # Giữ nguyên HTML parser

logger = logging.getLogger(__name__)

class UnifiedArticleParser:
    """
    Parser thống nhất - TỰ CHỌN parser dựa trên dữ liệu đầu vào
    
    Ưu tiên: blocks > html
    """
    
    def __init__(self, article: SEOArticle):
        """
        Khởi tạo với SEOArticle
        
        Args:
            article: SEOArticle có thể chứa blocks hoặc html
        """
        self.article = article
        self._parser = None
        self._parser_type = None
        
        self._initialize_parser()
    
    def _initialize_parser(self):
        """Khởi tạo parser phù hợp"""
        # ƯU TIÊN 1: Dùng BlockArticleParser nếu có blocks
        if self.article.blocks:
            try:
                self._parser = BlockArticleParser(self.article.blocks)
                self._parser_type = "block"
                logger.info(f"Using BlockArticleParser with {len(self.article.blocks)} blocks")
            except Exception as e:
                logger.error(f"Failed to initialize BlockArticleParser: {e}")
                self._fallback_to_html()
        
        # ƯU TIÊN 2: Fallback về HTML nếu không có blocks
        elif self.article.html_content:
            self._parser = EnhancedArticleParser(self.article.html_content)
            self._parser_type = "html"
            logger.info("Using EnhancedArticleParser (HTML fallback)")
        
        else:
            raise ValueError("Article must have either blocks or html_content")
    
    def _fallback_to_html(self):
        """Fallback về HTML parser"""
        if self.article.html_content:
            self._parser = EnhancedArticleParser(self.article.html_content)
            self._parser_type = "html"
            logger.warning("Falling back to HTML parser")
        else:
            raise ValueError("No blocks and no html_content available")
    
    def get_parser_type(self) -> str:
        """Lấy loại parser đang dùng"""
        return self._parser_type
    
    # Các method delegate - interface giống nhau cho cả 2 parser
    
    def get_clean_text(self) -> str:
        """Lấy văn bản sạch"""
        return self._parser.get_clean_text()
    
    def get_first_paragraph(self) -> Tuple[Optional[str], str]:
        """
        Lấy đoạn văn đầu tiên
        
        Returns:
            Tuple[block_id, text] cho block parser
            Tuple[None, text] cho HTML parser (để tương thích)
        """
        if self._parser_type == "block":
            return self._parser.get_first_paragraph()
        else:
            # HTML parser không có block_id
            return (None, self._parser.get_first_paragraph())
    
    def get_headings(self) -> Dict[str, List[Tuple[str, str]]]:
        """
        Lấy headings
        
        Returns:
            Dict với value là List[Tuple[block_id, text]]
            Với HTML parser, block_id sẽ là None
        """
        if self._parser_type == "block":
            return self._parser.get_headings()
        else:
            # Convert HTML headings format sang block format
            html_headings = self._parser.get_headings()
            result = {}
            for tag, texts in html_headings.items():
                result[tag] = [(None, text) for text in texts]  # block_id = None
            return result
    
    def get_paragraphs_stats(self) -> List[Dict[str, Any]]:
        """
        Lấy thống kê paragraphs
        
        Returns:
            List[Dict] với block_id cho block parser
            List[Dict] không có block_id cho HTML parser
        """
        if self._parser_type == "block":
            return self._parser.get_paragraphs_stats()
        else:
            # HTML parser không có block_id
            stats = []
            html_stats = self._parser.get_paragraphs_stats()
            for stat in html_stats:
                stat.pop('block_id', None)  # Đảm bảo không có block_id
                stats.append(stat)
            return stats
    
    # Các method chỉ có trong BlockParser
    def get_blocks_by_tag(self, tag: str) -> List[Any]:
        """Chỉ khả dụng với BlockParser"""
        if self._parser_type == "block" and hasattr(self._parser, 'get_blocks_by_tag'):
            return self._parser.get_blocks_by_tag(tag)
        return []
    
    def get_block_by_id(self, block_id: str) -> Optional[Any]:
        """Chỉ khả dụng với BlockParser"""
        if self._parser_type == "block" and hasattr(self._parser, 'get_block_by_id'):
            return self._parser.get_block_by_id(block_id)
        return None
    
    def find_keyword_in_blocks(self, keyword: str) -> List[Tuple[str, str]]:
        """Tìm keyword trong blocks"""
        if self._parser_type == "block":
            return self._parser.find_keyword_in_blocks(keyword)
        else:
            # Fallback cho HTML parser
            text = self.get_clean_text().lower()
            keyword_lower = keyword.lower()
            if keyword_lower in text:
                return [(None, f"Keyword found in HTML content")]
            return []
    
    def get_total_word_count(self) -> int:
        """Lấy tổng số từ"""
        if self._parser_type == "block":
            return self._parser.get_total_word_count()
        else:
            # HTML parser tính từ clean_text
            return len(self.get_clean_text().split())
    
    # Các method của HTMLParser (giữ tương thích)
    def get_images(self) -> List[Dict[str, str]]:
        """Lấy thông tin images (chỉ HTML parser)"""
        if hasattr(self._parser, 'get_images'):
            return self._parser.get_images()
        return []
    
    def get_links(self) -> Dict[str, List[str]]:
        """Lấy links (chỉ HTML parser)"""
        if hasattr(self._parser, 'get_links'):
            return self._parser.get_links()
        return {'internal': [], 'external': []}