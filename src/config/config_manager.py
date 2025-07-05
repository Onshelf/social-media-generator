from pathlib import Path
from typing import Dict, List

DEFAULT_CONFIG = {
    "input_file": "/content/social-media-generator/input/Names.xlsx",
    "output_dir": "outputs",
    "platforms": ["YouTube", "X", "Facebook", "LinkedIn", "Patreon", "Medium", "Ko-fi", "Blog"],
    "openai_key": "YOUR-OPENAI-API-KEY",
    "model": "gpt-4",
    "max_figures": 5,
    "min_text_length": 500,
    "platform_requirements": {
        "Medium": 1000,
        "Patreon": 800,
        "Ko-fi": 300,
        "Blog": 700,
        "LinkedIn": 600
    },
    "timeout": 30,
    "x_char_limit": 280
}

class ConfigManager:
    def __init__(self, config: Dict = None):
        self.config = config or DEFAULT_CONFIG
    
    def get_platform_requirement(self, platform: str) -> int:
        return self.config["platform_requirements"].get(platform, self.config["min_text_length"])
    
    def get_platforms(self) -> List[str]:
        return self.config["platforms"]
    
    def get_output_dir(self) -> Path:
        return Path(self.config["output_dir"])
    
    def get_input_file(self) -> str:
        return self.config["input_file"]
    
    def get_max_figures(self) -> int:
        return self.config["max_figures"]
    
    def get_openai_key(self) -> str:
        return self.config["openai_key"]
    
    def get_timeout(self) -> int:
        return self.config["timeout"]
    
    def get_model(self) -> str:
        return self.config["model"]
    
    def get_x_char_limit(self) -> int:
        return self.config["x_char_limit"]
