# core/ai_prompt/news_filtering_prompt.py

REFERENCE_TEMPLATE = """
TIN {idx}
Tiêu đề: {title}
URL: {url}
Nội dung: {content_preview}
"""

QUESTION_TEMPLATES = """
THÔNG TIN BÀI VIẾT CẦN VIẾT:
- TIÊU ĐỀ: {article_title}
- TỪ KHÓA CHÍNH: {main_keyword}
- TỪ KHÓA PHỤ: {secondary_keywords}

DANH SÁCH TIN TỪ NGUỒN:
{news_text}
"""

PROMPT_TEMPLATES = """
Bạn là chuyên gia SEO và content planning. Nhiệm vụ của bạn:

BƯỚC 1: LỌC TIN TỨC
1. Đọc tiêu đề bài viết cần viết: "{article_title}"
2. Đọc từ khóa chính: "{main_keyword}"
3. Đọc và phân tích các tin tức dưới đây
4. Chọn 3 tin CÓ NỘI DUNG PHÙ HỢP NHẤT với cả tiêu đề và từ khóa
5. Loại bỏ hình ảnh trùng lặp trong mỗi tin

BƯỚC 2: TẠO OUTLINE JSON
Tạo outline dạng JSON cấu trúc cho bài viết dựa trên tiêu đề, từ khóa và nội dung 3 tin đã chọn.
Outline chỉ có id, level, title, order - KHÔNG có field config.

QUY TẮC TẠO OUTLINE:
- Mỗi heading phải có: id (duy nhất), level (1-6), title, order (số thứ tự)
- KHÔNG tạo field "config" - field này do user tự cấu hình sau
- Level 1 (H1): Tiêu đề chính của bài viết
- Level 2 (H2): Các phần lớn
- Level 3 (H3): Các mục con chi tiết
- ID format: "h{{level}}-{{số thứ tự}}", ví dụ: "h1-1", "h2-1", "h3-1"
- Order: số thứ tự tăng dần từ 1

VÍ DỤ OUTLINE JSON:
{{
  "article_outline": [
    {{
      "id": "h1-1",
      "level": 1,
      "title": "Tiêu đề bài viết chính",
      "order": 1
    }},
    {{
      "id": "h2-1",
      "level": 2,
      "title": "Phần giới thiệu",
      "order": 2
    }},
    {{
      "id": "h2-2",
      "level": 2,
      "title": "Nội dung chính",
      "order": 3
    }},
    {{
      "id": "h3-1",
      "level": 3,
      "title": "Chi tiết 1",
      "order": 4
    }},
    {{
      "id": "h3-2",
      "level": 3,
      "title": "Chi tiết 2",
      "order": 5
    }},
    {{
      "id": "h2-3",
      "level": 2,
      "title": "Kết luận",
      "order": 6
    }}
  ]
}}

TRẢ VỀ JSON VỚI CẤU TRÚC SAU:
{{
  "selected_news": [
    {{
      "rank": 1,
      "title": "Tiêu đề tin 1",
      "url": "https://example.com/1",
      "images": ["url1.jpg", "url2.jpg"]
    }},
    {{
      "rank": 2,
      "title": "Tiêu đề tin 2",
      "url": "https://example.com/2",
      "images": ["url3.jpg"]
    }},
    {{
      "rank": 3,
      "title": "Tiêu đề tin 3",
      "url": "https://example.com/3",
      "images": ["url4.jpg", "url5.jpg"]
    }}
  ],
  "article_outline": [
    {{
      "id": "h1-1",
      "level": 1,
      "title": "{article_title}",
      "order": 1
    }},
    {{
      "id": "h2-1",
      "level": 2,
      "title": "Phần 1 - Dựa trên nội dung các tin đã chọn",
      "order": 2
    }},
    {{
      "id": "h3-1",
      "level": 3,
      "title": "Chi tiết 1.1",
      "order": 3
    }},
    {{
      "id": "h2-2",
      "level": 2,
      "title": "Phần 2",
      "order": 4
    }},
    {{
      "id": "h2-3",
      "level": 2,
      "title": "Kết luận",
      "order": 5
    }}
  ]
}}

LƯU Ý QUAN TRỌNG:
- CHỈ TRẢ VỀ JSON, KHÔNG THÊM BẤT KỲ TEXT NÀO KHÁC
- article_outline là ARRAY của các object heading, KHÔNG phải HTML string
- Mỗi heading CHỈ có 4 field: id, level, title, order
- KHÔNG tạo field "config" - user sẽ tự cấu hình sau
"""