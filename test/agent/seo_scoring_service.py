"""
SEO Scoring Service - Module đánh giá điểm SEO dựa trên phân tích HTML
Author: Senior Python Engineer
Date: 2024
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass


@dataclass
class ScoreBreakdown:
    """Dataclass chứa điểm chi tiết từng hạng mục"""
    title: int = 0
    meta: int = 0
    structure: int = 0
    keyword_density: int = 0
    readability: int = 0
    links: int = 0
    images: int = 0


class SEOScoringService:
    """Dịch vụ chấm điểm SEO dựa trên kết quả phân tích HTML"""
    
    def __init__(self, analysis_data: Dict[str, Any]):
        self.data = analysis_data
        self.stats = analysis_data.get('stats', {})
        self.keyword_checks = analysis_data.get('keyword_checks', [])
        self.html_issues = analysis_data.get('html_issues', [])
        self.structure_issues = analysis_data.get('structure_issues', [])
        self.sections = analysis_data.get('sections', [])
        
        # Lấy từ khóa chính (keyword đầu tiên)
        self.main_keyword = self.keyword_checks[0]['keyword'] if self.keyword_checks else ""
        
        # Khởi tạo breakdown
        self.breakdown = ScoreBreakdown()
        self.recommendations = []
    
    def calculate_score(self) -> Dict[str, Any]:
        """Tính toán điểm SEO tổng hợp"""
        self._score_title()
        self._score_meta()
        self._score_structure()
        self._score_keyword_density()
        self._score_readability()
        self._score_links()
        self._score_images()
        
        # Tính tổng điểm (0-100)
        total_score = sum([
            self.breakdown.title,
            self.breakdown.meta,
            self.breakdown.structure,
            self.breakdown.keyword_density,
            self.breakdown.readability,
            self.breakdown.links,
            self.breakdown.images
        ])
        
        # Đảm bảo điểm trong khoảng 0-100
        total_score = max(0, min(100, total_score))
        
        return {
            "score": total_score,
            "score_breakdown": {
                "title": self.breakdown.title,
                "meta": self.breakdown.meta,
                "structure": self.breakdown.structure,
                "keyword_density": self.breakdown.keyword_density,
                "readability": self.breakdown.readability,
                "links": self.breakdown.links,
                "images": self.breakdown.images
            },
            "recommendations": self.recommendations
        }
    
    def _score_title(self) -> None:
        """Chấm điểm tiêu đề"""
        title_length = self.stats.get('title_length', 0)
        
        # Điểm dựa trên độ dài
        if 50 <= title_length <= 60:
            self.breakdown.title += 10
        elif 40 <= title_length <= 70:
            self.breakdown.title += 8
        elif title_length < 30 or title_length > 65:
            self.breakdown.title += 5
            self.recommendations.append(f"Tiêu đề {title_length} ký tự nên nằm trong khoảng 50-60 ký tự")
        else:
            self.breakdown.title += 7
        
        # Kiểm tra keyword trong tiêu đề
        if self.keyword_checks:
            main_keyword_check = next(
                (k for k in self.keyword_checks if k['keyword'] == self.main_keyword), 
                self.keyword_checks[0]
            )
            
            if not main_keyword_check.get('in_title', False):
                self.breakdown.title -= 3
                self.recommendations.append(f"Thiếu từ khóa chính '{self.main_keyword}' trong tiêu đề")
    
    def _score_meta(self) -> None:
        """Chấm điểm meta description"""
        meta_length = self.stats.get('meta_length', 0)
        
        # Điểm dựa trên độ dài
        if 120 <= meta_length <= 160:
            self.breakdown.meta += 10
        elif 110 <= meta_length <= 170:
            self.breakdown.meta += 8
        else:
            self.breakdown.meta += 5
            self.recommendations.append(f"Meta description {meta_length} ký tự nên nằm trong khoảng 120-160 ký tự")
        
        # Kiểm tra keyword trong meta
        if self.keyword_checks:
            main_keyword_check = next(
                (k for k in self.keyword_checks if k['keyword'] == self.main_keyword), 
                self.keyword_checks[0]
            )
            
            if not main_keyword_check.get('in_meta', False):
                self.breakdown.meta -= 5
                self.recommendations.append(f"Thiếu từ khóa chính '{self.main_keyword}' trong meta description")
    
    def _score_structure(self) -> None:
        """Chấm điểm cấu trúc heading"""
        num_h2 = self.stats.get('num_h2', 0)
        num_h3 = self.stats.get('num_h3', 0)
        
        # Kiểm tra H1
        has_h1 = any(section['level'] == 'h1' for section in self.sections)
        if has_h1:
            self.breakdown.structure += 5
        else:
            self.recommendations.append("Thiếu thẻ H1 trong bài viết")
        
        # Kiểm tra H2
        if num_h2 >= 2:
            self.breakdown.structure += 5
        else:
            self.recommendations.append(f"Cần thêm H2 (hiện có {num_h2} H2)")
        
        # Kiểm tra H3
        if num_h3 >= 2:
            self.breakdown.structure += 5
        else:
            self.recommendations.append(f"Cần thêm H3 (hiện có {num_h3} H3)")
        
        # Kiểm tra keyword trong heading
        if self.keyword_checks:
            main_keyword_check = next(
                (k for k in self.keyword_checks if k['keyword'] == self.main_keyword), 
                self.keyword_checks[0]
            )
            
            if main_keyword_check.get('in_headings'):
                self.breakdown.structure += 5
            else:
                self.recommendations.append(f"Từ khóa chính không xuất hiện trong các heading")
    
    def _score_keyword_density(self) -> None:
        """Chấm điểm mật độ từ khóa"""
        if not self.keyword_checks:
            self.recommendations.append("Không có từ khóa để phân tích")
            return
        
        # Lấy mật độ từ khóa chính
        main_keyword_check = next(
            (k for k in self.keyword_checks if k['keyword'] == self.main_keyword), 
            self.keyword_checks[0]
        )
        
        density = main_keyword_check.get('density_percent', 0)
        
        # Chấm điểm theo mật độ
        if 0.8 <= density <= 2.5:
            self.breakdown.keyword_density += 10
        elif 0.5 <= density < 0.8:
            self.breakdown.keyword_density += 5
            self.recommendations.append(f"Mật độ từ khóa {density:.1f}% hơi thấp, nên từ 0.8-2.5%")
        elif density < 0.5:
            self.breakdown.keyword_density -= 5
            self.recommendations.append(f"Mật độ từ khóa {density:.1f}% quá thấp, nên từ 0.8-2.5%")
        elif density > 3.5:
            self.breakdown.keyword_density -= 5
            self.recommendations.append(f"Mật độ từ khóa {density:.1f}% quá cao, có thể bị coi là spam")
        elif density > 2.5:
            self.breakdown.keyword_density += 5
            self.recommendations.append(f"Mật độ từ khóa {density:.1f}% hơi cao, nên từ 0.8-2.5%")
    
    def _score_readability(self) -> None:
        """Chấm điểm khả năng đọc"""
        # Đếm số câu dài từ structure_issues
        long_sentence_count = sum(
            1 for issue in self.structure_issues 
            if issue.get('type') == 'sentence_too_long'
        )
        
        # Mỗi câu dài trừ 1 điểm, tối đa trừ 15 điểm
        readability_penalty = min(long_sentence_count, 15)
        self.breakdown.readability -= readability_penalty
        
        if long_sentence_count > 0:
            self.recommendations.append(f"Rút ngắn {long_sentence_count} câu vượt quá 35 từ")
    
    def _score_links(self) -> None:
        """Chấm điểm internal/external links"""
        # Phân tích html_issues để tìm thông tin links
        has_internal = True
        has_external = True
        
        # Kiểm tra các issues liên quan đến links
        for issue in self.html_issues:
            issue_type = issue.get('type', '')
            
            if issue_type == 'no_internal_links':
                has_internal = False
                self.recommendations.append("Thêm internal links để cải thiện SEO")
            
            elif issue_type == 'no_external_links':
                has_external = False
                self.recommendations.append("Thêm external links chất lượng để tăng độ tin cậy")
        
        # Chấm điểm
        if has_internal:
            self.breakdown.links += 5
        
        if has_external:
            self.breakdown.links += 5
    
    def _score_images(self) -> None:
        """Chấm điểm ảnh và alt text"""
        images_no_alt = self.stats.get('images_no_alt', 0)
        
        # Mỗi ảnh thiếu alt trừ 2 điểm, tối đa trừ 10 điểm
        image_penalty = min(images_no_alt * 2, 10)
        self.breakdown.images -= image_penalty
        
        if images_no_alt > 0:
            self.recommendations.append(f"Thêm alt text cho {images_no_alt} ảnh")
        
        # Nếu không có ảnh nào
        total_images = images_no_alt  # Giả sử đây là tổng số ảnh (cần thêm logic đếm tổng ảnh)
        if total_images == 0:
            self.recommendations.append("Xem xét thêm hình ảnh minh họa")


def calculate_seo_score(analysis_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Hàm chính để tính điểm SEO từ dữ liệu phân tích
    
    Args:
        analysis_data: Dictionary chứa kết quả phân tích từ module trước
    
    Returns:
        Dictionary chứa điểm SEO và các khuyến nghị
    """
    scoring_service = SEOScoringService(analysis_data)
    return scoring_service.calculate_score()


