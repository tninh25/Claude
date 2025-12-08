"""
Module Parser và SEO Analysis cho AI Writer
Author: Senior Python Engineer
Date: 2024
"""

from bs4 import BeautifulSoup
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import math


@dataclass
class Section:
    """Dataclass đại diện cho một section trong bài viết"""
    heading: str
    level: str  # 'h1', 'h2', 'h3', 'intro', 'conclusion'
    text: str
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
    type: str
    detail: str


class ArticleParser:
    """Class chính để parse và trích xuất thông tin từ HTML"""
    
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
        """Trích xuất các section từ HTML theo heading"""
        sections = []
        
        # Tìm tất cả các heading và nội dung liên quan
        headings = self.soup.find_all(['h1', 'h2', 'h3'])
        
        for heading in headings:
            heading_text = heading.get_text().strip()
            level = heading.name
            
            # Tìm nội dung section (từ heading hiện tại đến heading tiếp theo)
            content_parts = []
            next_element = heading.next_sibling
            
            while next_element and (not hasattr(next_element, 'name') or 
                                  next_element.name not in ['h1', 'h2', 'h3']):
                if hasattr(next_element, 'get_text'):
                    text = next_element.get_text().strip()
                    if text:
                        content_parts.append(text)
                next_element = next_element.next_sibling
            
            section_text = ' '.join(content_parts)
            word_count = len(section_text.split())
            
            sections.append(Section(
                heading=heading_text,
                level=level,
                text=section_text,
                word_count=word_count
            ))
        
        self.sections = sections
        return sections
    
    def extract_intro_and_conclusion(self) -> Dict[str, str]:
        """Trích xuất phần giới thiệu và kết luận"""
        # Giới thiệu: đoạn văn đầu tiên sau H1 hoặc đầu bài viết
        first_paragraph = self.soup.find('p')
        self.intro = first_paragraph.get_text().strip() if first_paragraph else ""
        
        # Kết luận: tìm các từ khóa kết luận trong đoạn cuối
        conclusion_keywords = ['kết luận', 'tổng kết', 'như vậy', 'tóm lại']
        all_paragraphs = self.soup.find_all('p')
        
        for paragraph in reversed(all_paragraphs):
            text = paragraph.get_text().lower()
            if any(keyword in text for keyword in conclusion_keywords):
                self.conclusion = paragraph.get_text().strip()
                break
        else:
            # Nếu không tìm thấy, lấy đoạn cuối cùng
            self.conclusion = all_paragraphs[-1].get_text().strip() if all_paragraphs else ""
        
        return {
            "intro": self.intro,
            "conclusion": self.conclusion
        }
    
    def get_all_headings(self) -> Dict[str, List[str]]:
        """Lấy tất cả headings theo level"""
        return {
            'h1': [h.get_text().strip() for h in self.soup.find_all('h1')],
            'h2': [h.get_text().strip() for h in self.soup.find_all('h2')],
            'h3': [h.get_text().strip() for h in self.soup.find_all('h3')]
        }


