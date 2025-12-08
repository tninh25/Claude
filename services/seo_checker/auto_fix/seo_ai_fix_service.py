# services/seo_checker/auto_fix/seo_ai_fix_service.py
"""
Service gọi AI để sửa từng FixTask - SỬA ĐỂ DÙNG UniPipcAIClient
"""

import json
import logging
from typing import Dict, Any, Optional
from models.seo_checker.fix_schemas import FixTask, FixScope, PatchOperation
from core.ai_prompt.seo_fix_prompts import SEOFixPrompts

logger = logging.getLogger(__name__)

class SEOAIFixService:
    """Service xử lý AI fix cho từng task - UPDATED FOR UniPipcAIClient"""
    
    def __init__(self, ai_client):
        """
        Khởi tạo với AI client
        
        Args:
            ai_client: UniPipcAIClient (đã có sẵn trong dự án)
        """
        self.ai_client = ai_client
    
    async def process_task(self, task: FixTask, article: Dict[str, Any]) -> Optional[PatchOperation]:
        """
        Xử lý 1 FixTask bằng AI - UPDATED
        """
        try:
            logger.info(f"Processing task {task.task_id}: {task.type}")
            
            # Phân loại theo scope
            if task.target.scope == FixScope.BLOCK:
                return await self._process_block_task(task, article)
            
            elif task.target.scope == FixScope.META:
                return await self._process_meta_task(task, article)
            
            elif task.target.scope == FixScope.STRUCTURAL:
                return await self._process_structural_task(task, article)
            
            else:
                logger.warning(f"Unknown scope for task {task.task_id}: {task.target.scope}")
                return None
                
        except Exception as e:
            logger.error(f"Error processing task {task.task_id}: {e}")
            return None
    
    # SỬA PHƯƠNG THỨC _call_ai ĐỂ DÙNG UniPipcAIClient
    async def _call_ai(self, prompt: str) -> Optional[str]:
        """
        Gọi UniPipcAIClient để xử lý prompt - UPDATED
        
        Args:
            prompt: Prompt text
            
        Returns:
            AI response (string JSON) hoặc None nếu thất bại
        """
        try:
            # SỬA: Sử dụng UniPipcAIClient thay vì OpenAI
            # Tách system prompt và user prompt
            lines = prompt.strip().split('\n')
            
            # System prompt thường là phần đầu (có ## NHIỆM VỤ:)
            system_prompt_lines = []
            question_lines = []
            in_question = False
            
            for line in lines:
                if "## OUTPUT FORMAT" in line:
                    in_question = True
                if in_question:
                    question_lines.append(line)
                else:
                    system_prompt_lines.append(line)
            
            system_prompt = '\n'.join(system_prompt_lines)
            question_input = '\n'.join(question_lines)
            print("TÔI CẦN COI PROMPT:", system_prompt)
            # print("TÔI CẦN COI QUESTION INPUT:", question_input)

            # Gọi client theo cách của bạn
            ai_response = self.ai_client.ask_question_with_prompt(
                prompt=system_prompt,
                question=question_input
            )
            
            if not ai_response:
                logger.error("AI response is empty")
                return None
            
            # Parse response theo format của UniPipcAIClient
            data = ai_response.get("data", {})
            content = data.get("answer", "") or data.get("QAMsg", "")
            
            if not content:
                logger.error("No content in AI response")
                return None
            
            # Xử lý JSON wrapper (```json và ```)
            content = content.strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()
            
            logger.debug(f"AI response cleaned: {content[:100]}...")
            return content
            
        except Exception as e:
            logger.error(f"AI call failed: {e}")
            return None
    
    async def _process_block_task(self, task: FixTask, article: Dict[str, Any]) -> Optional[PatchOperation]:
        """Xử lý task sửa block"""
        # Lấy thông tin block
        block_id = task.target.block_id
        if not block_id:
            logger.warning(f"Task {task.task_id} has no block_id")
            return None
        
        block_info = self._get_block_info(block_id, article)
        if not block_info:
            logger.warning(f"Block {block_id} not found in article")
            return None
        
        # Chọn prompt phù hợp
        if 'keyword_stuffing' in task.type:
            prompt = SEOFixPrompts.get_keyword_reduction_prompt(
                block_id=block_id,
                current_text=block_info['text'],
                keyword=task.payload.get('keyword', ''),
                recommendation=task.recommendation
            )
        else:
            prompt = SEOFixPrompts.get_block_fix_prompt(
                block_id=block_id,
                tag=block_info['tag'],
                keyword=task.payload.get('keyword', ''),
                current_text=block_info['text'],
                recommendation=task.recommendation
            )
        
        # Gọi AI
        response = await self._call_ai(prompt)
        if not response:
            return None
        
        # Parse response
        try:
            result = json.loads(response)
            
            # Validate response
            if 'block_id' not in result or 'new_text' not in result:
                logger.error(f"Invalid AI response for task {task.task_id}: {response}")
                return None
            
            # Tạo patch operation
            return PatchOperation(
                operation_id=f"op-{task.task_id}",
                task_id=task.task_id,
                scope=FixScope.BLOCK,
                block_patch={
                    "block_id": result['block_id'],
                    "old_text": block_info['text'],
                    "new_text": result['new_text'],
                    "tag": block_info['tag']
                },
                description=f"Sửa block {block_id}: {task.type}",
                applied=False
            )
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI response for task {task.task_id}: {e}")
            logger.error(f"Response: {response}")
            return None
    
    async def _process_meta_task(self, task: FixTask, article: Dict[str, Any]) -> Optional[PatchOperation]:
        """Xử lý task sửa meta field"""
        field_name = task.target.field_name
        if not field_name:
            logger.warning(f"Task {task.task_id} has no field_name")
            return None
        
        # Lấy current value
        current_value = ""
        if field_name == "title":
            current_value = article.get('title', '')
        elif field_name == "meta_description":
            current_value = article.get('meta_description', '')
        
        # Tạo prompt
        prompt = SEOFixPrompts.get_meta_fix_prompt(
            field_name=field_name,
            current_value=current_value,
            recommendation=task.recommendation,
            article_keywords=article.get('keywords', [])
        )
        
        # Gọi AI
        response = await self._call_ai(prompt)
        if not response:
            return None
        
        # Parse response
        try:
            result = json.loads(response)
            
            if 'field' not in result or 'new_value' not in result:
                logger.error(f"Invalid AI response for meta task {task.task_id}: {response}")
                return None
            
            # Tạo patch
            return PatchOperation(
                operation_id=f"op-{task.task_id}",
                task_id=task.task_id,
                scope=FixScope.META,
                meta_patch={
                    "field": result['field'],
                    "old_value": current_value,
                    "new_value": result['new_value']
                },
                description=f"Sửa {field_name}: {task.type}",
                applied=False
            )
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI response for meta task {task.task_id}: {e}")
            return None
    
    async def _process_structural_task(self, task: FixTask, article: Dict[str, Any]) -> Optional[PatchOperation]:
        """Xử lý task sửa cấu trúc"""
        # Tạo prompt
        prompt = SEOFixPrompts.get_structural_fix_prompt(
            issue_type=task.type,
            recommendation=task.recommendation,
            article_title=article.get('title', ''),
            article_keywords=article.get('keywords', [])
        )
        
        # Gọi AI
        response = await self._call_ai(prompt)
        if not response:
            return None
        
        # Parse response
        try:
            result = json.loads(response)
            
            if 'element_type' not in result or 'new_text' not in result:
                logger.error(f"Invalid AI response for structural task {task.task_id}: {response}")
                return None
            
            # Tạo patch
            return PatchOperation(
                operation_id=f"op-{task.task_id}",
                task_id=task.task_id,
                scope=FixScope.STRUCTURAL,
                structural_patch={
                    "element_type": result['element_type'],
                    "new_text": result['new_text'],
                    "position_hint": self._get_position_hint(task.type)
                },
                description=f"Thêm {task.type.replace('_', ' ')}",
                applied=False
            )
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI response for structural task {task.task_id}: {e}")
            return None
    
    def _get_block_info(self, block_id: str, article: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Lấy thông tin block từ article"""
        if 'blocks' not in article or not article['blocks']:
            return None
        
        for block in article['blocks']:
            if block.get('id') == block_id:
                return {
                    'id': block['id'],
                    'tag': block.get('tag', 'p'),
                    'text': block.get('text', '')
                }
        
        return None
    
    def _get_position_hint(self, issue_type: str) -> str:
        """Xác định vị trí thêm block mới"""
        if issue_type == 'missing_h1':
            return 'beginning'
        elif issue_type == 'few_h2':
            return 'after_last_h2'
        elif issue_type == 'no_internal_links':
            return 'near_related_content'
        else:
            return 'end'
    
    
