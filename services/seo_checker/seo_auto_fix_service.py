# services/seo_checker/seo_auto_fix_service.py
"""
Service chính điều phối toàn bộ pipeline auto-fix - UPDATED
"""

import logging
from typing import Dict, Any, Optional, List
from models.llm.content_generation_schemas import SEOArticle
from models.seo_checker.fix_schemas import FixTask, AutoFixResponse

# SỬA: Import từ đúng vị trí
from .auto_fix.seo_fix_task_builder import FixTaskBuilder
from .auto_fix.seo_ai_fix_service import SEOAIFixService
from .auto_fix.seo_block_patch_service import SEOBlockPatchService
from .seo_service import SEOCheckerService

logger = logging.getLogger(__name__)

class SEOAutoFixService:
    """Service auto-fix SEO chính - UPDATED"""
    
    def __init__(self, config_dir: str = None):
        """
        Khởi tạo service - UPDATED để tự tạo ai_client
        
        Args:
            config_dir: Thư mục config cho SEO checker
        """
        self.config_dir = config_dir
        
        # SỬA: Tạo UniPipcAIClient từ clients của bạn
        try:
            from clients.ai_client import UniPipcAIClient
            ai_client = UniPipcAIClient()
            logger.info("✓ Initialized UniPipcAIClient for SEO auto-fix")
        except ImportError as e:
            logger.error(f"Failed to import UniPipcAIClient: {e}")
            # Fallback: tạo mock client cho development
            ai_client = self._create_mock_client()
        
        # Khởi tạo các service con với ai_client
        self.task_builder = FixTaskBuilder()
        self.ai_fix_service = SEOAIFixService(ai_client)  # Truyền ai_client vào
        self.patch_service = SEOBlockPatchService()
        self.seo_checker = SEOCheckerService(config_dir)
        
        # Cấu hình
        self.min_score_threshold = 70
        self.max_iterations = 3
    
    async def auto_fix_seo(self, 
                          article: SEOArticle, 
                          score_result: Dict[str, Any]) -> AutoFixResponse:
        """
        Tự động sửa SEO cho bài viết
        
        Args:
            article: Bài viết cần sửa
            score_result: Kết quả chấm điểm SEO
            
        Returns:
            Kết quả auto-fix
        """
        try:
            logger.info(f"Starting auto-fix for article: {article.title}")
            logger.info(f"Initial score: {score_result.get('score_breakdown', {}).get('total', 0)}")
            
            # 1. Xây dựng fix tasks
            tasks = self.task_builder.build_tasks(score_result, article)
            logger.info(f"Built {len(tasks)} fix tasks")
            
            if not tasks:
                return AutoFixResponse(
                    patched_article=article.dict(),
                    applied_tasks=[],
                    skipped_tasks=[],
                    new_score=score_result,
                    success=True,
                    message="Không có task nào cần sửa"
                )
            
            # 2. Xử lý từng task bằng AI
            patches = []
            applied_tasks = []
            skipped_tasks = []
            
            for task in tasks:
                patch = await self.ai_fix_service.process_task(task, article.dict())
                
                if patch:
                    patches.append(patch)
                    applied_tasks.append(task)
                    logger.info(f"Generated patch for task {task.task_id}")
                else:
                    task.status = "skipped"
                    skipped_tasks.append(task)
                    logger.warning(f"Failed to generate patch for task {task.task_id}")
            
            # 3. Áp dụng patches
            if patches:
                patched_article = self.patch_service.apply_patches(article, patches)
                patch_summary = self.patch_service.get_patch_summary(patches)
                logger.info(f"Applied {patch_summary['applied']} patches")
            else:
                patched_article = article
                patch_summary = {"applied": 0, "skipped": 0}
            
            # 4. Chấm điểm lại
            new_score = None
            if patch_summary['applied'] > 0:
                try:
                    # Chuyển đổi sang dict để gọi SEO checker
                    article_dict = patched_article.dict()
                    
                    # Tạo request data cho SEO checker
                    request_data = {
                        'title': article_dict.get('title', ''),
                        'meta_description': article_dict.get('meta_description', ''),
                        'content': article_dict.get('html_content', ''),
                        'keywords': article_dict.get('keywords', []),
                        'industry': None
                    }
                    
                    # Nếu có blocks, tạo HTML content từ blocks
                    if article_dict.get('blocks'):
                        html_content = self._blocks_to_html(article_dict['blocks'])
                        request_data['content'] = html_content
                    
                    # Chấm điểm lại
                    new_score = self.seo_checker.analyze_seo(request_data)
                    logger.info(f"New score: {new_score.get('score_breakdown', {}).get('total', 0)}")
                    
                except Exception as e:
                    logger.error(f"Failed to re-score article: {e}")
                    new_score = score_result
            
            # 5. Cập nhật trạng thái tasks
            for task in applied_tasks:
                task.status = "completed"
            
            # 6. Tạo response
            response = AutoFixResponse(
                patched_article=patched_article.dict(),
                applied_tasks=applied_tasks,
                skipped_tasks=skipped_tasks,
                new_score=new_score,
                success=True,
                message=f"Đã áp dụng {patch_summary['applied']}/{len(tasks)} fix tasks"
            )
            
            logger.info(f"Auto-fix completed: {response.message}")
            return response
            
        except Exception as e:
            logger.error(f"Auto-fix failed: {e}")
            return AutoFixResponse(
                patched_article=article.dict(),
                applied_tasks=[],
                skipped_tasks=[],
                new_score=score_result,
                success=False,
                message=f"Lỗi auto-fix: {str(e)}"
            )
    
    def _blocks_to_html(self, blocks: List[Dict[str, Any]]) -> str:
        """Chuyển blocks sang HTML để chấm điểm"""
        html_parts = []
        
        for block in blocks:
            tag = block.get('tag', 'p')
            text = block.get('text', '')
            
            if tag in ['h1', 'h2', 'h3', 'h4']:
                html_parts.append(f"<{tag}>{text}</{tag}>")
            elif tag == 'p':
                html_parts.append(f"<p>{text}</p>")
            elif tag == 'li':
                html_parts.append(f"<li>{text}</li>")
        
        return '\n'.join(html_parts)
    
    async def auto_fix_with_iteration(self, 
                                     article: SEOArticle,
                                     initial_score: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Auto-fix với vòng lặp cho đến khi đạt điểm tối thiểu
        
        Args:
            article: Bài viết cần sửa
            initial_score: Điểm ban đầu (nếu có)
            
        Returns:
            Kết quả với lịch sử các lần fix
        """
        current_article = article
        iteration = 0
        all_applied_tasks = []
        all_skipped_tasks = []
        history = []
        
        # Lấy điểm ban đầu nếu chưa có
        if not initial_score:
            try:
                article_dict = article.dict()
                request_data = {
                    'title': article_dict.get('title', ''),
                    'meta_description': article_dict.get('meta_description', ''),
                    'content': article_dict.get('html_content', ''),
                    'keywords': article_dict.get('keywords', []),
                    'industry': None
                }
                
                if article_dict.get('blocks'):
                    html_content = self._blocks_to_html(article_dict['blocks'])
                    request_data['content'] = html_content
                
                initial_score = self.seo_checker.analyze_seo(request_data)
            except Exception as e:
                logger.error(f"Failed to get initial score: {e}")
                initial_score = {"score_breakdown": {"total": 0}}
        
        current_score = initial_score
        
        while iteration < self.max_iterations:
            iteration += 1
            logger.info(f"Auto-fix iteration {iteration}")
            
            # Thực hiện auto-fix
            fix_result = await self.auto_fix_seo(current_article, current_score)
            
            # Lưu lịch sử
            history.append({
                "iteration": iteration,
                "score_before": current_score.get('score_breakdown', {}).get('total', 0),
                "score_after": fix_result.new_score.get('score_breakdown', {}).get('total', 0) 
                             if fix_result.new_score else 0,
                "applied_tasks": len(fix_result.applied_tasks),
                "skipped_tasks": len(fix_result.skipped_tasks)
            })
            
            # Cập nhật tasks
            all_applied_tasks.extend(fix_result.applied_tasks)
            all_skipped_tasks.extend(fix_result.skipped_tasks)
            
            # Kiểm tra điều kiện dừng
            current_score_total = fix_result.new_score.get('score_breakdown', {}).get('total', 0) \
                                 if fix_result.new_score else 0
            
            if current_score_total >= self.min_score_threshold:
                logger.info(f"Score reached threshold ({current_score_total} >= {self.min_score_threshold})")
                break
            
            if not fix_result.applied_tasks or len(fix_result.applied_tasks) == 0:
                logger.info("No more tasks to apply")
                break
            
            # Cập nhật cho vòng lặp tiếp theo
            current_article = SEOArticle(**fix_result.patched_article)
            current_score = fix_result.new_score or current_score
        
        # Tạo final response
        final_score_total = current_score.get('score_breakdown', {}).get('total', 0) \
                           if current_score else 0
        
        return {
            "final_article": current_article.dict(),
            "final_score": current_score,
            "history": history,
            "total_iterations": iteration,
            "total_applied_tasks": len(all_applied_tasks),
            "total_skipped_tasks": len(all_skipped_tasks),
            "initial_score": initial_score.get('score_breakdown', {}).get('total', 0),
            "final_score_total": final_score_total,
            "score_improvement": final_score_total - initial_score.get('score_breakdown', {}).get('total', 0),
            "success": True
        }