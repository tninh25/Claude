# core/ai_prompt/seo_fix_prompts.py
"""
Prompt templates cho AI sửa SEO theo block
"""

class SEOFixPrompts:
    """Collection các prompt sửa SEO"""
    
    @staticmethod
    def get_block_fix_prompt(block_id: str, tag: str, keyword: str, 
                            current_text: str, recommendation: str) -> str:
        """
        Prompt sửa 1 block cụ thể
        
        Args:
            block_id: ID của block
            tag: Loại tag (h1, h2, p, ...)
            keyword: Keyword cần chèn/giảm
            current_text: Nội dung hiện tại
            recommendation: Khuyến nghị sửa
            
        Returns:
            Prompt string
        """
        return f"""
        BẠN LÀ CHUYÊN GIA SEO CHỈNH SỬA NỘI DUNG.
        
        ## NHIỆM VỤ:
        Chỉnh sửa ĐÚNG 1 đoạn văn bản (block) theo yêu cầu SEO.
        
        ## THÔNG TIN BLOCK:
        - Block ID: {block_id}
        - Loại tag: {tag}
        - Keyword cần xử lý: "{keyword}"
        - Nội dung hiện tại: "{current_text}"
        
        ## YÊU CẦU CHỈNH SỬA:
        {recommendation}
        
        ## QUY TẮC BẮT BUỘC:
        1. CHỈ sửa đoạn văn bản này, không sửa bất kỳ đoạn nào khác
        2. Giữ nguyên ý chính, không thay đổi thông tin quan trọng
        3. Giữ nguyên giọng văn, phong cách
        4. Không thêm HTML tag, chỉ text thuần
        5. Không tạo block mới, không xóa block
        6. Nếu là H1/H2: giữ nguyên cấu trúc heading
        7. Keyword phải xuất hiện tự nhiên, không nhồi nhét
        
        ## OUTPUT FORMAT (JSON DUY NHẤT):
        {{
            "block_id": "{block_id}",
            "new_text": "nội dung đã sửa ở đây"
        }}
        
        Chỉ trả về JSON, không giải thích thêm.
        """
    
    @staticmethod
    def get_meta_fix_prompt(field_name: str, current_value: str, 
                           recommendation: str, article_keywords: list) -> str:
        """
        Prompt sửa meta field (title, meta_description)
        
        Args:
            field_name: title hoặc meta_description
            current_value: Giá trị hiện tại
            recommendation: Khuyến nghị sửa
            article_keywords: Danh sách keywords
            
        Returns:
            Prompt string
        """
        field_vietnamese = "tiêu đề" if field_name == "title" else "meta description"
        
        return f"""
        BẠN LÀ CHUYÊN GIA SEO CHỈNH SỬA {field_name.upper()}.
        
        ## NHIỆM VỤ:
        Chỉnh sửa {field_vietnamese} bài viết để tối ưu SEO.
        
        ## THÔNG TIN HIỆN TẠI:
        - {field_vietnamese} hiện tại: "{current_value}"
        - Keywords chính: {article_keywords}
        
        ## YÊU CẦU CHỈNH SỬA:
        {recommendation}
        
        ## QUY TẮC SEO:
        1. Tiêu đề (title): 50-60 ký tự, chứa keyword chính ở đầu
        2. Meta description: 120-160 ký tự, chứa keyword, có call-to-action
        3. Giữ nguyên thông tin chính của bài viết
        4. Tự nhiên, hấp dẫn người đọc
        5. Không spam keyword
        
        ## OUTPUT FORMAT (JSON DUY NHẤT):
        {{
            "field": "{field_name}",
            "new_value": "giá trị mới ở đây"
        }}
        
        Chỉ trả về JSON, không giải thích thêm.
        """
    
    @staticmethod
    def get_structural_fix_prompt(issue_type: str, recommendation: str, 
                                 article_title: str, article_keywords: list) -> str:
        """
        Prompt sửa cấu trúc (thêm block mới)
        
        Args:
            issue_type: Loại issue (missing_h1, few_h2, ...)
            recommendation: Khuyến nghị sửa
            article_title: Tiêu đề bài viết
            article_keywords: Danh sách keywords
            
        Returns:
            Prompt string
        """
        element_map = {
            "missing_h1": {"type": "h1", "desc": "thẻ H1 chính"},
            "few_h2": {"type": "h2", "desc": "thẻ H2"},
            "no_internal_links": {"type": "paragraph", "desc": "đoạn văn có internal link"},
            "add_content": {"type": "paragraph", "desc": "đoạn văn bổ sung nội dung"}
        }
        
        element_info = element_map.get(issue_type, {"type": "paragraph", "desc": "phần tử"})
        
        return f"""
        BẠN LÀ CHUYÊN GIA SEO TẠO NỘI DUNG MỚI.
        
        ## NHIỆM VỤ:
        Tạo {element_info['desc']} mới cho bài viết.
        
        ## THÔNG TIN BÀI VIẾT:
        - Tiêu đề: "{article_title}"
        - Keywords: {article_keywords}
        
        ## YÊU CẦU:
        {recommendation}
        
        ## QUY TẮC TẠO NỘI DUNG:
        1. Phù hợp với ngữ cảnh bài viết
        2. Chứa keyword chính một cách tự nhiên
        3. Giọng văn chuyên nghiệp, hấp dẫn
        4. Độ dài phù hợp: H1 5-10 từ, H2 5-8 từ, paragraph 50-100 từ
        5. Không lặp lại nội dung đã có
        
        ## OUTPUT FORMAT (JSON DUY NHẤT):
        {{
            "element_type": "{element_info['type']}",
            "new_text": "nội dung mới ở đây"
        }}
        
        Chỉ trả về JSON, không giải thích thêm.
        """
    
    @staticmethod
    def get_keyword_reduction_prompt(block_id: str, current_text: str, 
                                    keyword: str, recommendation: str) -> str:
        """
        Prompt giảm keyword stuffing
        
        Args:
            block_id: ID block
            current_text: Nội dung hiện tại
            keyword: Keyword cần giảm
            recommendation: Khuyến nghị
            
        Returns:
            Prompt string
        """
        return f"""
        BẠN LÀ CHUYÊN GIA SEO GIẢM KEYWORD STUFFING.
        
        ## NHIỆM VỤ:
        Giảm tần suất keyword "{keyword}" trong đoạn văn mà vẫn giữ nguyên ý chính.
        
        ## THÔNG TIN:
        - Block ID: {block_id}
        - Nội dung hiện tại: "{current_text}"
        
        ## YÊU CẦU:
        {recommendation}
        
        ## QUY TẮC:
        1. Giữ nguyên ý chính, thông tin quan trọng
        2. Giảm số lần xuất hiện của keyword
        3. Thay thế bằng từ đồng nghĩa hoặc cách diễn đạt khác
        4. Giữ nguyên giọng văn, phong cách
        5. Không làm mất tính tự nhiên
        
        ## OUTPUT FORMAT (JSON DUY NHẤT):
        {{
            "block_id": "{block_id}",
            "new_text": "nội dung đã giảm keyword ở đây"
        }}
        
        Chỉ trả về JSON, không giải thích thêm.
        """