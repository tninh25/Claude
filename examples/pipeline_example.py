import requests
import json
from typing import Dict, Any, Optional
import time

class SEOContentTester:
    """Client để test flow: Viết bài -> Chấm điểm -> Auto-fix"""
    
    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json"
        })
    
    def generate_content(self, request_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Bước 1: Gọi API tạo bài viết
        
        Args:
            request_data: Dữ liệu request cho API /contents
            
        Returns:
            Response từ API hoặc None nếu có lỗi
        """
        url = f"{self.base_url}/api/v1/ai/contents"
        
        print("\n" + "="*80)
        print("BƯỚC 1: TẠO BÀI VIẾT")
        print("="*80)
        print(f"📤 Gọi API: {url}")
        print(f"📝 User query: {request_data.get('user_query', 'N/A')}")
        
        try:
            response = self.session.post(url, json=request_data)
            response.raise_for_status()
            
            result = response.json()
            
            if result.get("success"):
                article = result.get("article")
                print(f"✅ Tạo bài viết thành công!")
                print(f"   - Title: {article.get('title', 'N/A')[:80]}...")
                print(f"   - Blocks: {len(article.get('blocks', []))} blocks")
                print(f"   - Keywords: {', '.join(article.get('keywords', []))}")
                return result
            else:
                print(f"❌ Lỗi: {result.get('message')}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {str(e)}")
            if hasattr(e.response, 'text'):
                print(f"   Response: {e.response.text[:200]}")
            return None
    
    def analyze_seo(self, article: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Bước 2: Chấm điểm SEO
        
        Args:
            article: Bài viết từ bước 1
            
        Returns:
            Kết quả chấm điểm SEO
        """
        url = f"{self.base_url}/api/v1/seo/analyze-blocks"
        
        print("\n" + "="*80)
        print("BƯỚC 2: CHẤM ĐIỂM SEO")
        print("="*80)
        print(f"📤 Gọi API: {url}")
        
        try:
            response = self.session.post(url, json=article)
            response.raise_for_status()
            
            result = response.json()
            
            if result.get("success"):
                score_breakdown = result.get("score_breakdown", {})
                issues = result.get("issues", {})
                
                print(f"✅ Chấm điểm thành công!")
                print(f"\n📊 ĐIỂM SỐ:")
                print(f"   - Tổng điểm: {score_breakdown.get('total', 0):.1f}/100")
                print(f"   - Xếp loại: {score_breakdown.get('grade', 'N/A')}")
                print(f"   - Cấu trúc: {score_breakdown.get('structure', 0):.1f}")
                print(f"   - Keyword: {score_breakdown.get('keyword_optimization', 0):.1f}")
                print(f"   - Readability: {score_breakdown.get('readability', 0):.1f}")
                print(f"   - Technical: {score_breakdown.get('technical_seo', 0):.1f}")
                print(f"   - Content Quality: {score_breakdown.get('content_quality', 0):.1f}")
                
                print(f"\n⚠️  VẤN ĐỀ PHÁT HIỆN:")
                total_issues = 0
                for severity, issue_list in issues.items():
                    count = len(issue_list)
                    total_issues += count
                    if count > 0:
                        print(f"   - {severity.upper()}: {count} issues")
                        # In 2 issues đầu tiên để preview
                        for issue in issue_list[:2]:
                            print(f"     • {issue.get('type', 'N/A')}")
                
                print(f"   📝 Tổng: {total_issues} issues")
                
                return result
            else:
                print(f"❌ Lỗi: {result.get('message')}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {str(e)}")
            if hasattr(e.response, 'text'):
                print(f"   Response: {e.response.text[:200]}")
            return None
    
    def auto_fix_iterative(self, article: Dict[str, Any], score_result: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Bước 3: Tự động sửa SEO với iteration
        
        Args:
            article: Bài viết gốc
            score_result: Kết quả chấm điểm
            
        Returns:
            Kết quả sau khi auto-fix
        """
        url = f"{self.base_url}/api/v1/seo/auto-fix-iterative"
        
        print("\n" + "="*80)
        print("BƯỚC 3: TỰ ĐỘNG SỬA SEO (ITERATIVE)")
        print("="*80)
        print(f"📤 Gọi API: {url}")
        print("⏳ Đang xử lý (có thể mất vài phút)...")
        
        request_data = {
            "article": article,
            "score_result": score_result
        }
        
        try:
            start_time = time.time()
            response = self.session.post(url, json=request_data, timeout=300)  # 5 phút timeout
            response.raise_for_status()
            elapsed = time.time() - start_time
            
            result = response.json()
            
            print(f"✅ Auto-fix hoàn thành! (Thời gian: {elapsed:.1f}s)")
            
            # Debug: In ra cấu trúc response để xem
            print(f"\n🔍 DEBUG - Response keys: {list(result.keys())}")
            
            # Hiển thị kết quả - XỬ LÝ LINH HOẠT HƠN
            print(f"\n📈 KẾT QUẢ:")
            print(f"   - Số lần iteration: {result.get('total_iterations', 0)}")
            
            # Xử lý initial_score
            initial_score_data = result.get('initial_score', {})
            if isinstance(initial_score_data, dict):
                initial_score = initial_score_data.get('score_breakdown', {}).get('total', 0)
            elif isinstance(initial_score_data, (int, float)):
                initial_score = initial_score_data
            else:
                initial_score = 0
            
            # Xử lý final_score
            final_score_data = result.get('final_score', {})
            if isinstance(final_score_data, dict):
                final_score = final_score_data.get('score_breakdown', {}).get('total', 0)
                final_grade = final_score_data.get('score_breakdown', {}).get('grade', 'N/A')
            elif isinstance(final_score_data, (int, float)):
                final_score = final_score_data
                final_grade = 'N/A'
            else:
                final_score = 0
                final_grade = 'N/A'
            
            print(f"   - Điểm ban đầu: {initial_score:.1f}")
            print(f"   - Điểm cuối cùng: {final_score:.1f}")
            print(f"   - Cải thiện: +{result.get('score_improvement', 0):.1f} điểm")
            print(f"   - Xếp loại cuối: {final_grade}")
            
            # Thống kê tasks
            if 'iteration_history' in result:
                total_applied = sum(len(iter_data.get('applied_tasks', [])) 
                                for iter_data in result['iteration_history'])
                print(f"\n🔧 TASKS ĐÃ ÁP DỤNG:")
                print(f"   - Tổng số tasks: {total_applied}")
                
                # Hiển thị chi tiết từng iteration
                for i, iter_data in enumerate(result['iteration_history'], 1):
                    applied = len(iter_data.get('applied_tasks', []))
                    
                    # Xử lý score_after
                    score_after = iter_data.get('score_after', {})
                    if isinstance(score_after, dict):
                        iter_score = score_after.get('score_breakdown', {}).get('total', 0)
                    elif isinstance(score_after, (int, float)):
                        iter_score = score_after
                    else:
                        iter_score = 0
                        
                    print(f"   - Iteration {i}: {applied} tasks applied, score = {iter_score:.1f}")
            
            # Bài viết cuối cùng
            final_article = result.get('final_article', {})
            print(f"\n📄 BÀI VIẾT CUỐI CÙNG:")
            print(f"   - Title: {final_article.get('title', 'N/A')[:80]}...")
            print(f"   - Meta: {final_article.get('meta_description', 'N/A')[:80]}...")
            print(f"   - Blocks: {len(final_article.get('blocks', []))} blocks")
            
            return result
            
        except requests.exceptions.Timeout:
            print(f"❌ Request timeout (>5 phút)")
            return None
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {str(e)}")
            if hasattr(e.response, 'text'):
                print(f"   Response: {e.response.text[:500]}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    
    def run_full_test(self, initial_request: Dict[str, Any]) -> bool:
        """
        Chạy toàn bộ flow test
        
        Args:
            initial_request: Request data cho bước tạo bài viết
            
        Returns:
            True nếu test thành công, False nếu có lỗi
        """
        print("\n" + "🚀"*40)
        print("BẮT ĐẦU TEST FLOW: VIẾT BÀI → CHẤM ĐIỂM → AUTO-FIX")
        print("🚀"*40)
        
        # Bước 1: Tạo bài viết
        content_result = self.generate_content(initial_request)
        if not content_result or not content_result.get("success"):
            print("\n❌ TEST THẤT BẠI: Không tạo được bài viết")
            return False
        
        article = content_result.get("article")
        if not article:
            print("\n❌ TEST THẤT BẠI: Không có article trong response")
            return False
        
        time.sleep(1)  # Chờ 1s giữa các requests
        
        # Bước 2: Chấm điểm SEO
        score_result = self.analyze_seo(article)
        if not score_result or not score_result.get("success"):
            print("\n❌ TEST THẤT BẠI: Không chấm điểm được")
            return False
        
        time.sleep(1)
        
        # Bước 3: Auto-fix
        fix_result = self.auto_fix_iterative(article, score_result)
        if not fix_result:
            print("\n❌ TEST THẤT BẠI: Auto-fix lỗi")
            return False
        
        # Tổng kết
        print("\n" + "🎉"*40)
        print("TEST HOÀN THÀNH THÀNH CÔNG!")
        print("🎉"*40)
        
        initial_score = score_result.get('score_breakdown', {}).get('total', 0)
        final_score = fix_result.get('final_score', {}).get('score_breakdown', {}).get('total', 0)
        improvement = final_score - initial_score
        
        print(f"\n📊 TỔNG KẾT:")
        print(f"   ✓ Bài viết đã được tạo")
        print(f"   ✓ Điểm SEO ban đầu: {initial_score:.1f}")
        print(f"   ✓ Điểm SEO sau fix: {final_score:.1f}")
        print(f"   ✓ Cải thiện: {'+' if improvement > 0 else ''}{improvement:.1f} điểm")
        print(f"   ✓ Số lần iteration: {fix_result.get('total_iterations', 0)}")
        
        # Lưu kết quả ra file
        output_file = "test_result.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                "initial_article": article,
                "initial_score": score_result,
                "fix_result": fix_result
            }, f, ensure_ascii=False, indent=2)
        print(f"\n💾 Kết quả đã được lưu vào: {output_file}")
        
        return True


# =============================================================================
# MAIN - SỬ DỤNG
# =============================================================================

if __name__ == "__main__":
    # Khởi tạo tester
    tester = SEOContentTester(base_url="http://localhost:8080")
    
    # Dữ liệu request cho API tạo bài viết
    # BẠN CÓ THỂ THAY ĐỔI request_data này theo dữ liệu của bạn
    request_data = {
  "top_news": [{
      "rank": 1,
      "title": "GPT-5 là gì? Ưu, nhược điểm? Đánh giá ChatGPT-5 chi tiết 12/2025",
      "url": "https://dienthoaivui.com.vn/tin-tuc/gpt-5-la-gi",
      "reason": "Bài viết cung cấp đánh giá chi tiết về GPT-5, so sánh với GPT-4, giải thích nguyên lý hoạt động, các cải tiến về khả năng suy luận, đa phương tiện, tốc độ phản hồi, cũng như ứng dụng thực tế và thông tin về chi phí. Nội dung nhiều phần mục rõ ràng và đi sâu vào cấu trúc công nghệ nền tảng, phù hợp cho người quan tâm chuyên sâu.",
      "images": [
        "https://dashboard.dienthoaivui.com.vn/uploads/dashboard/headers/dich-vu-chuyen-nghiep.png",
        "https://dashboard.dienthoaivui.com.vn/uploads/dashboard/headers/tiet-kiem.png",
        "https://dashboard.dienthoaivui.com.vn/uploads/dashboard/headers/tay-nghe-gioi.png",
        "https://dashboard.dienthoaivui.com.vn/uploads/dashboard/headers/may-cu-gia-tot.png",
        "https://dashboard.dienthoaivui.com.vn/uploads/wp-content/uploads/images/6137876315eead8e73476d48d58ff6ed.png",
        "https://dashboard.dienthoaivui.com.vn/uploads/wp-content/uploads/images/1a3904abf31d14f2540d4a7cc15d73d9.png",
        "https://dashboard.dienthoaivui.com.vn/uploads/wp-content/uploads/images/501483cfdcd34ee324c85f7f3cfc4caa.png",
        "https://dashboard.dienthoaivui.com.vn/uploads/wp-content/uploads/images/8103ad0ab25fce71601fff2b2a395a87.png",
        "https://dashboard.dienthoaivui.com.vn/uploads/wp-content/uploads/images/14f93abb99dfaaaf032843eb8578bf45.png",
        "https://dashboard.dienthoaivui.com.vn/uploads/wp-content/uploads/images/77cda568eaeb12193bf22bb3d5d2888f.png"
      ],
      "content_preview": "  * [Tin công nghệ](https://dienthoaivui.com.vn/tin-tuc)\n  * GPT-5 là gì? Ưu, nhược điểm? Đánh giá ChatGPT-5 chi tiết nhất 2025\n\n\n[Tin công nghệ](https://dienthoaivui.com.vn/tin-tuc)[Hỏi đáp](https://dienthoaivui.com.vn/tin-tuc/hoi-dap)\nGPT-5 là gì? Ưu, nhược điểm? Đánh giá ChatGPT-5 chi tiết nhất 2025\n[Tin công nghệ](https://dienthoaivui.com.vn/tin-tuc)[Hỏi đáp](https://dienthoaivui.com.vn/tin-tuc/hoi-dap)\n# GPT-5 là gì? Ưu, nhược điểm? Đánh giá ChatGPT-5 chi tiết nhất 2025\n[ Trần Thanh Nhật 17/08/2025 ](https://dienthoaivui.com.vn/author/tran-thanh-nhat)\n> GPT-5 là phiên bản trí tuệ nhân tạo (AI) mới nhất của OpenAI, được dự đoán sẽ tạo ra bước đột phá lớn về khả năng hiểu ngữ cảnh, xử lý đa phương tiện và tối ưu hóa hiệu suất.\nSo với GPT-4, GPT-5 hứa hẹn mang đến trải nghiệm tương tác tự nhiên hơn, tốc độ phản hồi nhanh hơn, đồng thời mở rộng phạm vi ứng dụng từ nghiên cứu, sáng tạo nội dung, lập trình cho tới trợ lý ảo chuyên biệt. Trong bài viết này, chúng ta sẽ khám phá chi tiết GPT-5 là gì, khi nào ra mắt, có gì mới và cách sử dụng hiệu quả.\nNội dung \n  * [1. GPT-5 là gì?](https://dienthoaivui.com.vn/tin-tuc/gpt-5-la-gi#gpt-5-la-gi%3F)\n  * [2. GPT-5 khi nào ra mắt?](https://dienthoaivui.com.vn/tin-tuc/gpt-5-la-gi#gpt-5-khi-nao-ra-mat%3F)\n  * [3. GPT-5 có gì mới so với GPT-4?](https://dienthoaivui.com.vn/tin-tuc/gpt-5-la-gi#gpt-5-co-gi-moi-so-voi-gpt-4%3F)\n  * [3.1. Khả năng suy luận và giải quyết vấn đề ngang tầm chuyên gia](https://dienthoaivui.com.vn/tin-tuc/gpt-5-la-gi#kha-nang-suy-luan-va-giai-quyet-van-de-ngang-tam-chuyen-gia)\n  * [3.2. Khả năng hiểu ngữ cảnh sâu hơn](https://dienthoaivui.com.vn/tin-tuc/gpt-5-la-gi#kha-nang-hieu-ngu-canh-sau-hon)\n  * [3.3. Đa phương tiện (multimodal) mạnh mẽ hơn](https://dienthoaivui.com.vn/tin-tuc/gpt-5-la-gi#da-phuong-tien-\\(multimodal\\)-manh-me-hon)\n  * [3.4. Tốc độ phản hồi và tối ưu chi phí](https://dienthoaivui.com.vn/tin-tuc/gpt-5-la-gi#toc-do-phan-hoi-va-toi-uu-chi-phi)\n  * [4. Nguyên lý hoạt động của GPT-5 là gì?](https://dienthoaivui.com.vn/tin-tuc/gpt-5-la-gi#nguyen-ly-hoat-dong-cua-gpt-5-la-gi%3F)\n  * [4.1. Cơ chế transformer cải tiến, huấn luyện với dữ liệu lớn và đa dạng hơn](https://dienthoaivui.com.vn/tin-tuc/gpt-5-la-gi#co-che-transformer-cai-tien%2C-huan-luyen-voi-du-lieu-lon-va-da-dang-hon)\n  * [4.2. Tích hợp công nghệ Context Vectors giúp nhớ ngữ cảnh dài hơn](https://dienthoaivui.com.vn/tin-tuc/gpt-5-la-gi#tich-hop-cong-nghe-context-vectors-giup-nho-ngu-canh-dai-hon)\n  * [4.3. Áp dụng kỹ thuật fine-tuning để tùy chỉnh cho từng lĩnh vực](https://dienthoaivui.com.vn/tin-tuc/gpt-5-la-gi#ap-dung-ky-thuat-fine-tuning-de-tuy-chinh-cho-tung-linh-vuc)\n  * [5. Bảng so sánh GPT-5 với GPT-4 chi tiết nhất 12/2025](https://dienthoaivui.com.vn/tin-tuc/gpt-5-la-gi#bang-so-sanh-gpt-5-voi-gpt-4-chi-tiet-nhat-12%2F2025)\n  * [6. GPT-5 có miễn phí không?](https://dienthoaivui.com.vn/tin-tuc/gpt-5-la-gi#gpt-5-co-mien-phi-khong%3F)\n  * [7. Ứng dụng thực tế GPT-5 tác động như thế nào?](https://dienthoai"
    },
    {
      "rank": 2,
      "title": "ChatGPT-5 có gì mới? Khám phá 10 nâng cấp đỉnh cao của OpenAI",
      "url": "https://tino.vn/blog/chatgpt-5-co-gi-moi/",
      "reason": "Bài viết tổng hợp rất kỹ lưỡng về 10 nâng cấp quan trọng của ChatGPT-5, nêu bật kiến trúc hợp nhất, khả năng cá nhân hóa, xử lý đa nhiệm, tự động hóa kết nối với Gmail và Google Calendar, cùng nhiều ứng dụng mới nhất. Cách trình bày chuyên nghiệp, hình ảnh minh họa phong phú – nổi bật là ảnh về tính năng và giao diện mới, có giá trị tham khảo cao.",
      "images": [
        "https://tino.vn/assets/img/vnnic-tinogroup-1.png",
        "https://tino.vn/blog/wp-content/uploads/2025/07/logo.png",
        "https://tino.vn/blog/wp-content/uploads/2025/12/cach-chia-cot-trong-wordpress-cover-150x150.png",
        "https://tino.vn/blog/wp-content/themes/wikitino/images/news.svg",
        "https://tino.vn/blog/wp-content/uploads/2025/12/web-scraper-de-crawler-tot-nhat-cover-150x150.png",
        "https://tino.vn/blog/wp-content/uploads/2025/12/sua-loi-Error-Establishing-A-Database-Connection-trong-WordPress-cover-150x150.png",
        "https://tino.vn/blog/wp-content/uploads/2025/12/cach-su-dung-scraper-api-voi-n8n-cover-150x150.png",
        "https://tino.vn/blog/wp-content/uploads/2025/11/cach-xoa-chu-powered-by-wordpress-cover-150x150.png",
        "https://tino.vn/blog/wp-content/uploads/2025/08/chatgpt-5-co-gi-moi-1.png"
      ],
      "content_preview": "# ChatGPT-5 có gì mới? 10 nâng cấp của OpenAI khiến dân công nghệ “phát sốt”\nTác giả: [Đông Tùng](https://tino.vn/blog/author/dong-tung/) Ngày cập nhật: 12/08/2025 Chuyên mục: [Công cụ AI](https://tino.vn/blog/cong-cu-ai/)\nDisclosure \nWebsite Tino blog được cung cấp bởi Tino Group. Truy cập và sử dụng website đồng nghĩa với việc bạn đồng ý với các điều khoản và điều kiện trong [chính sách bảo mật - điều khoản sử dụng nội dung](https://tino.vn/blog/chatgpt-5-co-gi-moi/chinh-sach-bao-mat-cua-wiki-tino-org). Wiki.tino.org có thể thay đổi điều khoản sử dụng bất cứ lúc nào. Việc bạn tiếp tục sử dụng Tino blog sau khi thay đổi có nghĩa là bạn chấp nhận những thay đổi đó. \nWhy Trust Us \nCác bài viết với hàm lượng tri thức cao tại Tino blog được tạo ra bởi các chuyên viên Marketing vững chuyên môn và được kiểm duyệt nghiêm túc theo [ chính sách biên tập](https://wiki.tino.org/chinh-sach-bien-tap-cua-wiki-tino-org/) bởi đội ngũ biên tập viên dày dặn kinh nghiệm. Mọi nỗ lực của chúng tôi đều hướng đến mong muốn mang đến cho cộng đồng nguồn thông tin chất lượng, chính xác, khách quan, đồng thời tuân thủ các tiêu chuẩn cao nhất trong báo cáo và xuất bản. \n**Ngày 7/8/2025, OpenAI chính thức ra mắt ChatGPT-5 – phiên bản được giới công nghệ đánh giá là “bước nhảy vọt” về trí tuệ nhân tạo. Không chỉ thông minh hơn, chính xác hơn, ChatGPT-5 còn mang đến nhiều tính năng hấp dẫn. Vậy ChatGPT-5 có gì mới? Bài viết này sẽ giúp bạn khám phá toàn bộ điểm mới nổi bật của ChatGPT-5 và lý do tại sao đây là công cụ AI đáng trải nghiệm nhất hiện nay.**\n##  Tổng quan về ChatGPT-5\n###  **ChatGPT-5 là gì?**\n[ChatGPT-5](https://openai.com/index/introducing-gpt-5/) là phiên bản mới nhất của mô hình [ChatGPT](https://tino.vn/blog/chatgpt-la-gi/) do OpenAI phát triển. Với kiến trúc transformer tiên tiến, ChatGPT-5 được thiết kế để hiểu và tạo ra văn bản giống con người một cách tự nhiên và mạch lạc hơn bao giờ hết. \nMục tiêu chính của phiên bản này là nâng cao khả năng lý luận, cải thiện bộ nhớ, và mang đến trải nghiệm cá nhân hóa sâu sắc hơn cho người dùng. Những cải tiến vượt bậc về kiến trúc và dữ liệu huấn luyện giúp cho ChatGPT-5 không chỉ đơn thuần là một công cụ tạo văn bản, mà còn là một trợ lý AI đa năng, có khả năng thực hiện nhiều tác vụ phức tạp từ sáng tạo nội dung, lập trình, đến phân tích dữ liệu và tương tác xã hội. \n**ChatGPT-5 là gì?**\nChatGPT-5 đóng vai trò kế nhiệm trực tiếp và thay thế hoàn toàn các phiên bản trước như GPT-4, GPT-4o và các biến thể liên quan. Sự ra đời của phiên bản này đánh dấu một cột mốc quan trọng trong hành trình phát triển của trí tuệ nhân tạo đàm thoại, mở ra nhiều tiềm năng ứng dụng mới trong mọi lĩnh vực của đời sống và công việc. \n###  **ChatGPT-5 có gì mới? 10 nâng cấp “đỉnh cao” của ChatGPT-5**\n####  #1. Thông minh hơn – Tự động “nghiên cứu sâu” khi cần\nĐiểm đột phá lớn nhất của GPT-5 chính là kiến trúc hợp nhất độc đáo. Thay vì chỉ dựa vào một mô hình duy nhất, GPT-5 hoạt động như “hai bộ não trong một”: \n  * Một mô hình nhẹ và nh"
    },
    {
      "rank": 3,
      "title": "Chat GPT-5 là gì? Khi nào ra mắt? Có gì nổi bật?",
      "url": "https://dienmaycholon.com/kien-thuc/chat-gpt-5-co-gi-moi",
      "reason": "Bài viết cập nhật đầy đủ về GPT-5: định nghĩa, các tính năng nổi bật (AI đa phương thức, lý luận, giảm ảo giác thông tin, cửa sổ ngữ cảnh mở rộng,...), lộ trình ra mắt và khả năng ứng dụng trên thị trường. Có các ảnh thiết kế đẹp về chương trình khuyến mãi, các banner liên quan – vừa minh họa, vừa tăng tính nhận diện đi kèm kiến thức cốt lõi.",
      "images": [
        "https://cdn11.dienmaycholon.vn/filewebdmclnew/DMCL21/Picture//Tm/Tm_picture_346/banner-khuyen-m_905_1920.png.webp",
        "https://cdn11.dienmaycholon.vn/filewebdmclnew/DMCL21/Picture/Tm/Tm_menu_1300/-sale--khong-lo_481_150.png.webp",
        "https://cdn11.dienmaycholon.vn/filewebdmclnew/DMCL21/Picture/Tm/Tm_menu_1410/thu-cu-doi-moi-_568_150.png.webp",
        "https://cdn11.dienmaycholon.vn/filewebdmclnew/DMCL21/Picture/Tm/Tm_menu_1411/doi-cu-lay-tu-l_47_150.png.webp",
        "https://cdn11.dienmaycholon.vn/filewebdmclnew/DMCL21/Picture/Tm/Tm_menu_1421/tra-gop-uu-dai-_873_150.png.webp",
        "https://cdn11.dienmaycholon.vn/filewebdmclnew/DMCL21/Picture/Tm/Tm_menu_1427/bo-phieu-qua-ta_407_150.png.webp",
        "https://cdn11.dienmaycholon.vn/filewebdmclnew/DMCL21/Picture/Tm/Tm_menu_1425/-cho-hssv-tai-x_117_150.png.webp",
        "https://cdn11.dienmaycholon.vn/filewebdmclnew/DMCL21/Picture/Tm/Tm_menu_1302/san-pham-noi-ba_882_150.png.webp",
        "https://cdn11.dienmaycholon.vn/filewebdmclnew/DMCL21/Picture/Tm/Tm_menu_1303/thiet-bi-giai-t_861_150.png.webp",
        "https://cdn11.dienmaycholon.vn/filewebdmclnew/DMCL21/Picture/Tm/Tm_menu_1412/thiet-bi-dien-l_282_150.png.webp"
      ],
      "content_preview": "  * [Món ngon mỗi ngày](https://dienmaycholon.com/mon-ngon \"Món ngon mỗi ngày\")\n\n\n  * AI\n  * [Kiến thức](https://dienmaycholon.com/kien-thuc/chat-gpt-5-co-gi-moi)\n    * [Mẹo vặt đời sống](https://dienmaycholon.com/kien-thuc/meo-vat-doi-song)\n    * [Du lịch - Khám phá](https://dienmaycholon.com/kien-thuc/du-lich-kham-pha)\n\n\n# Cập nhật thông tin về Chat GPT-5: Ngày ra mắt, tính năng nổi bật\nTác giả: Diệp LạcNgày cập nhật: 10/06/2025 14:16:17Tác giả: Diệp Lạc14480\nXem nhanh \n[1. Chat GPT-5 là gì?](https://dienmaycholon.com/kien-thuc/chat-gpt-5-co-gi-moi#titletab1)\n[2. Cập nhật một số tính năng nổi bật của Chat GPT-5](https://dienmaycholon.com/kien-thuc/chat-gpt-5-co-gi-moi#titletab2)\n[Chuyển từ đàm thoại sang lý luận](https://dienmaycholon.com/kien-thuc/chat-gpt-5-co-gi-moi#titletab2_1)[AI đa phương thức ](https://dienmaycholon.com/kien-thuc/chat-gpt-5-co-gi-moi#titletab2_2)[Từ Chatbot đến AI Agent](https://dienmaycholon.com/kien-thuc/chat-gpt-5-co-gi-moi#titletab2_3)[Lý luận tốt hơn, ít ảo giác hơn](https://dienmaycholon.com/kien-thuc/chat-gpt-5-co-gi-moi#titletab2_4)[Cửa sổ ngữ cảnh mở rộng](https://dienmaycholon.com/kien-thuc/chat-gpt-5-co-gi-moi#titletab2_5)\n[3. Chat GPT-5 dự kiến ra mắt khi nào?](https://dienmaycholon.com/kien-thuc/chat-gpt-5-co-gi-moi#titletab3)\nXem thêm \nSau khi trình làng Chat GPT-4.5 vào ngày 28/02/2025, OpenAI được cho là đang phát triển phiên bản GPT-5 với những nâng cấp vượt trội. Trong bài viết dưới đây, Siêu Thị Điện Máy - Nội Thất Chợ Lớn sẽ cập nhật thông tin về ngày ra mắt và tính năng của [Chat GPT-5](https://dienmaycholon.com/kien-thuc/chat-gpt-5-co-gi-moi). Cùng theo dõi nhé!\n_Cập nhật thông tin về Chat GPT-5_\n## 1. Chat GPT-5 là gì?\nChat GPT-5 là mô hình trí tuệ nhân tạo tiếp theo được OpenAI phát triển với những cải tiến đáng kể về khả năng xử lý ngôn ngữ tự nhiên, tư duy logic và sáng tạo nội dung. Khác với các phiên bản GPT tiền nhiệm, GPT-5 mang đến trải nghiệm tương tác liền mạch khi loại bỏ yêu cầu chuyển đổi mô hình cho các tác vụ riêng biệt. Đồng thời, nó cũng cho phép tương tác nâng cao giữa các loại đầu vào khác nhau.\n_Chat GPT-5 là mô hình trí tuệ nhân tạo do OpenAI phát triển_\n**Xem thêm:**[Nguyên nhân và cách xử lý lỗi trên ChatGPT đơn giản, hiệu quả mà bạn nên biết](https://dienmaycholon.com/kien-thuc/huong-dan-khac-phuc-loi-chatgpt)\n## 2. Cập nhật một số tính năng nổi bật của Chat GPT-5\n### Chuyển từ đàm thoại sang lý luận\nOpenAI dự kiến tích hợp nhiều kiến trúc hơn cho Chat GPT-5 thay vì chỉ tăng số lượng tham số. Theo đó, mô hình AI mới khả năng sẽ kết hợp các thành phần chuyên biệt như lý luận có cấu trúc của o3 vào một hệ thống thống nhất.\n_OpenAI dự kiến tích hợp nhiều kiến trúc hơn cho Chat GPT-5_\n### AI đa phương thức \nChat GPT-5 có thể được tinh chỉnh mô hình giọng nói, đồng thời bổ sung khả năng xử lý video, xây dựng trên SORA, mô hình chuyển văn bản thành video. Nhiều nguồn tin rò rỉ cho rằng, OpenAI đang nghiên cứu tích hợp tìm kiếm sâu hơn, cho phép Chat GPT-5 truy xuất và áp dụng thôn"
    }],
  "user_query": "chatgpt 5.0 có gì hot",
  "target_language": "Tiếng Việt",
  "config": {
    "bot_id": "GPT-4.1",
    "article_length": "1500-1800",
    "tone": "Chuyên Nghiệp",
    "article_type": "Blog",
    "language": "Tiếng Việt",
    "custom_instructions": "string"
  }
}
    
    # Chạy test
    success = tester.run_full_test(request_data)
    
    if success:
        print("\n✅ ALL TESTS PASSED!")
        exit(0)
    else:
        print("\n❌ TESTS FAILED!")
        exit(1)