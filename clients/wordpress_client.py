# clients/wordpress_client.py

import requests
from utils.config_loader import config
from requests.auth import HTTPBasicAuth

class WordPressClient:
    """Client kết nối Wordpress"""
    def __init__(self):
        wordpress_config = config.get("wordpress")
        # Lấy base URL (chỉ domain, không có /wp-json/wp/v2)
        self.base_url = wordpress_config["api_url"].rstrip('/')
        self.username = wordpress_config["username"]
        self.password = wordpress_config["application_password"]
        self.session = None
    
    def connect(self):
        """Kết nối và tạo session"""
        self.auth = HTTPBasicAuth(self.username, self.password)
        
        self.session = requests.Session()
        self.session.auth = self.auth
        self.session.headers.update({
            "User-Agent": "WordPressAPI/1.0",
            "Accept": "application/json",
            "Content-Type": "application/json"
        })
        
        print(f"✅ Connected to WordPress: {self.base_url}")
        
        # Test connection
        try:
            test_url = f"{self.base_url}/wp-json/"
            response = self.session.get(test_url, timeout=10)
            if response.status_code == 200:
                print("✅ WordPress REST API is ready")
                # In thông tin API
                api_info = response.json()
                print(f"   WordPress version: {api_info.get('version', 'unknown')}")
                print(f"   API namespace: {api_info.get('namespace', 'unknown')}")
            else:
                print(f"⚠️  API test returned: {response.status_code}")
        except Exception as e:
            print(f"❌ API test failed: {e}")
    
    def __del__(self):
        """Đảm bảo đóng session khi object bị hủy"""
        if hasattr(self, 'session') and self.session:
            self.session.close()