# services/crawl/image_utils.py
from typing import List
from urllib.parse import parse_qs, urlparse


IMAGE_EXTS = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.svg']


def clean_image_urls(image_urls: List[str], max_images: int) -> List[str]:
    """
    Giữ nguyên ý tưởng ban đầu:
    - loại bỏ url rác
    - chuẩn hóa, lấy base url (loại query param trùng lặp)
    - ưu tiên URL tốt nhất theo params (w, qlt ...)
    - giữ duy nhất 1 bản cho mỗi base_url
    - trả về tối đa max_images
    """
    if not image_urls:
        return []

    cleaned_urls: List[str] = []
    seen_base_urls = set()

    for raw in image_urls:
        if not raw:
            continue

        url = raw.strip()
        if url == "":
            continue

        # bỏ những file rõ ràng không phải ảnh
        low = url.lower()
        if any(bad in low for bad in ['transparent.png', 'pixel.gif', 'blank.gif', 'spacer.gif']):
            continue

        # bỏ base64 quá dài
        if low.startswith('data:image') and len(url) > 1000:
            continue

        base_url = extract_base_image_url(url)

        # only add if base_url not seen
        if base_url and base_url not in seen_base_urls:
            seen_base_urls.add(base_url)
            best = select_best_quality_url(url, base_url)
            cleaned_urls.append(best)

            if len(cleaned_urls) >= max_images:
                break

    return cleaned_urls[:max_images]


def extract_base_image_url(url: str) -> str:
    """
    Trích base URL trước dấu ? ; nếu có đuôi ảnh thì trả về base, 
    nếu không có extension rõ ràng trả về chính url (giống logic gốc).
    """
    base = url.split('?')[0]
    if any(base.lower().endswith(ext) for ext in IMAGE_EXTS):
        return base
    return url


def select_best_quality_url(current_url: str, base_url: str) -> str:
    """
    Giữ logic gốc: ưu tiên url không có parameters; nếu có params
    cố gắng parse 'w' hoặc 'qlt' để chọn url chất lượng hơn.
    Nếu parse thất bại, trả về base_url.
    """
    if '?' not in current_url:
        return current_url

    try:
        parsed = urlparse(current_url)
        params = parse_qs(parsed.query)

        if 'w' in params:
            try:
                width = int(params['w'][0])
                if width >= 400:
                    return current_url
            except Exception:
                pass

        if 'qlt' in params:
            try:
                quality = int(params['qlt'][0])
                if quality >= 80:
                    return current_url
            except Exception:
                pass

    except Exception:
        # nếu parse lỗi, fallback về base_url
        pass

    return base_url
