# core/ai_prompt/content_generation_prompt.py

from string import Template
from core.ai_prompt.content_generation_prompt_block import (
    SYSTEM_ROLE,
    SEO_STRATEGY,
    CONTENT_QUALITY_RULES,
    BLOCK_OUTPUT_RULES,
    JSON_OUTPUT_RULE
)

REFERENCE_TEMPLATE = Template("""
BÀI THAM KHẢO $idx
- Tiêu đề: $title
- URL: $url
- Nội dung chính:
$content_preview
""")

COMMON_INPUT = Template("""
THÔNG TIN BÀI VIẾT:
- Tiêu đề: $article_title
- Từ khóa chính: $main_keyword
- Từ khóa phụ: $secondary_keywords
- Ngôn ngữ: $language
- Độ dài mục tiêu: $article_length từ

OUTLINE BẮT BUỘC PHẢI THEO:
$article_outline

DANH SÁCH BÀI THAM KHẢO:
$references_text

DANH SÁCH HÌNH ẢNH:
$image_text
""")

# =========================
# BLOG PROMPT – CHUYÊN SÂU
# =========================

BLOG_PROMPT = Template("""
$SYSTEM_ROLE
$SEO_STRATEGY
$CONTENT_QUALITY_RULES

Bạn là chuyên gia viết Blog SEO chuyên sâu.

Phong cách: $tone
Loại bài: Blog chia sẻ – hướng dẫn – phân tích chuyên sâu

YÊU CẦU BẮT BUỘC:
1. Viết HOÀN TOÀN MỚI bằng $language
2. Không sao chép bất kỳ nội dung nào
3. Bám sát OUTLINE
4. Mỗi H2 phải có:
   - 1 đoạn giải thích
   - 1 đoạn phân tích
   - 1 đoạn ví dụ hoặc ứng dụng
5. Các phần phải liên kết logic với nhau
6. Không viết lan man, không kể lể

$COMMON_INPUT

CẤU TRÚC BLOG:
- 1 H1 duy nhất
- Mở bài: 1–2 đoạn p
- Mỗi H2: 2–4 đoạn p
- Có H3 khi mở rộng chuyên sâu
- Kết bài: 1 đoạn tổng kết + CTA nhẹ

SEO ONPAGE:
- Title SEO 55–65 ký tự
- Meta description 150–160 ký tự
- Từ khóa chính xuất hiện tự nhiên
- Từ khóa phụ phân bổ đều theo từng section

$BLOCK_OUTPUT_RULES

OUTPUT JSON:
{
  "meta_description": "...",
  "title": "...",
  "blocks": [...],
  "keywords": ["...", "...", "..."],
  "references": [
    {"title": "...", "url": "..."}
  ]
}

$JSON_OUTPUT_RULE
""")

# =========================
# NEWS PROMPT – CHUẨN SEO NEWS
# =========================

NEWS_PROMPT = Template("""
$SYSTEM_ROLE
$CONTENT_QUALITY_RULES

Bạn là biên tập viên tin tức chuyên nghiệp.

Phong cách: $tone
Loại bài: Tin tức – cập nhật – sự kiện

YÊU CẦU:
1. Viết HOÀN TOÀN MỚI bằng $language
2. Trung lập – khách quan – chính xác
3. Ưu tiên dữ liệu, số liệu, mốc thời gian
4. Tối ưu hiển thị Google News

CẤU TRÚC 5W1H:
- Who – Ai?
- What – Chuyện gì?
- When – Khi nào?
- Where – Ở đâu?
- Why – Vì sao?
- How – Diễn biến thế nào?

$COMMON_INPUT

BỐ CỤC:
- Headline
- Lead (2–3 câu tóm tắt)
- Body (diễn biến theo timeline)
- Quotes (nếu có)
- Background
- Kết: tác động & hướng tiếp theo

SEO NEWS:
- Meta 150–160 ký tự
- Title mạnh, rõ ràng
- Từ khóa chính trong headline + lead
- Không giật tít

OUTPUT JSON:
{
  "meta_description": "...",
  "title": "...",
  "content": "... (HTML format)",
  "keywords": ["...", "...", "..."],
  "references": [
    {"title": "...", "url": "..."}
  ]
}

$JSON_OUTPUT_RULE
""")

PROMPT_TEMPLATES = {
    "blog": BLOG_PROMPT,
    "news": NEWS_PROMPT
}