# test_auto_fix_api.py
"""
Test API auto-fix-iterative với dữ liệu thực tế
"""

import json
import requests
import asyncio
from typing import Dict, Any

# URL API của bạn
API_URL = "http://localhost:8080/api/v1/seo/auto-fix-iterative"

def create_test_data() -> Dict[str, Any]:
    """
    Tạo dữ liệu test từ score result bạn cung cấp
    """
    
    # 1. Tạo article (phải có đầy đủ các field theo schema)
    article = {
        "title": "ChatGPT 5.0 Ra Mắt: Công Nghệ AI Đột Phá Cho Tương Lai Nhân Loại Và Thế Giới Số",  # Title dài 66 ký tự
        "meta_description": "Khám phá những cải tiến mới nhất trong công nghệ AI với sự ra mắt của ChatGPT 5.0. Tìm hiểu về khả năng xử lý ngôn ngữ tự nhiên vượt trội và ứng dụng trong đời sống.",
        "keywords": [
            "chatgpt 5.0 có gì hot",
            "nâng cấp chatgpt 5.0", 
            "tính năng chatgpt 5.0"
        ],
        "blocks": [
            {
                "id": "h1-1",
                "tag": "h1",
                "text": "Sự Ra Mắt Của ChatGPT 5.0",
                "word_count": 6
            },
            {
                "id": "p-1",
                "tag": "p",
                "text": "Trong thế giới công nghệ đang phát triển với tốc độ chóng mặt, trí tuệ nhân tạo đã trở thành một phần không thể thiếu. Các nhà nghiên cứu liên tục tìm kiếm cách cải thiện khả năng của AI để phục vụ con người tốt hơn.",
                "word_count": 38
            },
            {
                "id": "h2-1",
                "tag": "h2",
                "text": "Công Nghệ Đằng Sau ChatGPT 5.0",
                "word_count": 5
            },
            {
                "id": "p-2",
                "tag": "p",
                "text": "Phiên bản mới nhất này được xây dựng trên kiến trúc Transformer cải tiến với hàng tỷ tham số được tối ưu hóa. Khả năng hiểu ngữ cảnh và tạo ra văn bản tự nhiên đã được nâng cao đáng kể so với các phiên bản trước.",
                "word_count": 35
            },
            {
                "id": "h2-2",
                "tag": "h2",
                "text": "Ứng Dụng Thực Tế",
                "word_count": 3
            },
            {
                "id": "p-3",
                "tag": "p",
                "text": "Từ hỗ trợ viết lách, lập trình đến nghiên cứu khoa học, ChatGPT 5.0 mang lại trải nghiệm mượt mà và chính xác hơn bao giờ hết. Nhiều doanh nghiệp đã bắt đầu tích hợp công nghệ này vào quy trình làm việc.",
                "word_count": 34
            }
        ],
        "html_content": None,
        "references": [],
        "images": []
    }
    
    # 2. Score result bạn cung cấp
    score_result = {
        "score_breakdown": {
            "structure": 20,
            "keyword_optimization": 0,
            "readability": 20,
            "technical_seo": 7,
            "content_quality": 20,
            "bonus": 5,
            "total": 72,
            "grade": "B"
        },
        "issues": {
            "critical": [
                {
                    "type": "title_too_long",
                    "detail": "Title có 66 ký tự - sẽ bị cắt",
                    "severity": "critical",
                    "penalty": 5,
                    "recommendation": "Rút ngắn xuống 60 ký tự"
                }
            ],
            "warning": [
                {
                    "type": "keyword_not_in_meta",
                    "detail": "Keyword 'chatgpt 5.0 có gì hot' không có trong meta description",
                    "severity": "warning",
                    "penalty": 3,
                    "recommendation": "Thêm keyword 'chatgpt 5.0 có gì hot' vào meta description"
                },
                {
                    "type": "keyword_not_in_title",
                    "detail": "Keyword 'nâng cấp chatgpt 5.0' không có trong tiêu đề bài viết",
                    "severity": "warning",
                    "penalty": 5,
                    "recommendation": "Thêm keyword 'nâng cấp chatgpt 5.0' vào tiêu đề, ưu tiên đứng đầu"
                },
                {
                    "type": "keyword_not_in_meta",
                    "detail": "Keyword 'nâng cấp chatgpt 5.0' không có trong meta description",
                    "severity": "warning",
                    "penalty": 3,
                    "recommendation": "Thêm keyword 'nâng cấp chatgpt 5.0' vào meta description"
                },
                {
                    "type": "keyword_not_in_h1",
                    "detail": "Keyword 'nâng cấp chatgpt 5.0' không có trong thẻ H1 chính",
                    "severity": "warning",
                    "penalty": 3,
                    "recommendation": "Thêm keyword 'nâng cấp chatgpt 5.0' vào thẻ H1 này"
                },
                {
                    "type": "keyword_not_in_title",
                    "detail": "Keyword 'tính năng chatgpt 5.0' không có trong tiêu đề bài viết",
                    "severity": "warning",
                    "penalty": 5,
                    "recommendation": "Thêm keyword 'tính năng chatgpt 5.0' vào tiêu đề, ưu tiên đứng đầu"
                },
                {
                    "type": "keyword_not_in_meta",
                    "detail": "Keyword 'tính năng chatgpt 5.0' không có trong meta description",
                    "severity": "warning",
                    "penalty": 3,
                    "recommendation": "Thêm keyword 'tính năng chatgpt 5.0' vào meta description"
                },
                {
                    "type": "keyword_not_in_h1",
                    "detail": "Keyword 'tính năng chatgpt 5.0' không có trong thẻ H1 chính",
                    "severity": "warning",
                    "penalty": 3,
                    "recommendation": "Thêm keyword 'tính năng chatgpt 5.0' vào thẻ H1 này"
                },
                {
                    "type": "no_internal_links",
                    "detail": "Không có internal links",
                    "severity": "warning",
                    "penalty": 3,
                    "recommendation": "Thêm 3-5 internal links liên quan"
                }
            ],
            "info": [
                {
                    "type": "keyword_not_in_h2",
                    "detail": "Keyword 'chatgpt 5.0 có gì hot' không xuất hiện trong bất kỳ thẻ H2 nào",
                    "severity": "info",
                    "penalty": 1,
                    "recommendation": "Thêm keyword 'chatgpt 5.0 có gì hot' vào thẻ H2 này hoặc một H2 khác"
                },
                {
                    "type": "keyword_not_in_first_paragraph",
                    "detail": "Keyword 'nâng cấp chatgpt 5.0' không xuất hiện trong đoạn văn đầu tiên",
                    "severity": "info",
                    "penalty": 2,
                    "recommendation": "Chèn keyword 'nâng cấp chatgpt 5.0' vào đoạn mở đầu này"
                },
                {
                    "type": "keyword_not_in_h2",
                    "detail": "Keyword 'nâng cấp chatgpt 5.0' không xuất hiện trong bất kỳ thẻ H2 nào",
                    "severity": "info",
                    "penalty": 1,
                    "recommendation": "Thêm keyword 'nâng cấp chatgpt 5.0' vào thẻ H2 này hoặc một H2 khác"
                },
                {
                    "type": "keyword_not_in_first_paragraph",
                    "detail": "Keyword 'tính năng chatgpt 5.0' không xuất hiện trong đoạn văn đầu tiên",
                    "severity": "info",
                    "penalty": 2,
                    "recommendation": "Chèn keyword 'tính năng chatgpt 5.0' vào đoạn mở đầu này"
                },
                {
                    "type": "keyword_not_in_h2",
                    "detail": "Keyword 'tính năng chatgpt 5.0' không xuất hiện trong bất kỳ thẻ H2 nào",
                    "severity": "info",
                    "penalty": 1,
                    "recommendation": "Thêm keyword 'tính năng chatgpt 5.0' vào thẻ H2 này hoặc một H2 khác"
                }
            ]
        },
        "bonuses": [
            {
                "type": "good_heading_structure",
                "points": 5
            }
        ],
        "stats": {
            "word_count": 1613,
            "title_length": 66,
            "meta_length": 139,
            "headings": {},
            "images_count": 0,
            "links": {}
        },
        "config_used": {},
        "success": True,
        "message": "Phân tích SEO với blocks thành công"
    }
    
    return {
        "article": article,
        "score_result": score_result
    }

