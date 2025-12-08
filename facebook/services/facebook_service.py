import requests
import logging
from typing import Optional, Dict, Any, List
from models.facebook import FacebookPostCreate, FacebookPostUpdate, FacebookPostResponse, FacebookPostListResponse

logger = logging.getLogger(__name__)

class FacebookService:
    def __init__(self, page_access_token: str, page_id: str):
        self.page_access_token = page_access_token
        self.page_id = page_id
        self.base_url = "https://graph.facebook.com/v19.0"
        
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Thực hiện request đến Facebook Graph API"""
        url = f"{self.base_url}/{endpoint}"
        
        # Thêm access token vào params
        if params is None:
            params = {}
        params['access_token'] = self.page_access_token
        
        try:
            if method.upper() == 'GET':
                response = requests.get(url, params=params, timeout=30)
            elif method.upper() == 'POST':
                response = requests.post(url, params=params, json=data, timeout=30)
            elif method.upper() == 'DELETE':
                response = requests.delete(url, params=params, timeout=30)
            else:
                raise ValueError(f"Method {method} không được hỗ trợ")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Lỗi khi gọi Facebook API: {str(e)}")
            raise Exception(f"Lỗi kết nối đến Facebook: {str(e)}")
        except Exception as e:
            logger.error(f"Lỗi không xác định: {str(e)}")
            raise
    
    def create_post(self, post_data: FacebookPostCreate) -> FacebookPostResponse:
        """
        Tạo bài viết mới trên Facebook Page
        """
        endpoint = f"{self.page_id}/feed"
        
        # Chuẩn bị data cho Facebook API
        data = {}
        if post_data.message:
            data['message'] = post_data.message
        if post_data.link:
            data['link'] = post_data.link
        if post_data.scheduled_publish_time:
            data['scheduled_publish_time'] = post_data.scheduled_publish_time
            data['published'] = False  # Bài viết lên lịch phải là unpublished
            
        result = self._make_request('POST', endpoint, data=data)
        
        # Lấy thông tin chi tiết của bài viết vừa tạo
        post_details = self._make_request('GET', result['id'], params={
            'fields': 'id,message,created_time,updated_time,permalink_url'
        })
        
        return FacebookPostResponse(**post_details)
    
    def get_post(self, post_id: str) -> FacebookPostResponse:
        """
        Lấy thông tin chi tiết của một bài viết
        """
        endpoint = post_id
        params = {
            'fields': 'id,message,created_time,updated_time,permalink_url'
        }
        
        result = self._make_request('GET', endpoint, params=params)
        return FacebookPostResponse(**result)
    
    def update_post(self, post_id: str, update_data: FacebookPostUpdate) -> FacebookPostResponse:
        """
        Cập nhật nội dung bài viết
        """
        endpoint = post_id
        
        data = {}
        if update_data.message:
            data['message'] = update_data.message
            
        result = self._make_request('POST', endpoint, data=data)
        
        if result.get('success'):
            # Lấy thông tin mới sau khi cập nhật
            return self.get_post(post_id)
        else:
            raise Exception("Cập nhật bài viết thất bại")
    
    def delete_post(self, post_id: str) -> Dict[str, Any]:
        """
        Xóa bài viết
        """
        endpoint = post_id
        result = self._make_request('DELETE', endpoint)
        
        return {
            "success": result.get('success', False),
            "post_id": post_id,
            "message": "Xóa bài viết thành công" if result.get('success') else "Xóa bài viết thất bại"
        }
    
    def get_posts(self, limit: int = 10) -> FacebookPostListResponse:
        """
        Lấy danh sách bài viết từ page
        """
        endpoint = f"{self.page_id}/posts"
        params = {
            'fields': 'id,message,created_time,updated_time,permalink_url',
            'limit': limit
        }
        
        result = self._make_request('GET', endpoint, params=params)
        posts = [FacebookPostResponse(**post) for post in result.get('data', [])]
        
        return FacebookPostListResponse(
            posts=posts,
            total=len(posts)
        )