# core/content_review_prompt.py

REVIEW_SYSTEM_TEMPLATE = """
Bạn là chuyên gia SEO với 10 năm kinh nghiệm. Đánh giá bài viết dựa trên:
1. Chất lượng nội dung & giá trị cho người đọc
2. Tối ưu SEO (từ khóa, meta, title)
3. Phù hợp với yêu cầu và tone giọng
4. Tính hấp dẫn và thu hút

Trả lời bằng JSON format cố định.
"""

SCORING_CRITERIA = {
    "content_quality": {"weight": 0.3, "description": "Độ sâu, giá trị, độc đáo"},
    "seo_optimization": {"weight": 0.3, "description": "Từ khóa, meta, title"},
    "style_tone": {"weight": 0.2, "description": "Phù hợp tone giọng yêu cầu"},
    "requirements": {"weight": 0.2, "description": "Đáp ứng yêu cầu đặc biệt"}
}