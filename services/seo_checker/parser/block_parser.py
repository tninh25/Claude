# services/seo_checker/parser/block_parser.py
"""
BlockArticleParser - Parser chính cho block-based analysis
"""
from typing import Dict, List, Tuple, Optional, Any
import logging
from models.seo_checker.block_schemas import ArticleBlock

logger = logging.getLogger(__name__)

class BlockArticleParser:
    """Parser block-first - BLOCK LÀ NGUỒN DỮ LIỆU GỐC"""
    
    def __init__(self, blocks: List[ArticleBlock]):
        """
        Khởi tạo với danh sách blocks
        
        Args:
            blocks: Danh sách ArticleBlock
        """
        if not blocks:
            raise ValueError("Danh sách blocks không được rỗng")
        
        self.blocks = blocks
        self._validate_blocks()
        self._cached_data = {}
    
    def _validate_blocks(self):
        """Validate block structure"""
        seen_ids = set()
        for block in self.blocks:
            if block.id in seen_ids:
                logger.warning(f"Duplicate block_id: {block.id}")
            seen_ids.add(block.id)
            
            # Tính word_count nếu chưa có
            if block.word_count is None:
                block.word_count = len(block.text.split())
    
    def get_clean_text(self) -> str:
        """Lấy toàn bộ văn bản từ blocks"""
        if 'clean_text' not in self._cached_data:
            text_parts = []
            for block in self.blocks:
                if block.tag in ['p', 'li']:  # Chỉ lấy nội dung từ paragraph và list
                    text_parts.append(block.text)
            self._cached_data['clean_text'] = ' '.join(text_parts)
        
        return self._cached_data['clean_text']
    
    def get_first_paragraph(self) -> Tuple[Optional[str], str]:
        """
        Lấy đoạn văn đầu tiên có nội dung thực sự
        
        Returns:
            Tuple[block_id, text]: ID và nội dung của đoạn đầu
        """
        if 'first_para' not in self._cached_data:
            for block in self.blocks:
                if block.tag == 'p' and block.word_count and block.word_count > 10:
                    self._cached_data['first_para'] = (block.id, block.text)
                    break
            else:
                self._cached_data['first_para'] = (None, "")
        
        return self._cached_data['first_para']
    
    def get_headings(self) -> Dict[str, List[Tuple[str, str]]]:
        """
        Lấy tất cả headings theo loại
        
        Returns:
            Dict với key là tag (h1, h2, h3) và value là list of (block_id, text)
        """
        if 'headings' not in self._cached_data:
            headings = {
                'h1': [],
                'h2': [],
                'h3': [],
                'h4': []
            }
            
            for block in self.blocks:
                if block.tag in headings:
                    headings[block.tag].append((block.id, block.text))
            
            self._cached_data['headings'] = headings
        
        return self._cached_data['headings']
    
    def get_paragraphs_stats(self) -> List[Dict[str, Any]]:
        """
        Thống kê các đoạn văn với block_id
        
        Returns:
            List[Dict] với đầy đủ thông tin kèm block_id
        """
        if 'para_stats' not in self._cached_data:
            stats = []
            for block in self.blocks:
                if block.tag == 'p':
                    stats.append({
                        'block_id': block.id,
                        'index': len(stats) + 1,
                        'word_count': block.word_count or len(block.text.split()),
                        'char_count': len(block.text),
                        'text_preview': block.text[:100] + '...' if len(block.text) > 100 else block.text
                    })
            self._cached_data['para_stats'] = stats
        
        return self._cached_data['para_stats']
    
    def get_blocks_by_tag(self, tag: str) -> List[ArticleBlock]:
        """Lấy tất cả blocks theo tag"""
        return [block for block in self.blocks if block.tag == tag]
    
    def get_block_by_id(self, block_id: str) -> Optional[ArticleBlock]:
        """Lấy block theo ID"""
        for block in self.blocks:
            if block.id == block_id:
                return block
        return None
    
    def get_total_word_count(self) -> int:
        """Tính tổng số từ từ tất cả blocks"""
        return sum(block.word_count or 0 for block in self.blocks if block.word_count is not None)
    
    def find_keyword_in_blocks(self, keyword: str) -> List[Tuple[str, str]]:
        """
        Tìm keyword trong tất cả blocks
        
        Returns:
            List[Tuple[block_id, text]] chứa keyword
        """
        keyword_lower = keyword.lower()
        results = []
        
        for block in self.blocks:
            if keyword_lower in block.text.lower():
                results.append((block.id, block.text))
        
        return results