# services/llm/news_filtering_service.py

import json
import re
from typing import List, Optional

from clients.ai_client import UniPipcAIClient
from core.ai_prompt.news_filtering_prompt import REFERENCE_TEMPLATE, PROMPT_TEMPLATES, QUESTION_TEMPLATES
from models.llm.news_filtering_schemas import NewsFilteringRequest, NewsFilteringResponse, OutlineItem
from models.llm.utils_schemas import NewsItem, ArticleContent
from services.crawl.image_deduplication_service import ImageDeduplicationService

class NewsFilteringService:
    """Phân tích nội dung các tin tức -> chọn nội dung phù hợp và tạo outline"""
    
    def __init__(self):
        self.ai_client = UniPipcAIClient()
        self.image_service = ImageDeduplicationService()
    
    def _prepare_news_data(self, articles: List[ArticleContent]) -> str:
        """Chuẩn hóa dữ liệu tin tức - rút gọn để tiết kiệm token"""
        news_data = []
        for idx, article in enumerate(articles, 1):
            content_preview = article.content_preview[:300] if article.content_preview else ""
            
            ref = REFERENCE_TEMPLATE.format(
                idx=idx,
                title=article.title[:80],
                url=article.url,
                content_preview=content_preview
            )
            news_data.append(ref)
        
        return "\n".join(news_data)
    
    def _clean_ai_response(self, content: str) -> str:
        """Làm sạch response từ AI để parse JSON"""
        if not content:
            return ""
            
        content = content.strip()
        
        # Loại bỏ markdown code blocks
        if content.startswith("```json"):
            content = content[7:]
        elif content.startswith("```"):
            content = content[3:]
        
        if content.endswith("```"):
            content = content[:-3]
        
        content = content.strip()
        
        if content.startswith('\n'):
            content = content[1:]
            
        return content
    
    def _process_images_for_article(self, article: ArticleContent) -> List[str]:
        """Xử lý hình ảnh cho một article: lọc public và deduplicate"""
        if not article.images:
            return []
        
        best_images = self.image_service.get_best_images(article.images, max_images=3)
        return best_images
    
    def _parse_outline_items(self, outline_data) -> Optional[List[OutlineItem]]:
        """Parse outline từ JSON - giữ nguyên logic gốc"""
        if not outline_data:
            return None
        
        try:
            # Nếu là list -> parse trực tiếp
            if isinstance(outline_data, list):
                outline_items = []
                for item in outline_data:
                    outline_items.append(OutlineItem(
                        id=item.get("id", ""),
                        level=item.get("level", 2),
                        title=item.get("title", ""),
                        order=item.get("order", 0)
                    ))
                return outline_items if outline_items else None
            
            return None
            
        except Exception as e:
            print(f"Error parsing outline: {e}")
            return None
    
    async def filtering_news(self, request: NewsFilteringRequest) -> NewsFilteringResponse:
        """Thực hiện lọc tin và tạo outline bài viết"""
        if not request.articles:
            return NewsFilteringResponse(
                success=False,
                selected_news=[],
                article_outline=None,
                total_analyzed=0
            )
        
        # Format prompt với thông tin mới
        system_prompt = PROMPT_TEMPLATES.format(
            article_title=request.article_title,
            main_keyword=request.main_keyword
        )
        
        news_text = self._prepare_news_data(request.articles)
        question_input = QUESTION_TEMPLATES.format(
            article_title=request.article_title,
            main_keyword=request.main_keyword,
            secondary_keywords=", ".join(request.secondary_keywords) if request.secondary_keywords else "Không có",
            news_text=news_text,
        )
        
        # Gọi AI
        ai_response = self.ai_client.ask_question_with_prompt(
            prompt=system_prompt,
            question=question_input
        )
        
        if not ai_response:
            return NewsFilteringResponse(
                success=False,
                selected_news=[],
                article_outline=None,
                total_analyzed=len(request.articles)
            )
        
        try:
            # Xử lý response
            data = ai_response.get("data", {})
            content = data.get("answer", "") or data.get("QAMsg", "")
            
            if not content:
                return NewsFilteringResponse(
                    success=False,
                    selected_news=[],
                    article_outline=None,
                    total_analyzed=len(request.articles)
                )
            
            # Clean response
            content = self._clean_ai_response(content)
            
            # Parse JSON
            result = json.loads(content)
            
            # Lấy selected news và outline từ response
            filtered_news = result.get("selected_news", [])
            article_outline_data = result.get("article_outline")
            
            # Parse outline
            parsed_outline = self._parse_outline_items(article_outline_data)
            
            # Tạo mapping để lấy thông tin gốc
            url_to_article = {article.url: article for article in request.articles}
            
            # Chuẩn bị selected news với xử lý hình ảnh
            selected_news = []
            for news_item in filtered_news[:request.top_k]:
                news_url = news_item.get("url", "")
                original_article = url_to_article.get(news_url)
                
                if not original_article:
                    continue
                
                # Xử lý hình ảnh: lọc public và deduplicate
                processed_images = self._process_images_for_article(original_article)
                
                selected_news.append(NewsItem(
                    rank=news_item.get("rank", 0),
                    title=news_item.get("title", ""),
                    url=news_url,
                    images=processed_images,
                    content_preview=original_article.content_preview
                ))
            
            return NewsFilteringResponse(
                success=True,
                selected_news=selected_news,
                article_outline=parsed_outline,
                article_title=request.article_title, 
                main_keyword=request.main_keyword,  
                secondary_keywords=request.secondary_keywords, 
                total_analyzed=len(request.articles)
            )
            
        except json.JSONDecodeError:
            # Thử tìm JSON trong content nếu parse lỗi
            if 'content' in locals():
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    try:
                        result = json.loads(json_match.group())
                        
                        filtered_news = result.get("selected_news", [])
                        article_outline_data = result.get("article_outline")
                        parsed_outline = self._parse_outline_items(article_outline_data)
                        
                        url_to_article = {article.url: article for article in request.articles}
                        selected_news = []
                        
                        for news_item in filtered_news[:request.top_k]:
                            news_url = news_item.get("url", "")
                            original_article = url_to_article.get(news_url)
                            
                            if original_article:
                                processed_images = self._process_images_for_article(original_article)
                                
                                selected_news.append(NewsItem(
                                    rank=news_item.get("rank", 0),
                                    title=news_item.get("title", ""),
                                    url=news_url,
                                    images=processed_images,
                                    content_preview=original_article.content_preview
                                ))
                        
                        return NewsFilteringResponse(
                            success=True,
                            selected_news=selected_news,
                            article_outline=parsed_outline,
                            article_title=request.article_title,
                            main_keyword=request.main_keyword,
                            secondary_keywords=request.secondary_keywords,
                            total_analyzed=len(request.articles)
                        )
                    except:
                        pass
            
            return NewsFilteringResponse(
                success=False,
                selected_news=[],
                article_outline=None,
                total_analyzed=len(request.articles)
            )
        except Exception as e:
            print(f"Error in filtering_news: {e}")
            return NewsFilteringResponse(
                success=False,
                selected_news=[],
                article_outline=None,
                total_analyzed=len(request.articles)
            )