# services/seo_checker/analyzers/block_based/readability_analyzer.py
"""
BlockReadabilityAnalyzer - Phiên bản block-based của ReadabilityAnalyzer
Mỗi issue về độ dài đoạn văn phải có block_id cụ thể
"""
from typing import Tuple, List, Dict, Any
import logging
import re
from ...scoring.block_issues import BlockIssue, BlockIssueSeverity

logger = logging.getLogger(__name__)

class BlockReadabilityAnalyzer:
    """Phân tích khả năng đọc - BLOCK-BASED VERSION"""
    
    def __init__(self, parser, config_manager, clean_text: str):
        self.parser = parser
        self.config = config_manager
        self.clean_text = clean_text
        self._is_block_based = parser.get_parser_type() == "block"
    
    def analyze(self) -> Tuple[float, List[BlockIssue]]:
        """Phân tích readability - CHỈ RA BLOCK CỤ THỂ QUÁ DÀI"""
        thresholds = self.config.get_thresholds()
        weights = self.config.get_scoring_weights()
        max_score = weights.get('readability', 20)
        score = max_score
        issues = []
        
        # VÍ DỤ CỤ THỂ 1: Kiểm tra độ dài đoạn văn với BLOCK_ID
        para_stats = self.parser.get_paragraphs_stats()
        max_para_words = thresholds.get('paragraph', {}).get('max_words', 150)
        
        # Tìm các paragraph quá dài
        long_paragraphs = [p for p in para_stats if p['word_count'] > max_para_words]
        
        for para in long_paragraphs[:3]:  # Chỉ báo 3 đoạn đầu tiên
            # Lấy block_id từ thống kê (nếu có)
            block_id = para.get('block_id')
            if not block_id and self._is_block_based:
                block_id = f"p-{para['index']}"  # Fallback ID
            
            if block_id:  # Chỉ tạo issue nếu có block_id
                penalty = self.config.get_penalty('paragraph_too_long')
                score -= penalty
                
                issues.append(BlockIssue(
                    type="paragraph_too_long",
                    block_id=block_id,
                    severity=BlockIssueSeverity.WARNING,
                    penalty=penalty,
                    detail=f"Đoạn văn có {para['word_count']} từ (vượt quá {max_para_words} từ)",
                    recommendation=f"Chia nhỏ đoạn văn này thành 2-3 đoạn ngắn hơn, mỗi đoạn tối đa {max_para_words} từ"
                ))
        
        # VÍ DỤ CỤ THỂ 2: Kiểm tra độ dài câu trong các paragraph
        if self._is_block_based:
            # Lấy tất cả paragraph blocks
            para_blocks = self.parser.get_blocks_by_tag('p')
            max_sentence_words = thresholds.get('sentence', {}).get('max_words', 25)
            
            for block in para_blocks:
                # Phân tích câu trong block này
                sentences = re.split(r'[.!?]+', block.text)
                long_sentences = [
                    s for s in sentences 
                    if len(s.strip().split()) > max_sentence_words
                ]
                
                if len(long_sentences) > 2:  # Nhiều hơn 2 câu dài trong cùng block
                    issues.append(BlockIssue(
                        type="many_long_sentences_in_paragraph",
                        block_id=block.id,
                        severity=BlockIssueSeverity.WARNING,
                        penalty=2,
                        detail=f"Đoạn này có {len(long_sentences)} câu dài hơn {max_sentence_words} từ",
                        recommendation=f"Viết câu ngắn hơn trong đoạn này, mỗi câu tối đa {max_sentence_words} từ"
                    ))
                    score -= 2
        
        return max(0, min(score, max_score)), issues