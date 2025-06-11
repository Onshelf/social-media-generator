import openai
from pathlib import Path
from typing import Dict, Optional
import logging

class OpenAIClient:
    def __init__(self, api_key: str):
        """Initialize with API key and default settings"""
        openai.api_key = api_key
        self.logger = logging.getLogger(__name__)
        self.default_params = {
            'model': "gpt-4-1106-preview",  # Updated to latest model
            'temperature': 0.7,
            'max_tokens': 2000
        }

    def generate_content(self, prompt: str, content_type: str, **kwargs) -> Optional[Dict]:
        """
        Generate content with proper error handling
        
        Args:
            prompt: The input prompt
            content_type: Story/Post/Blog (for logging)
            **kwargs: Override default params
            
        Returns:
            API response or None if failed
        """
        params = {**self.default_params, **kwargs}
        
        try:
            response = openai.ChatCompletion.create(
                messages=[
                    {"role": "system", "content": f"You are a professional {content_type} writer."},
                    {"role": "user", "content": prompt}
                ],
                **params
            )
            self.logger.info(f"Successfully generated {content_type}")
            return response
        except Exception as e:
            self.logger.error(f"Failed to generate {content_type}: {str(e)}")
            return None

    def save_to_file(self, content: str, output_path: Path) -> bool:
        """Save generated content to file"""
        try:
            output_path.write_text(content)
            self.logger.info(f"Saved content to {output_path}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to save file: {str(e)}")
            return False
