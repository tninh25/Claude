# utils/ai_token.py

import os
import json
from typing import Optional

TOKEN_FILE = "token.json"

def save_token(token: str):
    with open(TOKEN_FILE, 'w', encoding="utf-8") as f:
        json.dump({"access_token": token}, f, ensure_ascii=False, indent=4)

def load_token() -> Optional[str]:
    if not os.path.exists(TOKEN_FILE):
        return None
    try:
        with open(TOKEN_FILE, 'r', encoding="utf-8") as f:
            data = json.load(f)
            return data.get("access_token")
    except Exception:
        return None
    