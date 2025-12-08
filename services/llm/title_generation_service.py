# services/llm/title_generation_service.py

import json
from typing import List
from clients.ai_client import UniPipcAIClient
from models.llm.title_generation_schemas import TitleSuggestionRequest, TitleSuggestionResponse
from core.ai_prompt.title_generation_prompt import PROMPT_TEMPLATES, QUESTION_INPUT
from services.ui_config.config_service import ConfigService

class TitleGenerationService:
    """Gợi ý tiêu đề bài viết"""
    def __init__(self):
        self.ai_client = UniPipcAIClient()
    
    def _generate_title_prompt(self, main_keyword: str, secondary_keywords: List[str], language: str) -> str:
        """Tạo system prompt cho việc gợi ý tiêu đề"""

        secondary_keywords_text = ", ".join(secondary_keywords) if secondary_keywords else "Không có"

        system_prompt = PROMPT_TEMPLATES.format(
            main_keyword=main_keyword,
            secondary_keywords_text=secondary_keywords_text,
            lang_name=language
        )

        return system_prompt

    async def suggest_titles(self, request: TitleSuggestionRequest) -> TitleSuggestionResponse:
        """Gợi ý tiêu đề bài viết dựa trên từ khóa"""
        try:
            language_config = ConfigService.get_language_by_name(request.language)

            system_prompt = self._generate_title_prompt(
                main_keyword=request.main_keyword,
                secondary_keywords=request.secondary_keywords or [],
                language=request.language
            )

            question_input = QUESTION_INPUT.format(
                main_keyword=request.main_keyword,
                secondary_keywords_text=request.secondary_keywords,
                lang_name=request.language
            )

            ai_response = self.ai_client.ask_question_with_prompt(
                prompt=system_prompt,
                question=question_input,
                language_text=language_config.id
            )

            if not ai_response:
                return TitleSuggestionResponse(
                    success=False,
                    message="AI service không phản hồi"
                )

            data = ai_response.get("data", {})
            content = data.get("answer", "") or data.get("QAMsg", "") or data.get("content", "")

            if not content:
                return TitleSuggestionResponse(
                    success=False,
                    message="Không có nội dung nào được trả về bởi AI"
                )
            
            content = content.strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()

            titles_data = json.loads(content)
            titles = titles_data.get("titles", [])
            
            if not titles:
                return TitleSuggestionResponse(
                    success=False,
                    message="AI phản hồi nhưng không lấy được title nào"
                )
            
            # Làm sạch titles - loại bỏ các tiền tố không mong muốn
            cleaned_titles = []
            for title in titles:
                # Loại bỏ các tiền tố ngôn ngữ
                clean_title = title
                for prefix in ["vietnamese:", "tiếng việt:", "tieng viet:", "vn:"]:
                    if clean_title.lower().startswith(prefix):
                        clean_title = clean_title[len(prefix):].strip()
                
                # Loại bỏ dấu hai chấm thừa ở đầu
                if clean_title.startswith(':'):
                    clean_title = clean_title[1:].strip()
                
                # Loại bỏ dấu phẩy cuối câu
                if clean_title.endswith(','):
                    clean_title = clean_title[:-1].strip()
                    
                cleaned_titles.append(clean_title)
            
            # Đảm bảo có đúng 5 tiêu đề
            if len(cleaned_titles) < 5:
                # Nếu thiếu, có thể tạo thêm từ những cái có
                base_titles = cleaned_titles.copy()
                while len(cleaned_titles) < 5:
                    cleaned_titles.append(base_titles[len(cleaned_titles) % len(base_titles)])
            
            return TitleSuggestionResponse(
                success=True,
                titles=cleaned_titles[:5],  # Chỉ lấy 5 tiêu đề đã làm sạch
                total_suggestions=len(cleaned_titles[:5])
            )

        except Exception as e:
            return TitleSuggestionResponse(
                success=False,
                message=f"Lỗi tạo title: {str(e)}"
            )