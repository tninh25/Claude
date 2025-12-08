# services/llm/content_generation_service.py

import re
import json
from typing import List, Optional

from clients.ai_client import UniPipcAIClient
from core.ai_prompt.content_generation_prompt import REFERENCE_TEMPLATE, PROMPT_TEMPLATES, QUESTION_WITH_TOP_NEWS_AND_OUTLINE, QUESTION_WITHOUT_TOP_NEWS
from models.llm.content_generation_schemas import ContentRequest, ContentResponse, SEOArticle, ContentConfig, InternalContentRequest, ArticleBlock, OutlineItem
from models.llm.utils_schemas import NewsItem
from ..ui_config.config_service import ConfigService

class ContentGenerationService:
    """Thực hiện viết bài theo phong cách được cấu hình"""
    def __init__(self):
        self.ai_client = UniPipcAIClient()
        self.default_config = ContentConfig()
    
    def _compute_word_count(self, text: str) -> int:
        """Đếm số từ"""
        if not text:
            return 0
        
        normalized = re.sub(r"\s+", " ", text.strip())
        return len([w for w in normalized.split(" ") if w])

    def _prepare_reference_info(self, news_items: List[NewsItem]) -> str:
        """Lấy các bài để tham khảo làm KM"""
        reference_info = []
        all_images = []

        for idx, news in enumerate(news_items, 1):
            images = news.images if isinstance(news.images, list) else [news.images]
            all_images.extend(images)

            ref = REFERENCE_TEMPLATE.format(
                idx=idx,
                title=news.title,
                url=news.url,
                content_preview=news.content_preview
            )

            reference_info.append(ref)
        
        return "\n".join(reference_info), all_images
    
    def _convert_outline_to_text(self, outline: Optional[List[OutlineItem]]) -> str:
        """
        Convert outline JSON sang dạng text dễ đọc cho AI
        """
        if not outline:
            return "Không có outline"
        
        outline_lines = []
        for item in outline:
            # Tạo indent dựa trên level
            indent = "  " * (item.level - 1)
            
            # Format: H1: Title, H2: Title, H3: Title
            line = f"{indent}H{item.level}: {item.title}"
            
            # Thêm config nếu có
            if item.config:
                config_parts = []
                if item.config.get("word_count"):
                    config_parts.append(f"Số từ: {item.config['word_count']}")
                if item.config.get("keywords"):
                    keywords = ", ".join(item.config['keywords'])
                    config_parts.append(f"Keywords: {keywords}")
                if item.config.get("tone"):
                    config_parts.append(f"Tone: {item.config['tone']}")
                
                if config_parts:
                    line += f" [{', '.join(config_parts)}]"
            
            outline_lines.append(line)
        
        return "\n".join(outline_lines)
    
    def _generate_system_prompt(self, config: ContentConfig, 
                            title: Optional[str] = None,
                            outline: Optional[List[OutlineItem]] = None,
                            main_keyword: Optional[str] = None,
                            secondary_keywords: Optional[List[str]] = None) -> str:
        """Tạo system prompt với outline và keywords"""
        tone_config = ConfigService.get_tone_by_name(config.tone)
        tone_description = tone_config.description

        template = PROMPT_TEMPLATES.get(config.article_type, PROMPT_TEMPLATES["blog"])
        
        # Convert outline JSON sang text
        outline_text = self._convert_outline_to_text(outline)
        
        # Format với các tham số mới
        prompt = template.format(
            tone=tone_description,
            language=config.language,
            article_length=config.article_length,
            article_title=title or "Không có tiêu đề",
            article_outline=outline_text,
            main_keyword=main_keyword or "Không có",
            secondary_keywords=", ".join(secondary_keywords) if secondary_keywords else "Không có"
        )

        return prompt

    def render_blocks_to_html(self, blocks: list[ArticleBlock]) -> str:
        html_parts = []
        for b in blocks:
            html_parts.append(
                f'<{b.tag} data-block-id="{b.id}">{b.text}</{b.tag}>'
            )
        return "\n".join(html_parts)

    async def generate_seo_content(self, request: ContentRequest) -> ContentResponse:
        """Tạo bài SEO dựa trên từ khóa và yêu cầu của người dùng (BLOCK MODE - SAFE VERSION)"""
        try:
            # 1. Load config
            config = request.config or self.default_config

            # 2. Generate system prompt
            system_prompt = self._generate_system_prompt(
                config=config,
                title=request.title,  
                outline=request.outline,  # Giờ là List[OutlineItem]
                main_keyword=request.main_keyword,  
                secondary_keywords=request.secondary_keywords  
            )

            # 3.Prepare references
            references_text, all_images = self._prepare_reference_info(request.top_news)

            # 4. Build question
            if request.top_news:
                images_text = "\n".join([f"- {img}" for img in all_images[:15]])
                if len(all_images) > 15:
                    images_text += f"\n- ... và {len(all_images) - 15} hình ảnh khác"
                
                # Convert outline sang text cho question
                outline_text = self._convert_outline_to_text(request.outline)
                
                question_input = QUESTION_WITH_TOP_NEWS_AND_OUTLINE.format(
                    article_title=request.title or "Không có tiêu đề",
                    main_keyword=request.main_keyword or "Không có",
                    secondary_keywords=", ".join(request.secondary_keywords) if request.secondary_keywords else "Không có", 
                    article_outline=outline_text, 
                    references_text=references_text,
                    image_text=images_text
                )
            else:
                outline_text = self._convert_outline_to_text(request.outline)
                
                question_input = QUESTION_WITHOUT_TOP_NEWS.format(
                    article_title=request.title or "Không có tiêu đề",
                    main_keyword=request.main_keyword or "Không có",
                    secondary_keywords=", ".join(request.secondary_keywords) if request.secondary_keywords else "Không có", 
                    article_outline=outline_text
                )

            if config.custom_instructions:
                question_input += f"\n\nHƯỚNG DẪN ĐẶC BIỆT:\n{config.custom_instructions}"

            # 5. Get bot and language configs
            bot_config = ConfigService.get_bot_by_name(config.bot_id)
            language_config = ConfigService.get_language_by_name(config.language)

            # 6. Call AI
            ai_response = self.ai_client.ask_question_with_prompt(
                prompt=system_prompt,
                question=question_input,
                logical_bot_id=bot_config.id,
                language_text=language_config.id
            )

            if not ai_response:
                return ContentResponse(success=False, message="AI service không phản hồi")

            # 7. Parse response
            data = ai_response.get("data", {})
            raw_content = (
                data.get("answer")
                or data.get("QAMsg")
                or data.get("content")
                or ""
            )

            if not raw_content:
                return ContentResponse(success=False, message="AI không trả nội dung")

            raw_content = raw_content.strip()

            # Clean Markdown
            if raw_content.startswith("```json"):
                raw_content = raw_content[7:]
            if raw_content.startswith("```"):
                raw_content = raw_content[3:]
            if raw_content.endswith("```"):
                raw_content = raw_content[:-3]

            raw_content = raw_content.strip()

            # Parse JSON
            try:
                seo_data = json.loads(raw_content)
            except json.JSONDecodeError as e:
                return ContentResponse(
                    success=False,
                    message=f"Lỗi parse JSON từ AI: {str(e)}"
                )

            # 8. Build references
            references = []
            for news in request.top_news:
                references.append({
                    "title": news.title,
                    "url": news.url
                })

            # 9. Parse Blocks
            raw_blocks = seo_data.get("blocks", []) or []
            blocks: List[ArticleBlock] = []

            for idx, b in enumerate(raw_blocks, start=1):
                text = (b.get("text") or "").strip()
                tag = (b.get("tag") or "p").strip()
                block_id = (b.get("id") or f"{tag}-{idx}").strip()

                # word_count an toàn
                wc_raw = b.get("word_count")
                try:
                    word_count = int(wc_raw) if wc_raw is not None else None
                except (ValueError, TypeError):
                    word_count = None

                if word_count is None:
                    word_count = self._compute_word_count(text)

                blocks.append(ArticleBlock(
                    id=block_id,
                    tag=tag,
                    text=text,
                    word_count=word_count
                ))

            # 10. Render HTML
            html_content = self.render_blocks_to_html(blocks)

            # 11. Build SEO Article với generation_config
            seo_article = SEOArticle(
                title=seo_data.get("title", "").strip(),
                meta_description=seo_data.get("meta_description", "").strip(),
                blocks=blocks,
                html_content=html_content,
                keywords=seo_data.get("keywords", []),
                references=references,
                images=all_images,
                generation_config=config
            )

            return ContentResponse(
                success=True,
                article=seo_article
            )

        except Exception as e:
            return ContentResponse(
                success=False,
                message=f"Lỗi xử lý nội dung AI (SYSTEM): {str(e)}"
            )

    async def generate_internal_content(self, request: InternalContentRequest) -> ContentResponse:
        """Tạo bài SEO từ nội dung nội bộ"""
        
        # Tạo ContentRequest tương thích
        content_request = ContentRequest(
            config=request.config or self.default_config,
            top_news=[],  
            title=request.title,  
            outline=request.outline,  # Giờ là List[OutlineItem]
            main_keyword=request.main_keyword, 
            secondary_keywords=request.secondary_keywords 
        )
        
        return await self._generate_content_with_internal_reference(
            content_request, 
            request.internal_reference
        )
    
    async def _generate_content_with_internal_reference(
        self, 
        request: ContentRequest, 
        internal_reference: Optional[str] = None
    ) -> ContentResponse:
        """Internal method xử lý cả 2 trường hợp"""
        
        config = request.config or self.default_config
        system_prompt = self._generate_system_prompt(
            config=config,
            title=request.title,
            outline=request.outline,  # Giờ là List[OutlineItem]
            main_keyword=request.main_keyword,
            secondary_keywords=request.secondary_keywords
        )

        # Convert outline sang text
        outline_text = self._convert_outline_to_text(request.outline)
        
        question_input = QUESTION_WITHOUT_TOP_NEWS.format(
            article_title=request.title or "Không có tiêu đề",
            main_keyword=request.main_keyword or "Không có",
            secondary_keywords=", ".join(request.secondary_keywords) if request.secondary_keywords else "Không có", 
            article_outline=outline_text
        )
        
        # Nếu có internal_reference, thêm vào
        if internal_reference:
            question_input += f"""

THÔNG TIN NỘI BỘ THAM KHẢO (Sử dụng kiến thức này làm tài liệu tham khảo chính):
{internal_reference}
"""
        
        # Thêm hướng dẫn đặc biệt nếu có
        if config.custom_instructions:
            question_input += f"\n\nHƯỚNG DẪN ĐẶC BIỆT:\n{config.custom_instructions}"
        
        # Phần còn lại giữ nguyên
        bot_config = ConfigService.get_bot_by_name(config.bot_id)
        language_config = ConfigService.get_language_by_name(config.language)
        
        ai_response = self.ai_client.ask_question_with_prompt(
            prompt=system_prompt,
            question=question_input,
            logical_bot_id=bot_config.id,
            language_text=language_config.id
        )
        
        if not ai_response:
            return ContentResponse(
                success=False,
                message="AI service không phản hồi!!"
            )
        
        try:
            data = ai_response.get("data", {})
            raw_content = (
                data.get("answer")
                or data.get("QAMsg")
                or data.get("content")
                or ""
            )

            if not raw_content:
                return ContentResponse(success=False, message="AI không trả nội dung")

            raw_content = raw_content.strip()

            # Clean Markdown
            if raw_content.startswith("```json"):
                raw_content = raw_content[7:]
            if raw_content.startswith("```"):
                raw_content = raw_content[3:]
            if raw_content.endswith("```"):
                raw_content = raw_content[:-3]

            raw_content = raw_content.strip()

            # Parse JSON
            try:
                seo_data = json.loads(raw_content)
            except json.JSONDecodeError as e:
                return ContentResponse(
                    success=False,
                    message=f"Lỗi parse JSON từ AI: {str(e)}"
                )

            # Parse Blocks (GIỐNG NHƯ generate_seo_content)
            raw_blocks = seo_data.get("blocks", []) or []
            blocks: List[ArticleBlock] = []

            for idx, b in enumerate(raw_blocks, start=1):
                text = (b.get("text") or "").strip()
                tag = (b.get("tag") or "p").strip()
                block_id = (b.get("id") or f"{tag}-{idx}").strip()

                # word_count an toàn
                wc_raw = b.get("word_count")
                try:
                    word_count = int(wc_raw) if wc_raw is not None else None
                except (ValueError, TypeError):
                    word_count = None

                if word_count is None:
                    word_count = self._compute_word_count(text)

                blocks.append(ArticleBlock(
                    id=block_id,
                    tag=tag,
                    text=text,
                    word_count=word_count
                ))

            # Render HTML
            html_content = self.render_blocks_to_html(blocks)

            # Build SEO Article với generation_config (GIỐNG NHƯ generate_seo_content)
            seo_article = SEOArticle(
                title=seo_data.get("title", "").strip(),
                meta_description=seo_data.get("meta_description", "").strip(),
                blocks=blocks,
                html_content=html_content,
                keywords=seo_data.get("keywords", []),
                references=[],  # Không có references cho nội bộ
                images=[],  # Không có images
                generation_config=config
            )
            
            return ContentResponse(
                success=True,
                article=seo_article
            )
            
        except Exception as e:
            return ContentResponse(
                success=False,
                message=f"Lỗi xử lý nội dung AI (INTERNAL): {str(e)}"
            )