# clients/ai_client.py

import requests
from typing import Optional, Dict, Any
from utils.config_loader import config
from utils.ai_token import load_token, save_token
from services.ui_config.config_service import ConfigService
from utils.conversation_id import generate_time_based_conversation_suffix

class UniPipcAIClient:
    """Client gọi API LUMIN AI với token được lưu vào file."""
    def __init__(self):
        ai_config = config.get("ai_client")
        self.base_url = ai_config["base_url"].rstrip("/")
        self.user_id  = ai_config["user_id"]
        self.password = ai_config["password"]
        self.company_id = ai_config["company_id"] 

        # Load token từ file 
        self.token = load_token()
    
    def get_token(self) -> Optional[str]:
        """Lấy token mới hoặc load"""
        if self.token:
            return self.token
        
        url = f"{self.base_url}/api/GetToken"
        headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }
        body = {
            "userId": self.user_id,
            "pwd"   : self.password,
            "companyId": self.company_id
        }

        try:
            response = requests.post(url, headers=headers, json=body, timeout=30)
            response.raise_for_status()

            data = response.json()
            token = data.get("data", {}).get("access_token")

            if token:
                self.token = token
                save_token(token)
                return token
            return None
        
        except requests.RequestException:
            return None
    
    def ask_question_with_prompt(self, prompt: str, question: str, logical_bot_id: Optional[str] = None, language_text: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """ Đặt câu hỏi cho chatbot
            - prompt: Mô tả nhiệm vụ, vai trò của chatbot
            - question: Câu hỏi
            - bot_id: Chỉ định models được sử dụng 
        """
        if not self.token:
            if not self.get_token():
                return None 
        
        # Sử dụng ConfigService để mapping - KHÔNG cần map lại vì đã được xử lý ở service layer
        real_bot_id = logical_bot_id or ConfigService.DEFAULT_BOT.id
        real_language_id = language_text or ConfigService.DEFAULT_LANGUAGE.id
        
        conversation_suffix = generate_time_based_conversation_suffix(300)

        url = f"{self.base_url}/api/ProxyBotQA"
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {self.token}"
        }

        body = {
            "event": "",
            "language": real_language_id,
            "prompt": prompt,
            "question": {
                "role": "user",
                "content": question,
                "images": []
            },
            "user_id": self.user_id,
            "company_id": self.company_id,
            "conversation_id": f"{self.company_id}_{self.user_id}_{real_bot_id}_{conversation_suffix}",
            "history": [],
            "stream": False,
            "uris": [],
            "temperature": 0.5
        }

        try:
            response = requests.post(url, headers=headers, json=body, timeout=60)
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            return None

if __name__ == '__main__':
    luminAI = UniPipcAIClient()
    language = "Tiếng Trung"
    bot_id = "vietnam-ocr-vlm"
    prompt = "Bạn hãy là một trợ lý chuyên nghiệp, trả lời mọi câu hỏi của người dùng"
    question = "Thủ đô Việt Nam là ?"

    response = luminAI.ask_question_with_prompt(prompt=prompt, question=question, logical_bot_id=bot_id, language_text=language)
    print(response)