"""
HTML Parser Module
"""

from bs4 import BeautifulSoup
import re
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)


class EnhancedArticleParser:
    """Parser cải tiến với xử lý tốt hơn"""
    
    def __init__(self, html_content: str):
        self.soup = BeautifulSoup(html_content, 'html.parser')
        self._clean_html()
    
    def _clean_html(self):
        """Làm sạch HTML"""
        for tag in self.soup(["script", "style", "meta", "link"]):
            tag.decompose()
    
    def get_clean_text(self) -> str:
        """Lấy văn bản sạch - FIX BUG"""
        text = self.soup.get_text(separator='\n')
        
        # Chuẩn hóa whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return text
    
    def get_first_paragraph(self) -> str:
        """Lấy đoạn văn đầu tiên (intro)"""
        # Tìm đoạn văn đầu tiên có nội dung thực sự
        for p in self.soup.find_all('p'):
            text = p.get_text().strip()
            if len(text.split()) > 10:  # Ít nhất 10 từ
                return text
        return ""
    
    def get_headings(self) -> Dict[str, List[str]]:
        """Lấy tất cả headings"""
        return {
            'h1': [h.get_text().strip() for h in self.soup.find_all('h1')],
            'h2': [h.get_text().strip() for h in self.soup.find_all('h2')],
            'h3': [h.get_text().strip() for h in self.soup.find_all('h3')],
            'h4': [h.get_text().strip() for h in self.soup.find_all('h4')],
        }
    
    def get_images(self) -> List[Dict[str, str]]:
        """Lấy thông tin images"""
        return [
            {
                'src': img.get('src', ''),
                'alt': img.get('alt', ''),
                'has_alt': bool(img.get('alt'))
            }
            for img in self.soup.find_all('img')
        ]
    
    def get_links(self) -> Dict[str, List[str]]:
        """Phân loại links"""
        internal = []
        external = []
        
        for link in self.soup.find_all('a'):
            href = link.get('href', '')
            if not href or href == '#':
                continue
            
            if href.startswith(('http://', 'https://')):
                external.append(href)
            else:
                internal.append(href)
        
        return {'internal': internal, 'external': external}
    
    def get_paragraphs_stats(self) -> List[Dict[str, Any]]:
        """Thống kê các đoạn văn"""
        stats = []
        for i, p in enumerate(self.soup.find_all('p')):
            text = p.get_text().strip()
            words = text.split()
            stats.append({
                'index': i + 1,
                'word_count': len(words),
                'char_count': len(text),
                'text_preview': text[:100] + '...' if len(text) > 100 else text
            })
        return stats
    
    def __repr__(self):
        return self.get_clean_text()
    
