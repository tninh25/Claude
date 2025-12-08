# services/image/image_deduplication_service.py

import re
from typing import List, Dict, Tuple, Set
from urllib.parse import urlparse, urlunparse, parse_qs, unquote
import logging

logger = logging.getLogger(__name__)

class ImageDeduplicationService:
    """
    Service để phát hiện và loại bỏ hình ảnh trùng lặp
    Và chỉ giữ lại các ảnh có URL public hợp lệ (https://...)
    """
    
    # Patterns cho các kích thước phổ biến
    SIZE_PATTERNS = [
        r'[-_](\d+)x(\d+)',           # -300x169, _1024x768
        r'[-_](\d+)w',                 # -300w, _800w
        r'[-_](\d+)h',                 # -500h, _600h
        r'[-_]w(\d+)',                 # w300, w800
        r'[-_]h(\d+)',                 # h500, h600
        r'[-_](\d+)px',                # 300px, 800px
        r'[-_]size-(\d+)',             # size-300, size-800
        r'[-_](\d+)-(\d+)',            # 300-169, 800-600
    ]
    
    # Keywords cho chất lượng ảnh (ưu tiên giữ lại)
    QUALITY_KEYWORDS = [
        'large', 'original', 'full', 'high', 'hd', 'retina', 
        'quality', 'best', 'max', 'source', 'raw'
    ]
    
    # Keywords cho ảnh nhỏ/thấp (ưu tiên loại bỏ)
    LOW_QUALITY_KEYWORDS = [
        'thumb', 'thumbnail', 'small', 'mini', 'tiny', 
        'icon', 'avatar', 'preview', 'placeholder'
    ]
    
    # Domain patterns cho ảnh chất lượng cao (CDN, image hosting)
    QUALITY_DOMAINS = [
        'cdn', 'images', 'img', 'static', 'assets', 'media',
        'cloudfront', 'akamai', 'cloudinary', 'imgix', 'unsplash',
        'picsum', 'pexels', 'pixabay', 'flickr'
    ]
    
    # Patterns cho URL không public (cần loại bỏ)
    NON_PUBLIC_PATTERNS = [
        r'^/',                         # Relative paths starting with /
        r'^\./',                       # Relative paths starting with ./
        r'^\.\./',                     # Relative paths starting with ../
        r'^file://',                   # Local file URLs
        r'^data:image',               # Data URLs
        r'^blob:',                    # Blob URLs
        r'^/sites/default/files',     # Drupal private files
        r'^/wp-content/uploads',      # WordPress (relative)
        r'^/static/',                 # Static paths
        r'^/assets/',                 # Assets paths
        r'^/images/',                 # Images paths
        r'^/media/',                  # Media paths
        r'^/storage/',                # Storage paths
        r'^/public/',                 # Public paths (relative)
        r'^/uploads/',                # Uploads paths
        r'^/img/',                    # Img paths
        r'^/photo/',                  # Photo paths
        r'^/pics/',                   # Pics paths
        r'^/picture/',                # Picture paths
    ]
    
    def __init__(self):
        self.compiled_patterns = [re.compile(pattern) for pattern in self.SIZE_PATTERNS]
        self.non_public_patterns = [re.compile(pattern) for pattern in self.NON_PUBLIC_PATTERNS]
    
    def is_public_url(self, url: str) -> bool:
        """
        Kiểm tra xem URL có phải là public URL hợp lệ không
        Chỉ chấp nhận URLs bắt đầu với http:// hoặc https://
        và không phải là internal/relative URLs
        """
        if not url or not isinstance(url, str):
            return False
        
        url = url.strip()
        
        # Kiểm tra xem có bắt đầu với http:// hoặc https:// không
        if not url.startswith(('http://', 'https://')):
            return False
        
        try:
            parsed = urlparse(url)
            
            # Phải có scheme
            if not parsed.scheme:
                return False
            
            # Phải có netloc (domain)
            if not parsed.netloc:
                return False
            
            # Không chấp nhận localhost, 127.0.0.1, hoặc IP private
            netloc_lower = parsed.netloc.lower()
            if any(pattern in netloc_lower for pattern in ['localhost', '127.0.0.1', '192.168.', '10.', '172.16.', '::1']):
                return False
            
            # Kiểm tra xem có phải là relative path không
            for pattern in self.non_public_patterns:
                if pattern.search(url):
                    return False
            
            # Kiểm tra extension hợp lệ
            path_lower = parsed.path.lower()
            valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff', '.svg']
            if not any(path_lower.endswith(ext) for ext in valid_extensions):
                # Nếu không có extension, kiểm tra xem có phải là image URL với query param không
                if 'image' not in path_lower and 'img' not in path_lower:
                    # Kiểm tra query params cho image
                    query_params = parse_qs(parsed.query)
                    if not any(key in query_params for key in ['image', 'img', 'photo', 'picture', 'url']):
                        return False
            
            return True
            
        except Exception as e:
            logger.debug(f"Error checking public URL {url}: {e}")
            return False
    
    def normalize_url(self, url: str) -> str:
        """
        Chuẩn hóa URL: loại bỏ query params, hash, chuẩn hóa path
        """
        if not url or not self.is_public_url(url):
            return ""
        
        try:
            # Decode URL encoded characters
            url = unquote(url)
            
            # Parse URL
            parsed = urlparse(url)
            
            # Loại bỏ query parameters và fragment
            normalized = parsed._replace(query="", fragment="")
            
            # Chuẩn hóa path: loại bỏ các pattern kích thước
            path = normalized.path
            
            # Loại bỏ các pattern kích thước
            for pattern in self.compiled_patterns:
                path = pattern.sub('', path)
            
            # Loại bỏ số cuối cùng trước extension
            if '.' in path:
                base, ext = path.rsplit('.', 1)
                # Loại bỏ số ở cuối base (ví dụ: image-1.jpg -> image.jpg)
                base = re.sub(r'[-_]?\d+$', '', base)
                path = f"{base}.{ext}"
            
            normalized = normalized._replace(path=path)
            
            return urlunparse(normalized).lower()
            
        except Exception as e:
            logger.warning(f"Error normalizing URL {url}: {e}")
            return url.lower() if url else ""
    
    def extract_dimensions(self, url: str) -> Tuple[int, int]:
        """
        Trích xuất kích thước từ URL
        Returns: (width, height)
        """
        if not self.is_public_url(url):
            return 0, 0
            
        try:
            # Tìm pattern kích thước
            for pattern in [r'[-_](\d+)x(\d+)', r'[-_](\d+)-(\d+)']:
                match = re.search(pattern, url)
                if match:
                    return int(match.group(1)), int(match.group(2))
            
            # Tìm pattern chỉ width
            for pattern in [r'[-_](\d+)w', r'[-_]w(\d+)', r'[-_](\d+)px']:
                match = re.search(pattern, url)
                if match:
                    width = int(match.group(1)) if match.group(1) else int(match.group(2))
                    return width, 0
            
            # Tìm pattern chỉ height
            for pattern in [r'[-_](\d+)h', r'[-_]h(\d+)']:
                match = re.search(pattern, url)
                if match:
                    height = int(match.group(1)) if match.group(1) else int(match.group(2))
                    return 0, height
            
            # Tìm trong query parameters
            parsed = urlparse(url)
            query_params = parse_qs(parsed.query)
            
            if 'w' in query_params:
                width = int(query_params['w'][0])
                height = int(query_params.get('h', [0])[0])
                return width, height
            elif 'width' in query_params:
                width = int(query_params['width'][0])
                height = int(query_params.get('height', [0])[0])
                return width, height
            
            return 0, 0
            
        except Exception:
            return 0, 0
    
    def get_quality_score(self, url: str) -> int:
        """
        Đánh giá chất lượng ảnh dựa trên URL
        Score cao hơn = chất lượng tốt hơn
        """
        if not self.is_public_url(url):
            return -1000  # Rất thấp cho URL không public
        
        score = 0
        
        # Trích xuất kích thước
        width, height = self.extract_dimensions(url)
        if width > 0 and height > 0:
            score += (width * height) // 1000  # Diện tích ảnh
        
        # Kiểm tra keywords chất lượng cao
        url_lower = url.lower()
        for keyword in self.QUALITY_KEYWORDS:
            if keyword in url_lower:
                score += 100
        
        # Kiểm tra keywords chất lượng thấp
        for keyword in self.LOW_QUALITY_KEYWORDS:
            if keyword in url_lower:
                score -= 50
        
        # Ưu tiên domain chất lượng cao (CDN, image hosting)
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        for quality_domain in self.QUALITY_DOMAINS:
            if quality_domain in domain:
                score += 50
        
        # Ưu tiên ảnh có extension chất lượng cao
        if url_lower.endswith(('.png', '.webp', '.tiff')):
            score += 20
        elif url_lower.endswith('.jpg') or url_lower.endswith('.jpeg'):
            score += 10
        elif url_lower.endswith('.gif'):
            score -= 10
        
        # Ưu tiên ảnh có query parameter chất lượng cao
        query_params = parse_qs(parsed.query)
        
        if 'quality' in query_params:
            try:
                quality = int(query_params['quality'][0])
                score += quality // 10
            except:
                pass
        
        # Ưu tiên ảnh có kích thước rõ ràng
        if width > 1000 or height > 1000:
            score += 30
        
        # Ưu tiên HTTPS
        if parsed.scheme == 'https':
            score += 20
        
        # Ưu tiên URL ngắn và sạch (ít query params)
        if len(parsed.query) == 0:
            score += 10
        
        return score
    
    def filter_public_images(self, image_urls: List[str]) -> List[str]:
        """
        Lọc chỉ giữ lại các URL hình ảnh public hợp lệ
        """
        if not image_urls:
            return []
        
        public_images = []
        for url in image_urls:
            if self.is_public_url(url):
                public_images.append(url)
            else:
                logger.debug(f"Filtered out non-public image URL: {url}")
        
        logger.info(f"Filtered public images: {len(image_urls)} -> {len(public_images)}")
        return public_images
    
    def deduplicate_images(self, image_urls: List[str]) -> List[str]:
        """
        Loại bỏ hình ảnh trùng lặp từ danh sách URL
        Chỉ xử lý các URL public hợp lệ
        """
        if not image_urls:
            return []
        
        # Bước 1: Lọc chỉ lấy public URLs
        public_images = self.filter_public_images(image_urls)
        
        if not public_images:
            return []
        
        # Bước 2: Nhóm ảnh theo base URL đã chuẩn hóa
        groups: Dict[str, List[str]] = {}
        
        for url in public_images:
            normalized = self.normalize_url(url)
            if normalized:  # Chỉ xử lý nếu normalize thành công
                if normalized not in groups:
                    groups[normalized] = []
                groups[normalized].append(url)
        
        # Bước 3: Chọn ảnh tốt nhất từ mỗi nhóm
        selected_images = []
        
        for base_url, urls in groups.items():
            if len(urls) == 1:
                # Chỉ có 1 ảnh trong nhóm
                selected_images.append(urls[0])
            else:
                # Có nhiều ảnh trùng lặp, chọn ảnh tốt nhất
                best_url = self._select_best_image(urls)
                if best_url:
                    selected_images.append(best_url)
        
        # Log kết quả deduplication
        logger.info(f"Image deduplication: {len(image_urls)} total -> {len(public_images)} public -> {len(selected_images)} unique")
        
        return selected_images
    
    def _select_best_image(self, urls: List[str]) -> str:
        """
        Chọn ảnh tốt nhất từ danh sách các URL trùng lặp
        """
        if not urls:
            return ""
        
        # Tính score cho từng ảnh
        scored_urls = []
        for url in urls:
            score = self.get_quality_score(url)
            scored_urls.append((score, url))
        
        # Sắp xếp theo score (cao nhất trước)
        scored_urls.sort(reverse=True)
        
        # Log để debug
        if len(urls) > 1:
            logger.debug(f"Selecting best image from {len(urls)} duplicates:")
            for score, url in scored_urls[:3]:
                logger.debug(f"  Score {score}: {url[:80]}...")
        
        return scored_urls[0][1] if scored_urls else ""
    
    def analyze_image_group(self, image_urls: List[str]) -> Dict:
        """
        Phân tích nhóm ảnh để debug
        """
        # Lọc public images trước
        public_images = self.filter_public_images(image_urls)
        
        groups = {}
        for url in public_images:
            normalized = self.normalize_url(url)
            if normalized:
                if normalized not in groups:
                    groups[normalized] = []
                groups[normalized].append(url)
        
        analysis = {
            "total_images": len(image_urls),
            "public_images": len(public_images),
            "unique_groups": len(groups),
            "groups": {}
        }
        
        for base_url, urls in groups.items():
            analysis["groups"][base_url] = {
                "count": len(urls),
                "urls": urls[:3],  # Chỉ hiển thị 3 URL đầu
                "best_image": self._select_best_image(urls) if urls else ""
            }
        
        return analysis
    
    def get_best_images(self, image_urls: List[str], max_images: int = 5) -> List[str]:
        """
        Lấy danh sách ảnh tốt nhất từ các URL
        """
        # Lọc và deduplicate
        deduplicated = self.deduplicate_images(image_urls)
        
        if not deduplicated:
            return []
        
        # Tính score cho từng ảnh
        scored_images = []
        for url in deduplicated:
            score = self.get_quality_score(url)
            scored_images.append((score, url))
        
        # Sắp xếp theo score
        scored_images.sort(reverse=True)
        
        # Lấy top N ảnh
        best_images = [url for _, url in scored_images[:max_images]]
        
        logger.info(f"Selected {len(best_images)} best images from {len(image_urls)} total")
        
        return best_images