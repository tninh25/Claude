# services/seo_checker/auto_fix/seo_block_patch_service.py
"""
Service áp dụng patch vào bài viết
Chỉ sửa đúng block/field được chỉ định
"""

import logging
import copy
from typing import Dict, Any, List, Optional
from models.seo_checker.block_schemas import ArticleBlock
from models.llm.content_generation_schemas import SEOArticle
from models.seo_checker.fix_schemas import PatchOperation, FixScope

logger = logging.getLogger(__name__)

class SEOBlockPatchService:
    """Service áp dụng patch vào bài viết"""
    
    def apply_patches(self, 
                     article: SEOArticle, 
                     patches: List[PatchOperation]) -> SEOArticle:
        """
        Áp dụng danh sách patch vào bài viết
        
        Args:
            article: Bài viết gốc
            patches: Danh sách patch operations
            
        Returns:
            SEOArticle đã được sửa
        """
        # Tạo bản sao để không sửa bài viết gốc
        patched_article = copy.deepcopy(article)
        applied_count = 0
        
        # Áp dụng từng patch theo thứ tự
        for patch in patches:
            if patch.applied:
                logger.info(f"Patch {patch.operation_id} already applied, skipping")
                continue
            
            try:
                if patch.scope == FixScope.BLOCK and patch.block_patch:
                    success = self._apply_block_patch(patched_article, patch)
                elif patch.scope == FixScope.META and patch.meta_patch:
                    success = self._apply_meta_patch(patched_article, patch)
                elif patch.scope == FixScope.STRUCTURAL and patch.structural_patch:
                    success = self._apply_structural_patch(patched_article, patch)
                else:
                    logger.warning(f"Invalid patch {patch.operation_id}: no valid patch data")
                    success = False
                
                if success:
                    patch.applied = True
                    applied_count += 1
                    logger.info(f"Applied patch {patch.operation_id}: {patch.description}")
                else:
                    logger.warning(f"Failed to apply patch {patch.operation_id}")
                    
            except Exception as e:
                logger.error(f"Error applying patch {patch.operation_id}: {e}")
        
        logger.info(f"Applied {applied_count}/{len(patches)} patches successfully")
        return patched_article
    
    def _apply_block_patch(self, article: SEOArticle, patch: PatchOperation) -> bool:
        """Áp dụng patch cho block"""
        block_patch = patch.block_patch
        block_id = block_patch.get('block_id')
        new_text = block_patch.get('new_text')
        
        if not block_id or not new_text:
            logger.error(f"Invalid block patch: missing block_id or new_text")
            return False
        
        # Tìm block cần sửa
        if not article.blocks:
            logger.error(f"Article has no blocks")
            return False
        
        block_found = False
        for block in article.blocks:
            if block.id == block_id:
                # Lưu text cũ (cho rollback)
                if 'old_text' not in block_patch:
                    block_patch['old_text'] = block.text
                
                # Cập nhật text
                block.text = new_text
                
                # Cập nhật word_count
                block.word_count = len(new_text.split())
                
                block_found = True
                logger.debug(f"Updated block {block_id}: {block.text[:50]}...")
                break
        
        if not block_found:
            logger.error(f"Block {block_id} not found in article")
            return False
        
        return True
    
    def _apply_meta_patch(self, article: SEOArticle, patch: PatchOperation) -> bool:
        """Áp dụng patch cho meta field"""
        meta_patch = patch.meta_patch
        field = meta_patch.get('field')
        new_value = meta_patch.get('new_value')
        
        if not field or not new_value:
            logger.error(f"Invalid meta patch: missing field or new_value")
            return False
        
        # Lưu giá trị cũ
        if 'old_value' not in meta_patch:
            if field == 'title':
                meta_patch['old_value'] = article.title
            elif field == 'meta_description':
                meta_patch['old_value'] = article.meta_description
        
        # Cập nhật giá trị mới
        if field == 'title':
            article.title = new_value
        elif field == 'meta_description':
            article.meta_description = new_value
        else:
            logger.error(f"Unknown meta field: {field}")
            return False
        
        logger.debug(f"Updated {field}: {new_value[:50]}...")
        return True
    
    def _apply_structural_patch(self, article: SEOArticle, patch: PatchOperation) -> bool:
        """Áp dụng patch cấu trúc (thêm block mới)"""
        structural_patch = patch.structural_patch
        element_type = structural_patch.get('element_type')
        new_text = structural_patch.get('new_text')
        position_hint = structural_patch.get('position_hint', 'end')
        
        if not element_type or not new_text:
            logger.error(f"Invalid structural patch: missing element_type or new_text")
            return False
        
        # Tạo block mới
        new_block = self._create_new_block(element_type, new_text, article.blocks)
        
        if not new_block:
            logger.error(f"Failed to create new block for {element_type}")
            return False
        
        # Xác định vị trí chèn
        insert_index = self._get_insert_index(position_hint, element_type, article.blocks)
        
        # Chèn block vào vị trí phù hợp
        if article.blocks is None:
            article.blocks = []
        
        article.blocks.insert(insert_index, new_block)
        
        # Lưu thông tin patch
        structural_patch['added_block_id'] = new_block.id
        structural_patch['insert_index'] = insert_index
        
        logger.info(f"Added new {element_type} block at position {insert_index}")
        return True
    
    def _create_new_block(self, element_type: str, text: str, 
                         existing_blocks: List[ArticleBlock]) -> Optional[ArticleBlock]:
        """Tạo block mới với ID duy nhất"""
        if not existing_blocks:
            existing_blocks = []
        
        # Tạo ID duy nhất
        existing_ids = {block.id for block in existing_blocks}
        
        # Đếm số block hiện có của loại này
        count = sum(1 for block in existing_blocks if block.tag == element_type)
        new_id = f"{element_type}-{count + 1}"
        
        # Đảm bảo ID không trùng
        attempt = 1
        while new_id in existing_ids:
            new_id = f"{element_type}-{count + 1}-{attempt}"
            attempt += 1
        
        # Tạo block
        return ArticleBlock(
            id=new_id,
            tag=element_type,
            text=text,
            word_count=len(text.split())
        )
    
    def _get_insert_index(self, position_hint: str, element_type: str, 
                         blocks: List[ArticleBlock]) -> int:
        """Xác định vị trí chèn block mới"""
        if not blocks:
            return 0
        
        if position_hint == 'beginning':
            return 0
        
        elif position_hint == 'end':
            return len(blocks)
        
        elif position_hint == 'after_last_h2':
            # Tìm H2 cuối cùng
            last_h2_index = -1
            for i, block in enumerate(blocks):
                if block.tag == 'h2':
                    last_h2_index = i
            
            if last_h2_index >= 0:
                return last_h2_index + 1
            else:
                # Nếu không có H2, chèn sau H1 đầu tiên
                for i, block in enumerate(blocks):
                    if block.tag == 'h1':
                        return i + 1
                return len(blocks)
        
        elif position_hint == 'near_related_content':
            # Chèn ở 2/3 bài viết
            return len(blocks) * 2 // 3
        
        # Mặc định: chèn ở cuối
        return len(blocks)
    
    def get_patch_summary(self, patches: List[PatchOperation]) -> Dict[str, Any]:
        """Tạo summary các patch đã áp dụng"""
        applied = [p for p in patches if p.applied]
        skipped = [p for p in patches if not p.applied]
        
        summary = {
            "total_patches": len(patches),
            "applied": len(applied),
            "skipped": len(skipped),
            "by_scope": {
                "block": len([p for p in applied if p.scope == FixScope.BLOCK]),
                "meta": len([p for p in applied if p.scope == FixScope.META]),
                "structural": len([p for p in applied if p.scope == FixScope.STRUCTURAL])
            },
            "applied_operations": [
                {
                    "operation_id": p.operation_id,
                    "task_id": p.task_id,
                    "scope": p.scope.value,
                    "description": p.description
                }
                for p in applied
            ]
        }
        
        return summary