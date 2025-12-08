import json
import requests
from time import time  # Thay đổi ở đây
# Xóa dòng: from datetime import time

class UniPipcAIClient:
    def __init__(self, base_url: str, user_id: str, password: str, company_id: str):
        self.base_url = base_url.rstrip("/")
        self.user_id = user_id
        self.password = password
        self.company_id = company_id
        self.token = None

    def get_token(self):
        """
        Call GetToken API to retrieve bearer token.
        """
        url = f"{self.base_url}/api/GetToken"  # api/GetToken
        headers = {"accept": "application/json", "content-type": "application/json"}
        payload = {
            "userId": self.user_id,
            "pwd": self.password,
            "companyId": self.company_id,
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            print("Token Response:")
            print(json.dumps(data, indent=2, ensure_ascii=False))

            token_data = data.get("data", {})
            self.token = token_data.get("access_token")

            if self.token:
                print("Token retrieved successfully!")
                return self.token
            else:
                print("access_token not found in response!")
                return None

        except requests.RequestException as e:
            print("Error while retrieving token:", e)
            return None

    def _clean_up_final_response(self, final_response: dict) -> dict:
        """
        Clean up the final response by removing unnecessary fields.
        """
        # get the message and image uri
        messages = final_response.get("messages", [])
        cleaned_messages = []
        for message in messages:
            if message.get("type") == "text":
                data = message.get("data", {})
                cleaned_message = {"type": "text", "data": {}}
                cleaned_message["data"]["message"] = data.get("message", "")
                if data.get("media_type") == "image":
                    cleaned_message["data"]["media_type"] = "image"
                    cleaned_message["data"]["uri"] = data.get("uri", "")
                cleaned_messages.append(cleaned_message)
        return {"messages": cleaned_messages}

    def ask_question(self, question_text: str, bot_id: str = "bot-1739") -> dict:
        """
        Send a question to the AI bot using ProxyBotQA API.
        """
        if not self.token:
            print("Token not found. Please call get_token() first.")
            return None

        url = f"{self.base_url}/api/ProxyBotQA"
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {self.token}",
        }

        body = {
            "event": "",
            "language": "2",
            "prompt": "",
            "question": {"role": "user", "content": question_text, "images": []},
            "user_id": self.user_id,
            "company_id": self.company_id,
            "conversation_id": f"{self.company_id}_{self.user_id}_{bot_id}_{int(time())}",  # Sửa thành time() thay vì time.timestamp()
            "history": [],
            "stream": True,
            "uris": [],
            "temperature": 0.5,
        }

        try:
            print("Sending SSE request to ProxyBotQA...")
            print("Request Body:")
            print(json.dumps(body, indent=2, ensure_ascii=False))

            with requests.post(
                url, headers=headers, json=body, stream=True
            ) as response:
                response.raise_for_status()
                final_result = None
                for line in response.iter_lines(decode_unicode=True):
                    if line and line.startswith("data:"):
                        try:
                            data_str = line[len("data:") :].strip()
                            data_json = json.loads(data_str)
                            if data_json.get("type") == "final_response":
                                final_result = data_json.get("data")
                                break
                        except Exception as e:
                            print("Error parsing SSE line:", e)
                if final_result:
                    print("Final SSE Response:")
                    print(json.dumps(final_result, indent=2, ensure_ascii=False))
                    final_result = self._clean_up_final_response(final_result)
                    return final_result
                else:
                    print("No final_response found in SSE stream.")
                    return None

        except requests.RequestException as e:
            if hasattr(e, "response") and e.response is not None:
                print("Server returned an error response:", e.response.text)
            else:
                print("Error during request:", e)
            return None


if __name__ == "__main__":
    client = UniPipcAIClient(
        base_url="https://lumineai.pic.net.tw",
        user_id="ngocninh",
        password="ngocninh@VietSon150",
        company_id="99990013",
    )
    token = client.get_token()

    if token:
        result = client.ask_question("Please generate an image of a gaming PC ASUS desktop with coffes.")