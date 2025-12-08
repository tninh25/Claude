# services/crawl/crawler_config.py

from typing import Any, Dict

class CrawlConfig:
    def __init__(self, content_threshold: int, max_content_length: int, max_images: int, cache_mode: Any = None):
        self.content_threshold = content_threshold
        self.max_content_length = max_content_length
        self.max_images = max_images
        self.cache_mode = cache_mode

    @classmethod
    def from_settings(cls, settings: Dict[str, Any]):
        return cls(
            content_threshold=settings.get("content_threshold", 50),
            max_content_length=settings.get("max_content_length", 2000),
            max_images=settings.get("max_images", 5),
            cache_mode=settings.get("cache_mode", None)
        )
