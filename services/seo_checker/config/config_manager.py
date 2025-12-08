# services/seo_checker/config/config_manager.py

"""
    Config Manager - Load và quản lý cấu hình từ file
"""

import os
import yaml
import logging
from typing import Dict, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class ConfigManager:
    """Quản lý cấu hình - CHỈ LOAD TỪ FILE**"""

    def __init__(self, config_dir):
        
        self.config_dir = Path(config_dir)
        self.config = self._load_all_configs()

        if not self.config:
            raise ValueError(f"Không thể load config từ thư mục: {self.config_dir}")
    
    def _load_all_configs(self) -> Dict:
        """Load tất cả file config từ thư mục config"""
        config = {}

        # Load từng file config
        config_files = {
            'scoring_rules.yaml': ['default_thresholds'],
            'thresholds.yaml': ['industry_thresholds'],
            'weights.yaml': [
                'scoring_weights', 
                'issue_severity', 
                'issue_penalties', 
                'bonus_points'
            ]
        }

        for filename, keys in config_files.items():
            filepath = self.config_dir / filename

            if filepath.exists():
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        file_config = yaml.safe_load(f)

                    # Chỉ thêm các key hợp lệ
                    for key in keys:
                        if key in file_config:
                            config[key] = file_config[key]
                        else:
                            logger.warning(f"Key '{key}' không tìm thấy trong {filename}")
                    
                    logger.info(f"Loaded config from {filename}")
                
                except Exception as e:
                    logger.error(f"Lỗi khi load {filename}: {e}")
            
            else:
                logger.warning(f"File config không tồn tại: {filepath}")
        
        # Validate config cần thiết
        required_keys = ['default_thresholds', 'scoring_weights', 'issue_penalties']
        missing_keys = [key for key in required_keys if key not in config]
        
        if missing_keys:
            raise ValueError(f"Thiếu config bắt buộc: {missing_keys}")
        
        return config
    def get_thresholds(self, industry: Optional[str] = None) -> Dict:
        """Lấy ngưỡng theo ngành hoặc mặc định"""
        thresholds = self.config['default_thresholds'].copy()

        if industry and 'industry_thresholds' in self.config:
            industry_config = self.config['industry_thresholds'].get(industry, {})
            # Deep merge
            for key, value in industry_config.items():
                if key in thresholds and isinstance(value, dict):
                    thresholds[key].update(value)
                else:
                    thresholds[key] = value
        
        return thresholds

    def get_penalty(self, issue_type: str) -> int:
        """Lấy điểm phạt cho issue"""
        penalty = self.config.get('issue_penalties', {}).get(issue_type, 0)

        #  Chuyển sang số dương
        if penalty < 0:
            return abs(penalty)
        return penalty
    
    def get_bonus(self, bonus_type: str) -> int:
        """Lấy điểm thưởng"""
        return self.config.get('bonus_points', {}).get(bonus_type, 0)
    
    def get_issue_severity(self, issue_type: str) -> str:
        """Lấy mức độ nghiêm trọng của issue"""
        severity_config = self.config.get('issue_severity', {})

        for severity, issues in severity_config.items():
            if issue_type in issues:
                return severity
        
        return 'info'
    
    def get_scoring_weights(self) -> Dict[str, int]:
        """Lấy trọng số chấm điểm"""
        return self.config.get('scoring_weights', {
            'structure': 20,
            'keyword_optimization': 25, 
            'readability': 20,
            'technical_seo': 15,
            'content_quality': 20
        })
    
if __name__ == '__main__':
    config = ConfigManager("D:/C_to_D/Marketing-Platform/Ver 2.0/learn_architecture/core/score_yaml")

    # weights
    # weights = config.get_scoring_weights()
    # print(weights)

    # max_score = weights.get('structure', 20)
    # print('max score: ', max_score)

    # bonus
    # bonus = config.get_bonus('optimal_word_count')
    # print('bonus: ', bonus)

    # issue severity
    # severity = config.get_issue_severity('missing_h1')
    # print(severity)

    # thresholds
    # thresholds = config.get_thresholds()
    # wc_config = thresholds.get('word_count', {})
    # print(wc_config)

    # structure
    # weights = config.get_scoring_weights()
    # print(weights)
    # max_score = weights.get('structure')
    # print(max_score)

    # h2
    thresholds = config.get_thresholds()
    h2 =  thresholds.get('headings', {}).get('h2_min', 3)
    print(h2)