# services/ui/config.py

from dataclasses import dataclass
from typing import Dict

@dataclass
class BotConfig:
    id: str
    name: str

@dataclass
class LanguageConfig:
    id: str
    name: str

@dataclass
class ContentTypeConfig:
    id: str
    name: str

@dataclass
class ToneConfig:
    id: str
    name: str
    description: str
    