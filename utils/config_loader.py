"""
Config Loader Module
"""

import yaml
from typing import Dict, Any

class Config:
    def __init__(self, config_path="config.yaml"):
        self.config_path = config_path
        self._config     = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load config từ file YAML"""
        try:
            with open(self.config_path, "r", encoding="utf-8") as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            raise Exception(f"Config file not found: {self.config_path}")
        except yaml.YAMLError as e:
            raise Exception(f"Error parsing config file: {e}")

    def get(self, key: str, default=None) -> Any:
        """Lấy giá trị config theo key với dot notation"""
        keys = key.split('.')
        value = self._config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, {})
            else:
                return default
        return value if value != {} else default
    
    def get_seo_config(self) -> Dict[str, Any]:
        """Lấy config cho SEO Checker"""
        return self.get('seo_checker', {})
    
    def get_wordpress_config(self) -> Dict[str, Any]:
        """Lấy config cho WordPress"""
        return self.get('wordpress', {})

# -----------------------------------------------
# 📌 CONFIG GLOBAL — singleton instance
# -----------------------------------------------
_config_instance = None

def get_config(config_path: str = "config.yaml") -> Config:
    """Lấy instance config (singleton pattern)"""
    global _config_instance
    if _config_instance is None:
        _config_instance = Config(config_path)
    return _config_instance

def load_config(config_path: str = "config.yaml") -> Dict[str, Any]:
    """Load config trực tiếp (cho backward compatibility)"""
    config = get_config(config_path)
    return config._config

# Global config instance cho import trực tiếp
config = get_config()

# -----------------------------------------------
# 📌 CONFIG TRONG __main__ — chỉ chạy khi chạy file trực tiếp
# -----------------------------------------------
if __name__ == "__main__":
    local_config = Config()
    print("Config structure:", local_config._config)
    
    # Test các key
    print("\nSEO Config:", local_config.get_seo_config())
    print("WordPress Config:", local_config.get_wordpress_config())