class SEORuleChecker:
    """Class thực hiện các kiểm tra SEO rule-based"""
    
    def __init__(self, parser: ArticleParser, title: str, meta: str, keywords: List[str]):
        self.parser = parser
        self.title = title
        self.meta = meta
        self.keywords = keywords
        self.clean_text = parser.get_clean_text()
        self.word_count = len(self.clean_text.split())
        
    def check_structure(self) -> List[Issue]:
        """Kiểm tra cấu trúc bài viết"""
        issues = []
        headings = self.parser.get_all_headings()
        
        # Kiểm tra H1
        if not headings['h1']:
            issues.append(Issue("missing_h1", "Bài viết thiếu thẻ H1"))
        elif len(headings['h1']) > 1:
            issues.append(Issue("multiple_h1", f"Có {len(headings['h1'])} thẻ H1"))
        
        # Kiểm tra số lượng H2, H3
        num_h2 = len(headings['h2'])
        num_h3 = len(headings['h3'])
        
        if num_h2 < 2:
            issues.append(Issue("few_h2", f"Chỉ có {num_h2} thẻ H2"))
        if num_h3 > 10:  # Ngưỡng tùy chỉnh
            issues.append(Issue("too_many_h3", f"Có {num_h3} thẻ H3"))
        
        # Kiểm tra kết luận
        if not self.parser.conclusion:
            issues.append(Issue("missing_conclusion", "Không tìm thấy phần kết luận"))
        
        # Kiểm tra độ dài đoạn văn
        paragraphs = self.parser.soup.find_all('p')
        for i, p in enumerate(paragraphs):
            text = p.get_text().strip()
            word_count = len(text.split())
            if word_count > 200:
                issues.append(Issue("paragraph_too_long", 
                                  f"Đoạn văn #{i+1} có {word_count} từ"))
        
        # Kiểm tra độ dài câu
        sentences = re.split(r'[.!?]+', self.clean_text)
        for i, sentence in enumerate(sentences):
            word_count = len(sentence.strip().split())
            if word_count > 25:
                issues.append(Issue("sentence_too_long",
                                  f"Câu #{i+1} có {word_count} từ"))
        
        return issues
    
    def check_keywords(self) -> List[KeywordCheck]:
        """Kiểm tra từ khóa"""
        results = []
        clean_text_lower = self.clean_text.lower()
        title_lower = self.title.lower()
        meta_lower = self.meta.lower()
        intro_lower = self.parser.intro.lower()
        
        headings = self.parser.get_all_headings()
        all_headings_text = ' '.join(headings['h1'] + headings['h2'] + headings['h3']).lower()
        
        for keyword in self.keywords:
            keyword_lower = keyword.lower()
            
            # Kiểm tra sự xuất hiện
            in_title = keyword_lower in title_lower
            in_meta = keyword_lower in meta_lower
            in_intro = keyword_lower in intro_lower
            
            # Tính density
            keyword_count = clean_text_lower.count(keyword_lower)
            density_percent = (keyword_count / max(1, self.word_count)) * 100
            
            # Kiểm tra trong headings
            in_headings = []
            for level, heading_list in headings.items():
                for i, heading in enumerate(heading_list):
                    if keyword_lower in heading.lower():
                        in_headings.append(f"{level.upper()} #{i+1}")
            
            # Kiểm tra keyword stuffing (density quá cao)
            stuffing = density_percent > 3.0  # Ngưỡng 3%
            
            results.append(KeywordCheck(
                keyword=keyword,
                in_title=in_title,
                in_meta=in_meta,
                in_intro=in_intro,
                density_percent=round(density_percent, 2),
                in_headings=in_headings,
                stuffing=stuffing
            ))
        
        return results
    
    def check_lengths(self) -> Dict[str, Any]:
        """Kiểm tra độ dài các phần"""
        return {
            "title_length": len(self.title),
            "meta_length": len(self.meta),
            "intro_length": len(self.parser.intro.split()),
            "total_word_count": self.word_count
        }
    
    def check_html_issues(self) -> List[Issue]:
        """Kiểm tra các vấn đề HTML"""
        issues = []
        soup = self.parser.soup
        
        # Kiểm tra alt text trong images
        images = soup.find_all('img')
        for i, img in enumerate(images):
            if not img.get('alt'):
                issues.append(Issue("missing_alt", f"Image at index {i+1}"))
        
        # Kiểm tra links
        links = soup.find_all('a')
        internal_links = 0
        external_links = 0
        
        for i, link in enumerate(links):
            href = link.get('href', '')
            
            # Kiểm tra empty href
            if not href or href == '#':
                issues.append(Issue("empty_href", f"Link <a> at position {i+1}"))
            
            # Phân loại internal/external links
            if href.startswith(('http://', 'https://')):
                external_links += 1
            else:
                internal_links += 1
        
        # Thêm thông tin về links
        if internal_links == 0:
            issues.append(Issue("no_internal_links", "Không có internal links"))
        if external_links == 0:
            issues.append(Issue("no_external_links", "Không có external links"))
        
        return issues
    
    def check_semantic_coverage(self) -> List[Issue]:
        """Kiểm tra semantic coverage bằng string matching"""
        issues = []
        clean_text_lower = self.clean_text.lower()
        
        # Kiểm tra sự lặp heading
        headings = self.parser.get_all_headings()
        all_headings = headings['h1'] + headings['h2'] + headings['h3']
        
        # Tìm headings trùng lặp
        seen_headings = set()
        for heading in all_headings:
            heading_lower = heading.lower()
            if heading_lower in seen_headings:
                issues.append(Issue("duplicate_heading", f"Heading trùng: '{heading}'"))
            seen_headings.add(heading_lower)
        
        # Kiểm tra các từ khóa hỗ trợ (có thể mở rộng)
        support_keywords = {
            'du lịch': ['địa điểm', 'khách sạn', 'ẩm thực', 'kinh nghiệm'],
            'mua sắm': ['giá cả', 'chất lượng', 'khuyến mãi']
        }
        
        # Logic đơn giản để kiểm tra coverage
        for primary_keyword in self.keywords:
            for category, related_words in support_keywords.items():
                if category in primary_keyword.lower():
                    found_related = [word for word in related_words if word in clean_text_lower]
                    if len(found_related) < 2:  # Ít hơn 2 từ liên quan
                        issues.append(Issue("poor_semantic_coverage", 
                                          f"Thiếu từ liên quan cho '{primary_keyword}'"))
        
        return issues