async def test_api():
    """Test API auto-fix-iterative"""
    print("=" * 80)
    print("TEST API AUTO-FIX-ITERATIVE")
    print("=" * 80)
    
    # Tạo dữ liệu test
    data = create_test_data()
    
    print("\n📋 THÔNG TIN BÀI VIẾT:")
    print(f"   - Title: {data['article']['title']}")
    print(f"   - Meta length: {len(data['article']['meta_description'])} chars")
    print(f"   - Keywords: {', '.join(data['article']['keywords'])}")
    print(f"   - Blocks: {len(data['article']['blocks'])}")
    print(f"   - Score: {data['score_result']['score_breakdown']['total']} ({data['score_result']['score_breakdown']['grade']})")
    
    print("\n🔍 ISSUES FOUND:")
    for severity, issues in data['score_result']['issues'].items():
        print(f"   - {severity.upper()}: {len(issues)} issues")
        for issue in issues[:2]:  # Hiển thị 2 issue đầu mỗi loại
            print(f"     • {issue['type']}: {issue['detail'][:50]}...")
    
    print("\n🚀 GỬI REQUEST ĐẾN API...")
    
    try:
        # Gửi request
        response = requests.post(
            API_URL,
            json=data,
            headers={"Content-Type": "application/json"},
            timeout=300  # Timeout 5 phút cho AI processing
        )
        
        print(f"\n📥 RESPONSE STATUS: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            print("\n✅ AUTO-FIX THÀNH CÔNG!")
            print(f"\n📊 KẾT QUẢ TỔNG QUAN:")
            print(f"   - Tổng iterations: {result.get('total_iterations', 0)}")
            print(f"   - Tasks đã áp dụng: {result.get('total_applied_tasks', 0)}")
            print(f"   - Tasks bỏ qua: {result.get('total_skipped_tasks', 0)}")
            print(f"   - Điểm ban đầu: {result.get('initial_score', 0)}")
            print(f"   - Điểm cuối cùng: {result.get('final_score_total', 0)}")
            print(f"   - Cải thiện: +{result.get('score_improvement', 0)} điểm")
            
            print(f"\n🔄 LỊCH SỬ ITERATIONS:")
            for history in result.get('history', []):
                print(f"   - Iteration {history['iteration']}: {history['score_before']} → {history['score_after']} (+{history['score_after'] - history['score_before']})")
                print(f"     Applied: {history['applied_tasks']}, Skipped: {history['skipped_tasks']}")
            
            print(f"\n📝 THAY ĐỔI QUAN TRỌNG:")
            final_article = result.get('final_article', {})
            
            # Hiển thị title mới
            new_title = final_article.get('title', '')
            old_title = data['article']['title']
            if new_title != old_title:
                print(f"   - Title mới ({len(new_title)} chars): {new_title}")
            
            # Hiển thị meta mới
            new_meta = final_article.get('meta_description', '')
            old_meta = data['article']['meta_description']
            if new_meta != old_meta:
                print(f"   - Meta mới ({len(new_meta)} chars): {new_meta[:80]}...")
            
            # Hiển thị block changes
            new_blocks = final_article.get('blocks', [])
            old_blocks = data['article']['blocks']
            
            if len(new_blocks) > len(old_blocks):
                print(f"   - Đã thêm {len(new_blocks) - len(old_blocks)} block(s) mới")
            
            # Tìm các block đã sửa
            print(f"\n🔧 CÁC BLOCK ĐÃ SỬA:")
            for new_block in new_blocks:
                new_id = new_block.get('id')
                new_text = new_block.get('text', '')
                
                # Tìm block cũ tương ứng
                old_block = None
                for block in old_blocks:
                    if block.get('id') == new_id:
                        old_block = block
                        break
                
                if old_block and old_block.get('text') != new_text:
                    print(f"   - Block {new_id}:")
                    print(f"     Cũ: {old_block.get('text', '')[:50]}...")
                    print(f"     Mới: {new_text[:50]}...")
            
            # Lưu kết quả ra file để xem chi tiết
            output_file = "auto_fix_result.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            print(f"\n💾 Đã lưu kết quả chi tiết vào: {output_file}")
            
        else:
            print(f"\n❌ ERROR: {response.status_code}")
            print(f"Response: {response.text[:200]}...")
            
    except requests.exceptions.RequestException as e:
        print(f"\n❌ LỖI KẾT NỐI: {e}")
        print("\n⚠️ Đảm bảo server đang chạy:")
        print("   python main.py")
        print(f"\n⚠️ URL: {API_URL}")
    
    except Exception as e:
        print(f"\n❌ LỖI KHÔNG XÁC ĐỊNH: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 80)
    print("KẾT THÚC TEST")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(test_api())