# services/seo_checker/auto_fix/seo_fix_task_builder.py
"""
Service xây dựng FixTask từ SEO issues
Mỗi issue → 1 FixTask với target cụ thể
"""

import logging
from typing import List, Dict, Any, Optional
from enum import Enum
import uuid
from models.llm.content_generation_schemas import SEOArticle
from models.seo_checker.fix_schemas import FixTask, FixTarget, FixScope, FixTaskSeverity

logger = logging.getLogger(__name__)

class FixTaskBuilder:
    """Builder chuyển đổi SEO issues thành FixTask"""
    
    # Mapping từ issue type sang scope và target
    ISSUE_MAPPING = {
        # Keyword issues
        "keyword_not_in_first_paragraph": {"scope": FixScope.BLOCK, "target": "first_paragraph"},
        "keyword_not_in_h1": {"scope": FixScope.BLOCK, "target": "h1"},
        "keyword_not_in_h2": {"scope": FixScope.BLOCK, "target": "h2"},
        "keyword_not_in_title": {"scope": FixScope.META, "target": "title"},
        "keyword_not_in_meta": {"scope": FixScope.META, "target": "meta_description"},
        "keyword_stuffing": {"scope": FixScope.BLOCK, "target": "detected_block"},
        "keyword_density_too_low": {"scope": FixScope.BLOCK, "target": "multiple_blocks"},
        
        # Title issues
        "title_too_short": {"scope": FixScope.META, "target": "title"},
        "title_too_long": {"scope": FixScope.META, "target": "title"},
        
        # Meta issues
        "meta_too_short": {"scope": FixScope.META, "target": "meta_description"},
        
        # Structure issues
        "missing_h1": {"scope": FixScope.STRUCTURAL, "target": "add_h1"},
        "multiple_h1": {"scope": FixScope.BLOCK, "target": "extra_h1"},
        "few_h2": {"scope": FixScope.STRUCTURAL, "target": "add_h2"},
        "too_many_h3": {"scope": FixScope.BLOCK, "target": "extra_h3"},
        
        # Readability issues
        "paragraph_too_long": {"scope": FixScope.BLOCK, "target": "long_paragraph"},
        "many_long_sentences": {"scope": FixScope.BLOCK, "target": "paragraph_with_long_sentences"},
        
        # Technical issues
        "missing_alt_text": {"scope": FixScope.STRUCTURAL, "target": "add_alt_text"},
        "no_internal_links": {"scope": FixScope.STRUCTURAL, "target": "add_internal_links"},
        
        # Content quality issues
        "content_too_short": {"scope": FixScope.STRUCTURAL, "target": "add_content"},
    }
    
    # Mapping severity
    SEVERITY_MAP = {
        "critical": FixTaskSeverity.CRITICAL,
        "warning": FixTaskSeverity.WARNING,
        "info": FixTaskSeverity.INFO
    }
    
    def __init__(self):
        self.task_counter = 0
    
    def build_tasks(self, 
                   score_result: Dict[str, Any], 
                   article: SEOArticle) -> List[FixTask]:
        """
        Xây dựng danh sách FixTask từ kết quả chấm điểm
        
        Args:
            score_result: Kết quả từ SEO checker
            article: Bài viết gốc
            
        Returns:
            List[FixTask]: Danh sách tasks cần sửa
        """
        tasks = []
        
        # Lấy tất cả issues từ result
        issues_by_severity = score_result.get('issues', {})
        
        # Duyệt qua từng severity level
        for severity_level, issues in issues_by_severity.items():
            for issue in issues:
                task = self._build_single_task(issue, severity_level, article)
                if task:
                    tasks.append(task)
        
        # Sắp xếp theo mức độ ưu tiên: critical → warning → info
        tasks.sort(key=lambda x: {
            FixTaskSeverity.CRITICAL: 0,
            FixTaskSeverity.WARNING: 1,
            FixTaskSeverity.INFO: 2
        }[x.severity])
        
        logger.info(f"Built {len(tasks)} fix tasks from {sum(len(issues) for issues in issues_by_severity.values())} issues")
        return tasks
    
    def _build_single_task(self, 
                          issue: Dict[str, Any], 
                          severity_level: str,
                          article: SEOArticle) -> Optional[FixTask]:
        """
        Xây dựng 1 FixTask từ 1 issue
        
        Args:
            issue: Issue dict từ SEO checker
            severity_level: critical/warning/info
            article: Bài viết gốc
            
        Returns:
            FixTask hoặc None nếu không thể map
        """
        issue_type = issue.get('type')
        
        # Kiểm tra mapping
        if issue_type not in self.ISSUE_MAPPING:
            logger.warning(f"Không có mapping cho issue type: {issue_type}")
            return None
        
        mapping = self.ISSUE_MAPPING[issue_type]
        scope = mapping['scope']
        target_type = mapping['target']
        
        # Xây dựng target
        target = self._build_target(issue_type, target_type, article, issue)
        if not target:
            logger.warning(f"Không thể xác định target cho issue: {issue_type}")
            return None
        
        # Xây dựng payload
        payload = self._build_payload(issue_type, issue, article, target)
        
        # Lấy current text
        current_text = self._get_current_text(target, article, issue)
        
        # Tạo task
        task_id = f"fix-{self._generate_task_id()}"
        
        return FixTask(
            task_id=task_id,
            type=issue_type,
            target=target,
            payload=payload,
            current_text=current_text,
            recommendation=issue.get('recommendation', ''),
            severity=self.SEVERITY_MAP.get(severity_level, FixTaskSeverity.INFO),
            status="pending"
        )
    
    def _build_target(self, 
                     issue_type: str, 
                     target_type: str,
                     article: SEOArticle,
                     issue: Dict[str, Any]) -> Optional[FixTarget]:
        """
        Xây dựng FixTarget từ issue type
        
        Args:
            issue_type: Loại issue
            target_type: Loại target từ mapping
            article: Bài viết
            issue: Issue dict
            
        Returns:
            FixTarget object
        """
        # Xử lý block scope
        if target_type in ["first_paragraph", "h1", "h2", "long_paragraph"]:
            block_id = self._find_target_block_id(target_type, article, issue)
            if block_id:
                return FixTarget(scope=FixScope.BLOCK, block_id=block_id)
        
        # Xử lý meta scope
        elif target_type in ["title", "meta_description"]:
            return FixTarget(scope=FixScope.META, field_name=target_type)
        
        # Xử lý structural scope
        elif target_type in ["add_h1", "add_h2", "add_content", "add_internal_links", "add_alt_text"]:
            return FixTarget(scope=FixScope.STRUCTURAL)
        
        # Xử lý detected block (cho keyword stuffing)
        elif target_type == "detected_block":
            # Tìm block có keyword density cao nhất
            if 'keyword' in issue.get('detail', '').lower():
                keyword = self._extract_keyword_from_issue(issue)
                if keyword and article.blocks:
                    # Tìm block có nhiều keyword nhất
                    max_count = 0
                    target_block_id = None
                    
                    for block in article.blocks:
                        if block.tag == 'p':
                            count = block.text.lower().count(keyword.lower())
                            if count > max_count:
                                max_count = count
                                target_block_id = block.id
                    
                    if target_block_id:
                        return FixTarget(scope=FixScope.BLOCK, block_id=target_block_id)
        
        return None
    
    def _find_target_block_id(self, 
                             target_type: str,
                             article: SEOArticle,
                             issue: Dict[str, Any]) -> Optional[str]:
        """
        Tìm block_id dựa trên target_type
        
        Args:
            target_type: Loại block cần tìm
            article: Bài viết
            issue: Issue dict (có thể chứa block_id nếu có)
            
        Returns:
            block_id hoặc None
        """
        # Nếu issue đã có block_id (từ block-based analyzer)
        if 'block_id' in issue and issue['block_id']:
            return issue['block_id']
        
        # Tìm block dựa trên target_type
        if not article.blocks:
            return None
        
        if target_type == "first_paragraph":
            # Tìm paragraph đầu tiên
            for block in article.blocks:
                if block.tag == 'p':
                    return block.id
        
        elif target_type == "h1":
            # Tìm H1 đầu tiên
            for block in article.blocks:
                if block.tag == 'h1':
                    return block.id
        
        elif target_type == "h2":
            # Tìm H2 đầu tiên
            for block in article.blocks:
                if block.tag == 'h2':
                    return block.id
        
        elif target_type == "long_paragraph":
            # Tìm paragraph dài nhất
            max_words = 0
            target_id = None
            
            for block in article.blocks:
                if block.tag == 'p':
                    words = block.word_count or len(block.text.split())
                    if words > max_words:
                        max_words = words
                        target_id = block.id
            
            return target_id
        
        return None
    
    def _build_payload(self, 
                      issue_type: str,
                      issue: Dict[str, Any],
                      article: SEOArticle,
                      target: FixTarget) -> Dict[str, Any]:
        """
        Xây dựng payload cho task
        
        Args:
            issue_type: Loại issue
            issue: Issue dict
            article: Bài viết
            target: FixTarget
            
        Returns:
            Dict payload
        """
        payload = {}
        
        # Keyword-related issues
        if 'keyword' in issue_type:
            keyword = self._extract_keyword_from_issue(issue)
            if keyword:
                payload['keyword'] = keyword
                payload['action'] = 'insert_keyword' if 'not_in' in issue_type else 'reduce_keyword'
        
        # Length-related issues
        elif 'too_short' in issue_type or 'too_long' in issue_type:
            current_length = len(issue.get('current_text', '')) if 'current_text' in issue else 0
            payload['current_length'] = current_length
            
            # Ước tính target length từ recommendation
            rec = issue.get('recommendation', '')
            if 'nên có' in rec or 'ít nhất' in rec:
                # Parse số từ recommendation
                import re
                numbers = re.findall(r'\d+', rec)
                if numbers:
                    payload['target_length'] = int(numbers[0])
        
        # Structure issues
        elif issue_type in ['missing_h1', 'few_h2', 'no_internal_links']:
            payload['action'] = 'add_element'
            if 'h1' in issue_type:
                payload['element_type'] = 'h1'
                # Lấy keyword từ article
                if article.keywords:
                    payload['suggested_text'] = f"{article.keywords[0]} - {article.title}"
            elif 'h2' in issue_type:
                payload['element_type'] = 'h2'
            elif 'links' in issue_type:
                payload['element_type'] = 'internal_link'
        
        return payload
    
    def _extract_keyword_from_issue(self, issue: Dict[str, Any]) -> Optional[str]:
        """Trích xuất keyword từ issue detail"""
        detail = issue.get('detail', '')
        
        # Tìm pattern: "Keyword '...'"
        import re
        match = re.search(r"Keyword\s+['\"]([^'\"]+)['\"]", detail)
        if match:
            return match.group(1)
        
        # Tìm trong recommendation
        rec = issue.get('recommendation', '')
        match = re.search(r"keyword\s+['\"]([^'\"]+)['\"]", rec, re.IGNORECASE)
        if match:
            return match.group(1)
        
        return None
    
    def _get_current_text(self, 
                         target: FixTarget,
                         article: SEOArticle,
                         issue: Dict[str, Any]) -> Optional[str]:
        """Lấy current text dựa trên target"""
        if target.scope == FixScope.BLOCK and target.block_id:
            # Tìm block theo ID
            for block in article.blocks:
                if block.id == target.block_id:
                    return block.text
        
        elif target.scope == FixScope.META:
            if target.field_name == 'title':
                return article.title
            elif target.field_name == 'meta_description':
                return article.meta_description
        
        return issue.get('current_text', None)
    
    def _generate_task_id(self) -> str:
        """Tạo task ID duy nhất"""
        self.task_counter += 1
        return f"{self.task_counter:03d}"