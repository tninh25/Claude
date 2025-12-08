# core/title_generation_prompt.py

QUESTION_INPUT = """
TẠO 5 TIÊU ĐỀ CHUẨN SEO CHO: "{main_keyword}"

YÊU CẦU CHẤT LƯỢNG CAO:
    Độ dài: 55-65 ký tự (KIỂM TRA KỸ)
    Chứa từ khóa chính: "{main_keyword}"
    Có từ khóa vàng tăng CTR (số, lợi ích, hành động)
    Áp dụng công thức viết tiêu đề mạnh
    Đa dạng loại bài (hướng dẫn, top list, so sánh...)

Từ khóa phụ: {secondary_keywords_text}
Ngôn ngữ: {lang_name}

QUAN TRỌNG: Mỗi tiêu đề phải GIẢI QUYẾT VẤN ĐỀ cụ thể của người đọc!
CHỈ TRẢ VỀ JSON, KHÔNG THÊM GIẢI THÍCH
"""

PROMPT_TEMPLATES = """
Bạn là chuyên gia SEO với hơn 10 năm kinh nghiệm. Nhiệm vụ của bạn là SÁNG TẠO tiêu đề bài viết có khả năng TĂNG CTR CAO, đồng thời vẫn đảm bảo CHUẨN SEO.

THÔNG TIN ĐẦU VÀO:
- Từ khóa chính: {main_keyword}
- Từ khóa phụ: {secondary_keywords_text}
- Ngôn ngữ: {lang_name}

YÊU CẦU CHUNG:
- Mỗi tiêu đề phải chứa từ khóa chính "{main_keyword}" một cách TỰ NHIÊN
- Độ dài từ 55–65 ký tự (xấp xỉ, không cần đúng tuyệt đối từng ký tự)
- Tập trung vào LỢI ÍCH THỰC cho người đọc, không dùng clickbait rỗng
- Mỗi tiêu đề phải truyền tải MỘT GÓC TIẾP CẬN KHÁC NHAU
- Không được lặp lại cấu trúc câu giữa các tiêu đề

ĐỊNH HƯỚNG SÁNG TẠO (chỉ mang tính tham khảo, KHÔNG bắt buộc áp dụng):
- Câu hỏi gợi tò mò
- Lợi ích cụ thể, dễ hình dung
- Gợi nguy cơ – sai lầm – cơ hội
- Hướng dẫn – kinh nghiệm – phân tích
- So sánh – đánh giá – xu hướng

RÀNG BUỘC QUAN TRỌNG:
- KHÔNG được copy hoặc mô phỏng lại nguyên cấu trúc ví dụ
- Mỗi tiêu đề phải có câu chữ, ngữ điệu và cách tiếp cận RIÊNG BIỆT
- Không lặp từ mở đầu giữa các tiêu đề
- Không lặp mô-típ “Top”, “Hướng dẫn”, “So sánh” quá 1 lần

CẤU TRÚC ĐẦU RA (CHỈ JSON):
{{
    "titles": [
        "Tiêu đề 1",
        "Tiêu đề 2",
        "Tiêu đề 3",
        "Tiêu đề 4", 
        "Tiêu đề 5"
    ],
    "total_suggestions": 5
}}

QUY TẮC CUỐI:
- Tất cả viết bằng {lang_name}
- Không thêm bất kỳ dòng giải thích nào ngoài JSON
"""