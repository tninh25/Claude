# models/ui_config.py

from pydantic import BaseModel
from typing import List

class ContentKeysResponse(BaseModel):
    keys: List[str]
