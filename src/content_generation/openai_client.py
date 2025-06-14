from openai import OpenAI
from pathlib import Path
from typing import Optional
import logging

class OpenAIClient:
    def __init__(self, api_key: str):
        """Initialize with API key and default settings"""
        self.client = OpenAI(api_key=api_key)
        self.logger = logging.getLogger(__name__)
        self.default_params = {
            'model': "gpt-4-1106-preview",
            'temperature': 0.7,
            'max_tokens': 2000
        }

    def generate_content(self, prompt: str, content_type: str, **kwargs) -> Optional[str]:
        """
        Generate content using the latest OpenAI API
        
        Args:
            prompt: Input prompt
            content_type: For logging purposes
            **kwargs: Override default params
            
        Returns:
            Generated content or None if failed
        """
        params = {**self.default_params, **kwargs}
        
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": f"You are a professional {content_type} writer."},
                    {"role": "user", "content": prompt}
                ],
                **params
            )
            self.logger.info(f"Successfully generated {content_type}")
            return response.choices[0].message.content
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
