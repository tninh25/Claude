# services/seo_checker/analyzers/block_based/keyword_analyzer.py
"""
BlockKeywordAnalyzer - Phiên bản block-based của KeywordAnalyzer
Mỗi issue gắn với block cụ thể không có keyword
"""
from typing import Tuple, List, Dict, Optional
import logging
from ...scoring.block_issues import BlockIssue, BlockIssueSeverity

logger = logging.getLogger(__name__)

class BlockKeywordAnalyzer:
    """Phân tích keyword optimization - BLOCK-BASED VERSION"""
    
    def __init__(self, parser, config_manager, title: str, meta_description: str, 
                 keywords: List[str], clean_text: str, word_count: int):
        self.parser = parser
        self.config = config_manager
        self.title = title
        self.meta = meta_description
        self.keywords = keywords
        self.clean_text = clean_text
        self.word_count = word_count
        self._is_block_based = parser.get_parser_type() == "block"
    
    def analyze(self) -> Tuple[float, List[BlockIssue]]:
        """Phân tích keyword - MỖI ISSUE CÓ BLOCK_ID CỤ THỂ"""
        thresholds = self.config.get_thresholds()
        weights = self.config.get_scoring_weights()
        max_score = weights.get('keyword_optimization', 25)
        score = max_score
        issues = []
        
        # Chuẩn hóa text
        text_lower = self.clean_text.lower()
        title_lower = self.title.lower()
        meta_lower = self.meta.lower()
        
        # Lấy first paragraph với block_id
        first_para_block_id, first_para_text = self.parser.get_first_paragraph()
        first_para_lower = first_para_text.lower()
        
        # Lấy headings với block_id
        headings = self.parser.get_headings()
        h1_blocks = headings.get('h1', [])
        h2_blocks = headings.get('h2', [])
        
        # Lấy tất cả blocks nếu là block-based
        if self._is_block_based:
            # Tìm tất cả paragraph blocks
            para_stats = self.parser.get_paragraphs_stats()
        else:
            para_stats = []
        
        for keyword in self.keywords:
            kw_lower = keyword.lower()
            
            # 1. Kiểm tra keyword trong TITLE
            if kw_lower not in title_lower:
                issues.append(BlockIssue(
                    type="keyword_not_in_title",
                    block_id="title",  # Special block_id cho title
                    severity=BlockIssueSeverity.WARNING,
                    penalty=5,
                    detail=f"Keyword '{keyword}' không có trong tiêu đề bài viết",
                    recommendation=f"Thêm keyword '{keyword}' vào tiêu đề, ưu tiên đứng đầu"
                ))
                score -= 5
            
            # 2. Kiểm tra keyword trong META DESCRIPTION
            if kw_lower not in meta_lower:
                issues.append(BlockIssue(
                    type="keyword_not_in_meta",
                    block_id="meta",  # Special block_id cho meta
                    severity=BlockIssueSeverity.WARNING,
                    penalty=3,
                    detail=f"Keyword '{keyword}' không có trong meta description",
                    recommendation=f"Thêm keyword '{keyword}' vào meta description"
                ))
                score -= 3
            
            # 3. Kiểm tra keyword trong ĐOẠN ĐẦU - VÍ DỤ CỤ THỂ VỚI BLOCK_ID
            if first_para_block_id and kw_lower not in first_para_lower:
                issues.append(BlockIssue(
                    type="keyword_not_in_first_paragraph",
                    block_id=first_para_block_id,  # BLOCK_ID CỤ THỂ
                    severity=BlockIssueSeverity.INFO,
                    penalty=2,
                    detail=f"Keyword '{keyword}' không xuất hiện trong đoạn văn đầu tiên",
                    recommendation=f"Chèn keyword '{keyword}' vào đoạn mở đầu này"
                ))
                score -= 2
            
            # 4. Kiểm tra keyword trong H1 - VÍ DỤ CỤ THỂ
            if h1_blocks:
                h1_block_id, h1_text = h1_blocks[0]  # Lấy H1 đầu tiên
                if kw_lower not in h1_text.lower():
                    issues.append(BlockIssue(
                        type="keyword_not_in_h1",
                        block_id=h1_block_id if h1_block_id else "h1-1",
                        severity=BlockIssueSeverity.WARNING,
                        penalty=3,
                        detail=f"Keyword '{keyword}' không có trong thẻ H1 chính",
                        recommendation=f"Thêm keyword '{keyword}' vào thẻ H1 này"
                    ))
                    score -= 3
            
            # 5. Kiểm tra keyword trong ít nhất 1 H2
            keyword_in_h2 = False
            for h2_block_id, h2_text in h2_blocks:
                if kw_lower in h2_text.lower():
                    keyword_in_h2 = True
                    break
            
            if not keyword_in_h2 and h2_blocks:
                # Chọn H2 đầu tiên để đề xuất sửa
                h2_block_id, h2_text = h2_blocks[0]
                issues.append(BlockIssue(
                    type="keyword_not_in_h2",
                    block_id=h2_block_id if h2_block_id else "h2-1",
                    severity=BlockIssueSeverity.INFO,
                    penalty=1,
                    detail=f"Keyword '{keyword}' không xuất hiện trong bất kỳ thẻ H2 nào",
                    recommendation=f"Thêm keyword '{keyword}' vào thẻ H2 này hoặc một H2 khác"
                ))
                score -= 1
            
            # 6. Kiểm tra keyword density trên toàn bài (logic cũ giữ nguyên)
            count = text_lower.count(kw_lower)
            density = (count / max(1, self.word_count)) * 100
            
            stuffing_threshold = thresholds.get('keyword_density', {}).get('stuffing_threshold', 4.0)
            if density > stuffing_threshold:
                # Tìm các paragraph có nhiều keyword nhất để chỉ ra cụ thể
                if para_stats:
                    # Tìm paragraph có density cao nhất
                    max_density_para = None
                    max_density = 0
                    
                    for para in para_stats:
                        if 'block_id' in para:
                            para_text = self.parser.get_block_by_id(para['block_id'])
                            if para_text:
                                para_count = para_text.text.lower().count(kw_lower)
                                para_density = (para_count / max(1, para['word_count'])) * 100
                                if para_density > max_density:
                                    max_density = para_density
                                    max_density_para = para
                    
                    if max_density_para:
                        block_id = max_density_para.get('block_id', 'unknown')
                        penalty = self.config.get_penalty('keyword_stuffing')
                        score -= penalty
                        issues.append(BlockIssue(
                            type="keyword_stuffing",
                            block_id=block_id,
                            severity=BlockIssueSeverity.CRITICAL,
                            penalty=penalty,
                            detail=f"Keyword '{keyword}' xuất hiện quá nhiều trong đoạn này ({max_density:.1f}%)",
                            recommendation=f"Giảm số lần xuất hiện keyword '{keyword}' trong đoạn này"
                        ))
        
        return max(0, min(score, max_score)), issues