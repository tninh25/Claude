# services/prompt/prompt_service.py

from models.llm.content_generation_schemas import ContentConfig
from models.llm.prompt_schemas import PromptUpdateRequest, PromptUpdateResponse

class PromptService:
    """Lấy cấu hình prompt hoặc update prompt mới"""
    def __init__(self):
        self.default_config = ContentConfig()
        
    async def update_prompt_config(self, update_request: PromptUpdateRequest) -> PromptUpdateResponse:
        """Cập nhật cấu hình prompt mặc định"""
        try:
            # Cập nhật các trường được cung cấp
            update_data = update_request.dict(exclude_unset=True)
            for key, value in update_data.items():
                if hasattr(self.default_config, key):
                    setattr(self.default_config, key, value)
            
            return PromptUpdateResponse(
                success=True,
                message="Prompt configuration updated successfully",
                current_config=self.default_config
            )
        except Exception as e:
            return PromptUpdateResponse(
                success=False,
                message=f"Failed to update prompt configuration: {str(e)}"
            )

    async def get_current_config(self) -> ContentConfig:
        """Lấy cấu hình hiện tại"""
        return self.default_config

if __name__ == '__main__':
    prompt_service = PromptService()
    print(prompt_service.get_current_config)