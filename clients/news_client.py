# clients/news_client.py

import requests
import logging
from typing import Dict, Any, List
from utils.config_loader import config

logger = logging.getLogger(__name__)

class GoogleSearchClient:
    """Google Search Custome"""
    def __init__(self):
        search_config = config.get('search')
        self.api_key  = search_config['google_api_key']
        self.base_url = search_config['search_url']
        self.search_engine_id = search_config['search_engine_id']

        # Log config
        logger.info(f"Search client initialized with API key: {self.api_key[:10]}..")
        logger.info(f"Search engine ID: {self.search_engine_id}")

    def search(self, query: str, num_results: int = 10) -> Dict[str, Any]:
        params = {
            "key": self.api_key,
            "cx" : self.search_engine_id,
            "q"  : query,
            "num": num_results
        }
        try:
            logger.info(f"Searching for: {query}")
            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            if "items" not in data:
                logger.warning(f"No items found in search results for query: {query}")
                return {
                    "success": False,
                    "message": "No search results found",
                    "results": []
                }

            results = []
            for item in data["items"]:
                results.append({
                    "title": item.get("title"),
                    "link" : item.get("link"),
                    "snippet": item.get("snippet")
                })

            logger.info(f"Search successful, found {len(results)} results")
            return {
                "success": True,
                "query": query,
                "total_results": len(results),
                "results": results
            }
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Search request failed: {str(e)}")
            return {
                "success": False,
                "message": f"Search connection error: {str(e)}",
                "results": []
            }

        except Exception as e:
            logger.error(f"Unexpected error in search: {str(e)}")
            return {
                "success": False,
                "message": f"Search error: {str(e)}",
                "results": []
            }

    def search_images(self, query: str, num_results: int = 10) -> List[Dict]:
        """Tìm kiếm hình ảnh"""
        params = {
            "key": self.api_key,
            "cx" : self.search_engine_id,
            "q"  : query,
            "searchType": "image",
            "num": min(num_results, 10)
        }
        try:
            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            if "items" not in data:
                return []
            
            images = []
            for item in data['items']:
                images.append({
                    "url": item.get("link"),
                    "thumbnail": item.get("image", {}).get("thumbnailLink"),
                    "title": item.get("title"),
                    "source": item.get("displayLink"),
                    "size": f"{item.get('image', {}).get('width')}x{item.get('image', {}).get('height')}"
                })
            
            return images
        
        except Exception as e:
            print(f"Lỗi tìm kiếm: {e}")
            return []
        
if __name__ == '__main__':
    google_search_client = GoogleSearchClient()

    query = "Tin tức về chatgpt 5"

    print(google_search_client.search(query))