# examples/block_analysis_example.py
"""
Ví dụ sử dụng hệ thống block-based SEO analysis
"""

from models.seo_checker.block_schemas import ArticleBlock
from models.llm.content_generation_schemas import SEOArticle
from services.seo_checker.seo_service import SEOCheckerService

def example_block_analysis():
    """Ví dụ phân tích với blocks"""
    
    # 1. Tạo bài viết với blocks
    article = SEOArticle(
        title="AMD Việt Nam: Giải Mã Sức Mạnh Công Nghệ",
        meta_description="Phân tích các sản phẩm mới của AMD tại Việt Nam",
        keywords=["AMD Việt Nam", "công nghệ", "sản phẩm mới"],
        blocks=[
            # H1 - có keyword
            ArticleBlock(id="h1-1", tag="h1", text="AMD Việt Nam Ra Mắt Sản Phẩm Mới"),
            
            # Đoạn mở đầu - KHÔNG có keyword
            ArticleBlock(id="p-1", tag="p", text="Trong bối cảnh công nghệ liên tục chuyển mình..."),
            
            # H2 thứ nhất - có keyword
            ArticleBlock(id="h2-1", tag="h2", text="AMD Việt Nam Với Ryzen 9000 Series"),
            
            # Đoạn văn QUÁ DÀI (>150 từ)
            ArticleBlock(
                id="p-2", 
                tag="p", 
                text="Là tâm điểm của sự kiện, bộ vi xử lý Ryzen 9000 Series..." * 20  # Giả sử 300+ từ
            ),
            
            # H2 thứ hai - không có keyword
            ArticleBlock(id="h2-2", tag="h2", text="Card Đồ Họa Cao Cấp"),
            
            # H2 thứ ba
            ArticleBlock(id="h2-3", tag="h2", text="Công Nghệ FSR4 Mới"),
            
            # Thêm H1 thừa
            ArticleBlock(id="h1-2", tag="h1", text="Đây là H1 thừa"),
        ],
        html_content=None,  # Không dùng HTML
        references=[],
        images=[]
    )
    
    # 2. Phân tích SEO
    service = SEOCheckerService()
    result = service.analyze_seo_with_blocks(article)
    
    # 3. Hiển thị kết quả
    print("=== KẾT QUẢ PHÂN TÍCH SEO VỚI BLOCKS ===")
    print(f"Điểm tổng: {result['score_breakdown']['total']}")
    print(f"Xếp loại: {result['score_breakdown']['grade']}")
    print(f"Loại parser: {result['stats']['parser_type']}")
    print()
    
    print("=== VÍ DỤ ISSUES VỚI BLOCK_ID ===")
    for severity in ["critical", "warning", "info"]:
        issues = result['issues'].get(severity, [])
        if issues:
            print(f"\n{severity.upper()} ISSUES ({len(issues)}):")
            for issue in issues[:3]:  # Hiển thị 3 issue đầu
                print(f"  • [{issue['type']}]")
                print(f"    Block: {issue['block_id']}")
                print(f"    Detail: {issue['detail']}")
                print(f"    Recommendation: {issue['recommendation']}")
    
    return result

if __name__ == '__main__':
  example_block_analysis()