import requests
import json
import base64
from datetime import datetime
from typing import Optional, Dict, Any, List
import mimetypes
import os


class WordPressClient:
    """Client để kết nối và tương tác với WordPress REST API"""
    
    def __init__(self, site_url: str, username: str, password: str):
        """
        Khởi tạo WordPress client
        
        Args:
            site_url: URL của trang WordPress (ví dụ: https://example.com)
            username: Tên đăng nhập WordPress
            password: Mật khẩu ứng dụng WordPress (Application Password)
                     Hoặc mật khẩu tài khoản nếu dùng Basic Auth
        """
        self.site_url = site_url.rstrip('/')
        self.api_base = f"{self.site_url}/wp-json/wp/v2"
        self.auth = (username, password)
        
        # Tạo session để tái sử dụng kết nối
        self.session = requests.Session()
        self.session.auth = self.auth
        
        # Headers mặc định
        self.session.headers.update({
            'User-Agent': 'WordPress-Python-Client/1.0',
            'Content-Type': 'application/json'
        })
        
    def test_connection(self) -> bool:
        """Kiểm tra kết nối đến WordPress API"""
        try:
            response = self.session.get(f"{self.api_base}/posts", params={'per_page': 1})
            response.raise_for_status()
            print("✅ Kết nối WordPress API thành công!")
            return True
        except requests.exceptions.RequestException as e:
            print(f"❌ Lỗi kết nối: {e}")
            return False
    
    def create_post(
        self,
        title: str,
        content: str,
        status: str = 'draft',
        categories: Optional[List[int]] = None,
        tags: Optional[List[int]] = None,
        excerpt: Optional[str] = None,
        featured_media: Optional[int] = None,
        slug: Optional[str] = None,
        meta_data: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Tạo bài viết mới trên WordPress
        
        Args:
            title: Tiêu đề bài viết
            content: Nội dung bài viết (HTML)
            status: Trạng thái ('draft', 'publish', 'pending', 'private')
            categories: Danh sách ID chuyên mục
            tags: Danh sách ID thẻ
            excerpt: Đoạn trích ngắn
            featured_media: ID của ảnh đại diện
            slug: Đường dẫn tùy chỉnh
            meta_data: Dữ liệu meta tùy chỉnh
            
        Returns:
            Dictionary chứa thông tin bài viết đã tạo hoặc None nếu có lỗi
        """
        
        post_data = {
            'title': title,
            'content': content,
            'status': status,
            'date': datetime.now().isoformat()
        }
        
        # Thêm các trường tùy chọn nếu có
        if excerpt:
            post_data['excerpt'] = excerpt
            
        if categories:
            post_data['categories'] = categories
            
        if tags:
            post_data['tags'] = tags
            
        if featured_media:
            post_data['featured_media'] = featured_media
            
        if slug:
            post_data['slug'] = slug
            
        if meta_data:
            post_data['meta'] = meta_data
        
        try:
            print(f"📝 Đang đăng bài: {title}")
            response = self.session.post(f"{self.api_base}/posts", json=post_data)
            response.raise_for_status()
            
            result = response.json()
            print(f"✅ Đã tạo bài viết thành công! ID: {result['id']}")
            print(f"🔗 Xem tại: {result['link']}")
            
            return result
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Lỗi khi tạo bài viết: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"📋 Chi tiết lỗi: {e.response.text}")
            return None
    
    def upload_media(
        self,
        file_path: str,
        title: Optional[str] = None,
        alt_text: Optional[str] = None,
        caption: Optional[str] = None,
        description: Optional[str] = None
    ) -> Optional[int]:
        """
        Upload file media lên WordPress
        
        Args:
            file_path: Đường dẫn đến file cần upload
            title: Tiêu đề media
            alt_text: Văn bản thay thế
            caption: Chú thích
            description: Mô tả
            
        Returns:
            ID của media đã upload hoặc None nếu có lỗi
        """
        
        if not os.path.exists(file_path):
            print(f"❌ File không tồn tại: {file_path}")
            return None
        
        # Xác định content type
        mime_type, _ = mimetypes.guess_type(file_path)
        if not mime_type:
            mime_type = 'application/octet-stream'
        
        # Đọc file
        try:
            with open(file_path, 'rb') as file:
                file_data = file.read()
        except IOError as e:
            print(f"❌ Lỗi đọc file: {e}")
            return None
        
        # Lấy tên file
        filename = os.path.basename(file_path)
        
        # Chuẩn bị headers cho upload
        headers = self.session.headers.copy()
        headers['Content-Disposition'] = f'attachment; filename={filename}'
        headers['Content-Type'] = mime_type
        
        # Tạm thời xóa auth header để dùng Basic Auth
        session_without_auth = requests.Session()
        session_without_auth.auth = self.auth
        session_without_auth.headers.update(headers)
        
        try:
            print(f"📤 Đang upload media: {filename}")
            response = session_without_auth.post(
                f"{self.api_base}/media",
                data=file_data,
                headers=headers
            )
            response.raise_for_status()
            
            media_data = response.json()
            media_id = media_data['id']
            
            # Cập nhật thông tin media nếu có
            if any([title, alt_text, caption, description]):
                update_data = {}
                if title:
                    update_data['title'] = {'raw': title}
                if caption:
                    update_data['caption'] = {'raw': caption}
                if description:
                    update_data['description'] = {'raw': description}
                if alt_text:
                    update_data['alt_text'] = alt_text
                
                if update_data:
                    update_response = self.session.post(
                        f"{self.api_base}/media/{media_id}",
                        json=update_data
                    )
                    update_response.raise_for_status()
            
            print(f"✅ Upload media thành công! ID: {media_id}")
            return media_id
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Lỗi upload media: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"📋 Chi tiết lỗi: {e.response.text}")
            return None
    
    def get_categories(self) -> List[Dict[str, Any]]:
        """Lấy danh sách chuyên mục"""
        try:
            response = self.session.get(f"{self.api_base}/categories", params={'per_page': 100})
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Lỗi lấy danh sách chuyên mục: {e}")
            return []
    
    def get_tags(self) -> List[Dict[str, Any]]:
        """Lấy danh sách thẻ"""
        try:
            response = self.session.get(f"{self.api_base}/tags", params={'per_page': 100})
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Lỗi lấy danh sách thẻ: {e}")
            return []
    
    def __del__(self):
        """Đóng session khi đối tượng bị hủy"""
        if hasattr(self, 'session'):
            self.session.close()


# ====================== VÍ DỤ SỬ DỤNG ======================

def example_usage():
    """Ví dụ cách sử dụng WordPressClient"""
    
    # Cấu hình kết nối
    WORDPRESS_URL = "https://your-wordpress-site.com"
    USERNAME = "your_username"
    
    # QUAN TRỌNG: Sử dụng Application Password thay vì mật khẩu tài khoản
    # Tạo tại: Users → Profile → Application Passwords
    PASSWORD = "your_application_password"
    
    # Khởi tạo client
    wp_client = WordPressClient(WORDPRESS_URL, USERNAME, PASSWORD)
    
    # Kiểm tra kết nối
    if not wp_client.test_connection():
        print("Không thể kết nối đến WordPress. Vui lòng kiểm tra thông tin đăng nhập.")
        return
    
    # Ví dụ 1: Tạo bài viết cơ bản
    print("\n" + "="*50)
    print("VÍ DỤ 1: Tạo bài viết cơ bản")
    print("="*50)
    
    post_content = """
    <h2>Đây là tiêu đề phụ</h2>
    
    <p>Đây là đoạn văn bản <strong>được định dạng</strong> trong bài viết.</p>
    
    <ul>
        <li>Mục danh sách 1</li>
        <li>Mục danh sách 2</li>
        <li>Mục danh sách 3</li>
    </ul>
    
    <p>Đoạn văn kết thúc bài viết.</p>
    """
    
    post_result = wp_client.create_post(
        title="Bài viết được tạo từ Python",
        content=post_content,
        status="draft",  # Có thể đổi thành "publish" để đăng ngay
        excerpt="Đây là đoạn trích ngắn của bài viết được tạo tự động từ Python.",
        slug="bai-viet-tu-python"
    )
    
    # Ví dụ 2: Upload ảnh và tạo bài viết có ảnh đại diện
    print("\n" + "="*50)
    print("VÍ DỤ 2: Upload ảnh và tạo bài viết có ảnh đại diện")
    print("="*50)
    
    # Upload ảnh (thay đường dẫn bằng file thực tế)
    image_path = "path/to/your/image.jpg"
    media_id = None
    
    if os.path.exists(image_path):
        media_id = wp_client.upload_media(
            file_path=image_path,
            title="Ảnh minh họa bài viết",
            alt_text="Mô tả ảnh minh họa",
            caption="Chú thích cho ảnh"
        )
    else:
        print(f"⚠️ File ảnh không tồn tại: {image_path}")
        print("📝 Sử dụng bài viết không có ảnh đại diện...")
    
    # Tạo bài viết với ảnh đại diện
    if media_id:
        post_with_image = wp_client.create_post(
            title="Bài viết có ảnh đại diện",
            content="<p>Bài viết này có ảnh đại diện được upload từ Python.</p>",
            status="draft",
            featured_media=media_id
        )
    
    # Ví dụ 3: Lấy danh sách chuyên mục và thẻ
    print("\n" + "="*50)
    print("VÍ DỤ 3: Lấy danh sách chuyên mục và thẻ")
    print("="*50)
    
    categories = wp_client.get_categories()
    print(f"📂 Tìm thấy {len(categories)} chuyên mục:")
    for cat in categories[:5]:  # Hiển thị 5 chuyên mục đầu tiên
        print(f"  - {cat['name']} (ID: {cat['id']})")
    
    tags = wp_client.get_tags()
    print(f"🏷️ Tìm thấy {len(tags)} thẻ:")
    for tag in tags[:5]:  # Hiển thị 5 thẻ đầu tiên
        print(f"  - {tag['name']} (ID: {tag['id']})")
    
    print("\n✨ Hoàn tất ví dụ!")


# ====================== HÀM CHÍNH ======================

def main():
    """Hàm chính với giao diện đơn giản"""
    
    print("🤖 WORDPRESS POST PUBLISHER")
    print("=" * 50)
    
    # Nhập thông tin từ người dùng
    print("\n🔧 Vui lòng cung cấp thông tin kết nối:")
    
    site_url = input("URL WordPress (ví dụ: https://example.com): ").strip()
    username = input("Tên đăng nhập: ").strip()
    password = input("Mật khẩu ứng dụng (Application Password): ").strip()
    
    # Khởi tạo client
    wp_client = WordPressClient(site_url, username, password)
    
    # Kiểm tra kết nối
    if not wp_client.test_connection():
        print("❌ Không thể kết nối. Vui lòng kiểm tra lại thông tin.")
        return
    
    # Nhập thông tin bài viết
    print("\n📝 NHẬP THÔNG TIN BÀI VIẾT:")
    title = input("Tiêu đề bài viết: ").strip()
    
    print("\nNhập nội dung bài viết (HTML, nhập 'END' trên một dòng mới để kết thúc):")
    content_lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        content_lines.append(line)
    
    content = "\n".join(content_lines)
    
    # Tùy chọn
    print("\n⚙️ TÙY CHỌN (bấm Enter để bỏ qua):")
    excerpt = input("Đoạn trích ngắn: ").strip() or None
    status = input("Trạng thái (draft/publish/pending/private, mặc định: draft): ").strip() or "draft"
    slug = input("Đường dẫn tùy chỉnh: ").strip() or None
    
    # Tạo bài viết
    print("\n⏳ Đang đăng bài...")
    result = wp_client.create_post(
        title=title,
        content=content,
        status=status,
        excerpt=excerpt,
        slug=slug
    )
    
    if result:
        print(f"\n🎉 Bài viết đã được tạo thành công!")
        print(f"📎 ID: {result['id']}")
        print(f"🔗 URL: {result.get('link', 'N/A')}")
        print(f"📊 Trạng thái: {result.get('status', 'N/A')}")
    else:
        print("\n😞 Có lỗi xảy ra khi đăng bài.")


if __name__ == "__main__":
    # Chạy ví dụ mẫu (bỏ comment dòng dưới để chạy)
    # example_usage()
    
    # Hoặc chạy chương trình chính với giao diện nhập liệu
    main()