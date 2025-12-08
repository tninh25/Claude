# test/agent/scorer

import re
import math

from bs4 import BeautifulSoup
from dataclasses import dataclass   
from typing import Dict, List, Any

@dataclass
class Section:
    """Dataclass đại diện cho một section trong bài viết"""
    heading: str
    level  : str    # 'h1', 'h2', 'h3', 'intro', 'conclusion'
    text   : str
    word_count: int

@dataclass
class KeywordCheck:
    """Dataclass cho kết quả kiểm tra keyword"""
    keyword: str
    in_title: bool
    in_meta: bool
    in_intro: bool
    density_percent: float
    in_headings: List[str]
    stuffing: bool

@dataclass
class Issue:
    """Dataclass cho các lỗi phát hiện"""

class ArticleParser:
    """Class chính để parse và trích xuất thoogn tin từ HTML"""
    def __init__(self, html_content: str):
        self.soup = BeautifulSoup(html_content, 'html.parser')
        self.clean_text = ""
        self.sections: List[Section] = []
        self.intro = ""
        self.conclusion = ""

    def get_clean_text(self) -> str:
        """Lấy văn bản sạch từ HTML"""
        # Remove script và style tags
        for script in self.soup(["script", "style"]):
            script.decompose()
        
        text = self.soup.get_text(separator='/n')
        # Clean up multiple newlines and spaces
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '/n'.join(chunk for chunk in chunks if chunk)
        self.clean_text = text
        return text
    
    def extract_sections(self) -> List[Section]:
        """Trích xuất các section từ HTMl theo heading"""
        sections = []
        
