# services/ui_config/config_service.py

from typing import List
from .config import BotConfig, LanguageConfig, ContentTypeConfig, ToneConfig

class ConfigService:
    """Service cung cấp cấu hình thống nhất cho toàn bộ ứng dụng"""
    
    # Config từ bot_catalog.py
    BOTS = {
        "GPT-4.1": BotConfig(id="bot-2016", name="GPT-4.1"),
        "Vietnam-ocr-vlm": BotConfig(id="bot-2004", name="Vietnam-ocr-vlm"),
        "Gemini-2.5-flash": BotConfig(id="bot-2006", name="Gemini-2.5-flash")
    }
    
    DEFAULT_BOT = BOTS["GPT-4.1"]
    
    LANGUAGES = {
        "Tiếng Trung": LanguageConfig(id="1", name="Tiếng Trung"),
        "Tiếng Anh": LanguageConfig(id="2", name="Tiếng Anh"),
        "Tiếng Nhật": LanguageConfig(id="3", name="Tiếng Nhật"),
        "Tiếng Thái": LanguageConfig(id="4", name="Tiếng Thái"),
        "Tiếng Việt": LanguageConfig(id="5", name="Tiếng Việt")
    }
    
    DEFAULT_LANGUAGE = LANGUAGES["Tiếng Việt"]
    
    # Config từ content_catalog.py
    CONTENT_TYPES = {
        "Blog": ContentTypeConfig(id="blog", name="Blog"),
        "Tin tức": ContentTypeConfig(id="news", name="Tin tức"),
        "Review": ContentTypeConfig(id="review", name="Review"),
        "Hướng dẫn": ContentTypeConfig(id="guide", name="Hướng dẫn"),
        "Giới thiệu sản phẩm": ContentTypeConfig(id="product", name="Giới thiệu sản phẩm"),
        "Landing Page": ContentTypeConfig(id="landing", name="Landing Page"),
        "So sánh sản phẩm": ContentTypeConfig(id="toplist", name="So sánh sản phẩm")
    }
    
    WRITING_TONES = {
        "Chuyên nghiệp": ToneConfig(id="chuyên nghiệp", name="Chuyên nghiệp", description="chuyên nghiệp, khách quan"),
        "Thân thiện": ToneConfig(id="thân thiện", name="Thân thiện", description="thân thiện, gần gũi"),
        "Trang trọng": ToneConfig(id="trang trọng", name="Trang trọng", description="trang trọng, học thuật"),
        "Sáng tạo": ToneConfig(id="sáng tạo", name="Sáng tạo", description="sáng tạo, thu hút"),
        "Thuyết phục": ToneConfig(id="thuyết phục", name="Thuyết phục", description="thuyết phục, marketing"),
        "Trung lập": ToneConfig(id="trung lập", name="Trung lập", description="trung lập, khách quan"),
        "Truyền cảm hứng": ToneConfig(id="truyền cảm hứng", name="Truyền cảm hứng", description="truyền cảm hứng, tích cực")
    }
    
    @classmethod
    def get_bot_by_name(cls, bot_name: str) -> BotConfig:
        return cls.BOTS.get(bot_name, cls.DEFAULT_BOT)
    
    @classmethod
    def get_language_by_name(cls, language_name: str) -> LanguageConfig:
        return cls.LANGUAGES.get(language_name, cls.DEFAULT_LANGUAGE)
    
    @classmethod
    def get_tone_by_name(cls, tone_name: str) -> ToneConfig:
        return cls.WRITING_TONES.get(tone_name, cls.WRITING_TONES["Chuyên nghiệp"])
    
    @classmethod
    def get_content_type_by_name(cls, content_type_name: str) -> ContentTypeConfig:
        return cls.CONTENT_TYPES.get(content_type_name, cls.CONTENT_TYPES["Blog"])
    
    @classmethod
    def get_all_bot_names(cls) -> List[str]:
        return list(cls.BOTS.keys())
    
    @classmethod
    def get_all_language_names(cls) -> List[str]:
        return list(cls.LANGUAGES.keys())
    
    @classmethod
    def get_all_content_type_names(cls) -> List[str]:
        return list(cls.CONTENT_TYPES.keys())
    
    @classmethod
    def get_all_tone_names(cls) -> List[str]:
        return list(cls.WRITING_TONES.keys())

if __name__ == '__main__':
    config = ConfigService()
    print(config.DEFAULT_BOT.id)