if __name__ == '__main__':
    html_content = "<h1>AMD Việt Nam: Giải Mã Sức Mạnh Công Nghệ Với Loạt Sản Phẩm Mới Nhất</h1>\n\n<p>Trong bối cảnh công nghệ liên tục chuyển mình, những cải tiến mạnh mẽ từ các hãng lớn luôn được cộng đồng người dùng quan tâm đặc biệt. <strong>AMD Việt Nam</strong> vừa tạo dấu ấn mới với series sản phẩm chủ lực ra mắt tại các sự kiện công nghệ gần đây, từ CPU đột phá đến các công nghệ đồ họa và xử lý hình ảnh tiên tiến. Bài viết này sẽ phân tích chi tiết về các dòng sản phẩm mới nhất của AMD, đồng thời hướng dẫn bạn cách lựa chọn phù hợp để khai thác tối đa lợi ích công nghệ cho công việc và giải trí.</p>\n\n<h2>AMD Việt Nam: Tăng Tốc Hiệu Suất Với Ryzen 9000 Series</h2>\n<p>Là tâm điểm của sự kiện, bộ vi xử lý <strong>Ryzen 9000 Series</strong> dựa trên kiến trúc Zen 5 được phát triển với mục tiêu nâng cao hiệu năng đa nhiệm, tiết kiệm điện, tối ưu cho cả PC cá nhân lẫn máy trạm chuyên nghiệp. Đặc điểm nổi bật của dòng CPU này gồm:</p>\n<ul>\n    <li><strong>Kiến trúc Zen 5 hoàn toàn mới:</strong> Tăng hiệu suất xử lý so với thế hệ cũ, cho tốc độ đa luồng mượt mà hơn.</li>\n    <li><strong>Công nghệ tiết kiệm năng lượng:</strong> Giúp máy tính vận hành êm ái với lượng tiêu thụ điện năng thấp.</li>\n    <li><strong>Lựa chọn đa dạng:</strong> Từ phiên bản dành cho người dùng phổ thông đến bản cao cấp cho sáng tạo nội dung, thiết kế đồ họa và gaming chuyên nghiệp.</li>\n</ul>\n<p>Điểm đáng chú ý là Ryzen 9000 Series không chỉ phù hợp cho các cấu hình PC desktop truyền thống mà còn tối ưu hóa trên các dòng laptop cao cấp.</p>\n\n<h2>Ryzen Z2 Series: Tối Ưu Cho Máy Chơi Game Cầm Tay</h2>\n<p>Bên cạnh CPU desktop, AMD Việt Nam lần đầu trình làng <strong>Ryzen Z2 Series</strong> – chip xử lý đặc thù cho máy chơi game cầm tay. Trong bối cảnh nhu cầu giải trí di động ngày càng cao, dòng CPU này mang lại trải nghiệm chơi game mượt mà với các tính năng nổi bật:</p>\n<ul>\n    <li>Nâng cao hiệu suất đồ họa và tốc độ xử lý tiết kiệm năng lượng.</li>\n    <li>Khả năng tương thích đa dạng với nhiều dòng máy chơi game cầm tay quốc tế và nội địa.</li>\n    <li>Hỗ trợ công nghệ làm mát và tối ưu hóa chơi game liên tục nhiều giờ.</li>\n</ul>\n<p>Dù là game thủ chuyên nghiệp hay chỉ yêu thích giải trí di động, Ryzen Z2 Series hứa hẹn mở ra những trải nghiệm vượt xa kỳ vọng truyền thống.</p>\n\n<h2>Card Đồ Họa Radeon 9000 Series: Đỉnh Cao Sáng Tạo Và Gaming</h2>\n<p>Nổi bật không kém là loạt <strong>card đồ họa Radeon 9000 Series</strong> – sản phẩm thế hệ mới mang lại sức mạnh xử lý đồ họa vượt trội cho cả trải nghiệm chơi game lẫn sáng tạo nội dung số.</p>\n<ul>\n    <li><strong>Hiệu năng đột phá:</strong> Phù hợp các ứng dụng nặng – dựng hình 3D, render video, thiết kế đồ họa chuyên nghiệp.</li>\n    <li><strong>Công nghệ làm mát hiệu quả:</strong> Giúp máy chạy ổn định kể cả khi gaming hay xử lý tác vụ liên tục.</li>\n    <li><strong>Hỗ trợ đa nền tảng:</strong> Tối ưu cho PC, workstation lẫn laptop gaming.</li>\n</ul>\n<p>Radeon 9000 Series trở thành lựa chọn lý tưởng cho những ai đòi hỏi hiệu suất cao và các tính năng tối ưu cho đồ họa hiện đại.</p>\n\n<h2>FSR4: Công Nghệ Nâng Cấp Hình Ảnh Mới Nhất</h2>\n<p>Bổ trợ cho trải nghiệm hình ảnh trên nền tảng phần cứng mới, AMD giới thiệu <strong>FSR4 (FidelityFX Super Resolution 4)</strong> – công nghệ nâng cấp hình ảnh giúp hiển thị sắc nét mà không làm giảm hiệu năng khung hình.</p>\n<ul>\n    <li>Độ nét ảnh nâng cao, giữ chi tiết ngay cả ở chế độ giả lập độ phân giải cao.</li>\n    <li>Tích hợp trực tiếp trong nhiều tựa game PC và thiết bị di động.</li>\n    <li>Giúp tối ưu tốc độ khung hình ngay trên các cấu hình máy vừa phải.</li>\n</ul>\n<p>FSR4 giúp người dùng tận hưởng trải nghiệm hình ảnh đỉnh cao mà không phải nâng cấp phần cứng mạnh tay.</p>\n\n<h2>Định Hình Lựa Chọn Cho Người Dùng Việt Nam</h2>\n<p>Sự ra mắt đồng loạt của các sản phẩm mới <strong>AMD Việt Nam</strong> như Ryzen 9000 Series, Radeon 9000 Series và giải pháp FSR4 mang tới cơ hội lớn cho cộng đồng công nghệ nước nhà. Người dùng có thể đa dạng hóa trải nghiệm theo nhu cầu:</p>\n<ul>\n    <li><strong>Học tập, làm việc văn phòng:</strong> Chọn các CPU Ryzen thế hệ mới tối ưu hiệu năng, tiết kiệm điện năng.</li>\n    <li><strong>Chơi game, sáng tạo nội dung:</strong> Card đồ họa Radeon 9000 và FSR4 đảm bảo chuyển động mượt, chất lượng hình ảnh sắc nét.</li>\n    <li><strong>Giải trí di động:</strong> Ryzen Z2 Series dành riêng cho máy chơi game cầm tay.</li>\n</ul>\n<p>Một điểm cộng lớn: AMD không ngừng đồng hành cùng đối tác Việt Nam để nâng cấp hệ thống bảo hành, tư vấn kỹ thuật và cập nhật công nghệ mới, giúp người dùng luôn yên tâm trải nghiệm.</p>\n\n<h2>Lời Kết & Gợi Ý Hành Động</h2>\n<p>Những sản phẩm mới của <strong>AMD Việt Nam</strong> không chỉ là bước tiến công nghệ mà còn là cam kết đồng hành phát triển cùng thị trường Việt. Nếu bạn đang cân nhắc nâng cấp máy tính hoặc tìm giải pháp đồ họa, hiệu năng cao, hãy khám phá chi tiết các lựa chọn mới từ AMD để bắt kịp xu hướng toàn cầu. Đừng quên theo dõi các thông tin cập nhật tại blog, diễn đàn công nghệ, và liên hệ các đại lý chính hãng khi cần tư vấn trực tiếp!</p>"
    en = EnhancedArticleParser(html_content=html_content)
    print(en.get_clean_text())