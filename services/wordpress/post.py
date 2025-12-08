# services/wordpress/post.py

# services/wordpress/post.py

import requests
from typing import Dict, Any
from clients.wordpress_client import WordPressClient
from models.wordpress.post import ArticleCreate

class WordPressPostService:
    """Service xử lý logic publish bài lên WordPress"""
    
    def __init__(self, client: WordPressClient):
        self.client = client
    
    def create_post(self, post: ArticleCreate) -> Dict[str, Any]:
        """
        Tạo bài viết mới trên WordPress
        """
        # Endpoint đúng: /wp-json/wp/v2/posts
        # Base URL đã có trong client.base_url
        endpoint = f"{self.client.base_url}/wp-json/wp/v2/posts"
        
        print(f"📤 Creating post at: {endpoint}")
        
        # Chuẩn bị payload
        payload = {
            "title": post.title,
            "content": post.content,
            "status": post.status,
        }
        
        # Thêm các trường optional
        if post.slug:
            payload["slug"] = post.slug
            
        if post.excerpt:
            payload["excerpt"] = post.excerpt
        
        # Xử lý categories - WordPress cần ID số, không phải string
        if post.categories:
            if isinstance(post.categories, str):
                try:
                    payload["categories"] = [int(post.categories)]
                except ValueError:
                    print(f"⚠️  Warning: Category should be numeric ID, got '{post.categories}'")
            elif isinstance(post.categories, list):
                # Convert string numbers to integers
                category_ids = []
                for cat in post.categories:
                    try:
                        category_ids.append(int(cat))
                    except ValueError:
                        print(f"⚠️  Warning: Skipping non-numeric category '{cat}'")
                if category_ids:
                    payload["categories"] = category_ids
        
        # Xử lý tags - WordPress cần ID số, không phải string
        if post.tags:
            if isinstance(post.tags, str):
                try:
                    payload["tags"] = [int(post.tags)]
                except ValueError:
                    print(f"⚠️  Warning: Tag should be numeric ID, got '{post.tags}'")
            elif isinstance(post.tags, list):
                tag_ids = []
                for tag in post.tags:
                    try:
                        tag_ids.append(int(tag))
                    except ValueError:
                        print(f"⚠️  Warning: Skipping non-numeric tag '{tag}'")
                if tag_ids:
                    payload["tags"] = tag_ids
        
        # Featured image - WordPress cần media ID, không phải URL
        # Để upload ảnh, cần xử lý riêng
        # if post.featured_image_url:
        #     media_id = self._upload_image(post.featured_image_url)
        #     if media_id:
        #         payload["featured_media"] = media_id
        
        print(f"📦 Payload: {payload}")
        
        try:
            # Gửi request
            response = self.client.session.post(
                endpoint,
                json=payload,
                timeout=30
            )
            
            print(f"📡 Response status: {response.status_code}")
            
            if response.status_code in [200, 201]:
                result = response.json()
                print(f"✅ Post created successfully!")
                print(f"   ID: {result.get('id')}")
                print(f"   Title: {result.get('title', {}).get('rendered', 'N/A')}")
                print(f"   Link: {result.get('link', 'N/A')}")
                return result
            else:
                error_detail = response.json() if response.content else response.text
                error_msg = f"WordPress API error {response.status_code}: {error_detail}"
                print(f"❌ {error_msg}")
                raise ValueError(error_msg)
                
        except requests.exceptions.RequestException as e:
            error_msg = f"Connection error: {str(e)}"
            print(f"❌ {error_msg}")
            raise requests.exceptions.RequestException(error_msg) from e
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            print(f"❌ {error_msg}")
            raise Exception(error_msg) from e

if __name__ == '__main__':
    # Khởi tạo
    client = WordPressClient()
    client.connect()
    service = WordPressPostService(client)

    # Tạo bài viết
    post_data = ArticleCreate(
        title="Tiêu đề bài viết",
        content="Nội dung bài viết",
        status="draft",
        categories=["1", "2"],
        tags=["tag1", "tag2"]
    )

    result = service.create_post(post_data)
    print(result) 