class ArticleAnalysisPipeline:
    """Pipeline chính để chạy toàn bộ phân tích"""
    
    def __init__(self, input_data: Dict[str, Any]):
        self.input_data = input_data
        self.article_data = input_data.get('article', {})
        
    def run_analysis(self) -> Dict[str, Any]:
        """Chạy toàn bộ pipeline phân tích"""
        # Parse article
        parser = ArticleParser(self.article_data.get('content', ''))
        sections = parser.extract_sections()
        parser.extract_intro_and_conclusion()
        
        # SEO Checking
        seo_checker = SEORuleChecker(
            parser=parser,
            title=self.article_data.get('title', ''),
            meta=self.article_data.get('meta_description', ''),
            keywords=self.article_data.get('keywords', [])
        )
        
        # Thực hiện tất cả các kiểm tra
        structure_issues = seo_checker.check_structure()
        keyword_checks = seo_checker.check_keywords()
        length_stats = seo_checker.check_lengths()
        html_issues = seo_checker.check_html_issues()
        semantic_issues = seo_checker.check_semantic_coverage()
        
        # Tổng hợp kết quả
        return {
            "clean_text": parser.clean_text,
            "sections": [
                {
                    "heading": section.heading,
                    "level": section.level,
                    "text": section.text[:200] + "..." if len(section.text) > 200 else section.text,
                    "word_count": section.word_count
                }
                for section in sections
            ],
            "stats": {
                "word_count": length_stats["total_word_count"],
                "title_length": length_stats["title_length"],
                "meta_length": length_stats["meta_length"],
                "intro_length": length_stats["intro_length"],
                "num_h2": len(parser.get_all_headings()['h2']),
                "num_h3": len(parser.get_all_headings()['h3']),
                "images_no_alt": len([issue for issue in html_issues if issue.type == "missing_alt"])
            },
            "keyword_checks": [
                {
                    "keyword": check.keyword,
                    "in_title": check.in_title,
                    "in_meta": check.in_meta,
                    "in_intro": check.in_intro,
                    "density_percent": check.density_percent,
                    "in_headings": check.in_headings,
                    "stuffing": check.stuffing
                }
                for check in keyword_checks
            ],
            "html_issues": [
                {"type": issue.type, "detail": issue.detail}
                for issue in html_issues
            ],
            "structure_issues": [
                {"type": issue.type, "detail": issue.detail}
                for issue in structure_issues + semantic_issues
            ]
        }


def test_sample():
    import json

    try:
        with open('D:/C_to_D/Marketing-Platform/Ver 2.0/learn_architecture/test/agent/articles.json', 'r', encoding='utf-8') as f:
            sample_input = json.load(f)
        
        if 'article' not in sample_input:
            return
        
        pipeline = ArticleAnalysisPipeline(sample_input)
        result = pipeline.run_analysis()

        print(json.dumps(result, indent=2, ensure_ascii=False))

        with open('D:/C_to_D/Marketing-Platform/Ver 2.0/learn_architecture/test/agent/analysis_result.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print("Kết quả đã được lưu!!")
    except Exception as e:
        print("Lỗi")

if __name__ == '__main__':
    test_sample()