def test_scoring():
    """Hàm test mẫu"""
    # Dữ liệu mẫu giống output của module phân tích trước
    sample_analysis = {
        "clean_text": "văn bản sạch...",
        "sections": [
            {
                "heading": "Du Lịch Hà Nội - Khám Phá Thủ Đô Việt Nam",
                "level": "h1",
                "text": "Nội dung H1...",
                "word_count": 50
            },
            {
                "heading": "Địa điểm du lịch Hà Nội nổi tiếng",
                "level": "h2",
                "text": "Nội dung H2...",
                "word_count": 150
            }
        ],
        "stats": {
            "word_count": 1200,
            "title_length": 58,
            "meta_length": 145,
            "intro_length": 80,
            "num_h2": 3,
            "num_h3": 5,
            "images_no_alt": 2
        },
        "keyword_checks": [
            {
                "keyword": "du lịch Hà Nội",
                "in_title": True,
                "in_meta": True,
                "in_intro": True,
                "density_percent": 1.5,
                "in_headings": ["H1", "H2 #1"],
                "stuffing": False
            },
            {
                "keyword": "ẩm thực Hà Nội",
                "in_title": False,
                "in_meta": True,
                "in_intro": False,
                "density_percent": 0.8,
                "in_headings": ["H2 #2"],
                "stuffing": False
            }
        ],
        "html_issues": [
            {"type": "missing_alt", "detail": "Image at index 1"},
            {"type": "missing_alt", "detail": "Image at index 2"}
        ],
        "structure_issues": [
            {"type": "sentence_too_long", "detail": "Câu #3 có 40 từ"},
            {"type": "sentence_too_long", "detail": "Câu #8 có 38 từ"}
        ]
    }
    
    result = calculate_seo_score(sample_analysis)
    
    import json
    print("📊 Kết quả chấm điểm SEO:")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    test_scoring()