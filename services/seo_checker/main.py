"""
SEO Checker Demo với output chi tiết
"""

import json
import os
from services.seo_checker import ProfessionalSEOPipeline

def detailed_demo():
    """Demo chi tiết với output đầy đủ"""
    
    # Đường dẫn config
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    config_dir = os.path.join(base_dir, "core", "score_yaml")
    
    # Dữ liệu demo
    article_data = {
        "title": "Cẩm Nang Du Lịch Hà Nội: Hành Trình Khám Phá Thủ Đô",
        "meta_description": "Hướng dẫn du lịch Hà Nội chi tiết với các địa điểm nổi tiếng và ẩm thực đặc trưng",
        "content": """
            <h1>Cẩm Nang Du Lịch Hà Nội</h1>
            <p>Hà Nội - thủ đô ngàn năm văn hiến của Việt Nam.</p>
            
            <h2>Địa Điểm Nổi Tiếng</h2>
            <p>Hồ Hoàn Kiếm, Văn Miếu Quốc Tử Giám, Phố cổ Hà Nội.</p>
            
            <h2>Ẩm Thực Hà Nội</h2>
            <p>Phở, bún chả, chả cá Lã Vọng, cốm làng Vòng.</p>
            
            <h2>Kinh Nghiệm Du Lịch</h2>
            <p>Thời điểm lý tưởng: mùa thu (tháng 9-11).</p>
        """,
        "keywords": ["du lịch Hà Nội", "điểm đến Hà Nội", "ẩm thực Hà Nội"]
    }
    
    try:
        # Khởi tạo pipeline
        pipeline = ProfessionalSEOPipeline(
            config_dir=config_dir,
            industry="blog_tin_tuc"
        )
        
        # Phân tích
        print("Đang phân tích bài viết...")
        result = pipeline.analyze(article_data)
        
        # Hiển thị kết quả
        print("\n" + "="*60)
        print("KẾT QUẢ PHÂN TÍCH SEO")
        print("="*60)
        
        score = result['score_breakdown']
        print(f"\n📊 ĐIỂM SỐ:")
        print(f"   • Tổng điểm: {score['total']}/100")
        print(f"   • Xếp loại: {score['grade']}")
        print(f"   • Cấu trúc: {score['structure']}")
        print(f"   • Từ khóa: {score['keyword_optimization']}")
        print(f"   • Dễ đọc: {score['readability']}")
        
        stats = result['stats']
        print(f"\n📈 THỐNG KÊ:")
        print(f"   • Số từ: {stats['word_count']}")
        print(f"   • Số H2: {len(stats['headings']['h2'])}")
        print(f"   • Số ảnh: {stats['images_count']}")
        
        # Đếm issues
        issues = result['issues']
        critical_count = len(issues['critical'])
        warning_count = len(issues['warning'])
        
        if critical_count > 0 or warning_count > 0:
            print(f"\n⚠️  VẤN ĐỀ PHÁT HIỆN:")
            print(f"   • Nghiêm trọng: {critical_count}")
            print(f"   • Cảnh báo: {warning_count}")
        
        # Lưu kết quả
        results_dir = os.path.join(base_dir, "results")
        os.makedirs(results_dir, exist_ok=True)
        
        output_file = os.path.join(results_dir, "seo_analysis_result.json")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Đã lưu kết quả chi tiết vào: {output_file}")
        
        return result
        
    except Exception as e:
        print(f"\n❌ LỖI: {str(e)}")
        return None

if __name__ == '__main__':
    detailed_demo()