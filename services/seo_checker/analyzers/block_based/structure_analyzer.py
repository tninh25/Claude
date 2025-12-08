# services/seo_checker/analyzers/block_based/structure_analyzer.py
"""
BlockStructureAnalyzer - Phiên bản block-based của StructureAnalyzer
Mỗi issue phải có block_id cụ thể
"""
from typing import Tuple, List, Optional
import logging
from ...scoring.block_issues import BlockIssue, BlockIssueSeverity

logger = logging.getLogger(__name__)

class BlockStructureAnalyzer:
    """Phân tích cấu trúc bài viết - BLOCK-BASED VERSION"""
    
    def __init__(self, parser, config_manager):
        self.parser = parser
        self.config = config_manager
        self._is_block_based = parser.get_parser_type() == "block"
    
    def analyze(self) -> Tuple[float, List[BlockIssue]]:
        """Phân tích cấu trúc - trả về điểm và BLOCK ISSUES"""
        thresholds = self.config.get_thresholds()
        weights = self.config.get_scoring_weights()
        max_score = weights.get('structure', 20)
        score = max_score
        issues = []
        
        headings = self.parser.get_headings()
        
        # 1. Kiểm tra H1 - VÍ DỤ CỤ THỂ
        h1_blocks = headings.get('h1', [])
        
        if len(h1_blocks) == 0:
            # Tạo issue với block_id = None (không có block nào)
            penalty = self.config.get_penalty('missing_h1')
            score -= penalty
            issues.append(BlockIssue(
                type="missing_h1",
                block_id="",  # Không có block nào
                severity=BlockIssueSeverity.CRITICAL,
                penalty=penalty,
                detail="Bài viết thiếu thẻ H1 - Cực kỳ quan trọng cho SEO",
                recommendation="Thêm 1 thẻ H1 duy nhất chứa keyword chính"
            ))
        elif len(h1_blocks) > 1:
            # Tạo issue cho TẤT CẢ H1 thừa
            penalty = self.config.get_penalty('multiple_h1')
            score -= penalty
            
            # Mỗi H1 thừa là một issue riêng
            for block_id, h1_text in h1_blocks[1:]:  # Giữ lại H1 đầu tiên
                issues.append(BlockIssue(
                    type="multiple_h1",
                    block_id=block_id if block_id else f"h1-{h1_blocks.index((block_id, h1_text))}",
                    severity=BlockIssueSeverity.CRITICAL,
                    penalty=penalty // len(h1_blocks[1:]),  # Chia đều penalty
                    detail=f"Thẻ H1 thừa: '{h1_text[:50]}...'",
                    recommendation="Chuyển thẻ này thành H2 hoặc xóa bỏ"
                ))
        
        # 2. Kiểm tra H2 - VÍ DỤ CỤ THỂ VỚI BLOCK_ID
        h2_blocks = headings.get('h2', [])
        h2_min = thresholds.get('headings', {}).get('h2_min', 3)
        
        if len(h2_blocks) < h2_min:
            penalty = self.config.get_penalty('few_h2')
            score -= penalty
            
            # Tạo issue cho toàn bài (không có block cụ thể)
            issues.append(BlockIssue(
                type="few_h2",
                block_id="",  # Không có block cụ thể gây lỗi
                severity=BlockIssueSeverity.WARNING,
                penalty=penalty,
                detail=f"Chỉ có {len(h2_blocks)} thẻ H2, nên có ít nhất {h2_min}",
                recommendation=f"Thêm {h2_min - len(h2_blocks)} thẻ H2 để cấu trúc rõ ràng hơn"
            ))
        else:
            # Kiểm tra từng H2 có keyword không (sẽ có trong keyword analyzer)
            pass
        
        # 3. Kiểm tra H3 quá nhiều
        h3_blocks = headings.get('h3', [])
        h3_max = thresholds.get('headings', {}).get('h3_max', 15)
        
        if len(h3_blocks) > h3_max:
            # Chỉ cảnh báo cho các H3 thừa
            excess_h3 = len(h3_blocks) - h3_max
            for block_id, h3_text in h3_blocks[h3_max:]:
                issues.append(BlockIssue(
                    type="too_many_h3",
                    block_id=block_id if block_id else f"h3-{h3_blocks.index((block_id, h3_text))}",
                    severity=BlockIssueSeverity.INFO,
                    penalty=2 // excess_h3,  # Chia đều penalty
                    detail=f"Thẻ H3 thứ {h3_blocks.index((block_id, h3_text)) + 1}: '{h3_text[:50]}...'",
                    recommendation="Xem xét nhóm nội dung này vào một H2 hoặc giảm bớt"
                ))
            score -= 2
        
        return max(0, min(score, max_score)), issues