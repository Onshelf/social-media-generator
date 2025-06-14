from openai import OpenAI
from pathlib import Path
from typing import Optional
import time

class OpenAIClient:
    def __init__(self, api_key: str):
        """
        Initialize the OpenAI client.
        Note: Model is specified in generate_content() calls, not during init
        """
        if not api_key.startswith('sk-'):
            raise ValueError("Invalid OpenAI API key format")
        self.client = OpenAI(api_key=api_key)
        self.max_retries = 3
        self.retry_delay = 2

    def generate_content(self, prompt: str, model: str = "gpt-4o-mini-2024-07-18", **kwargs) -> Optional[str]:
        """Generate content with automatic retries"""
        for attempt in range(self.max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=model,  # Model specified here
                    messages=[{"role": "user", "content": prompt}],
                    **kwargs
                )
                return response.choices[0].message.content
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                continue
        return None

    def save_to_file(self, content: str, output_path: Path) -> bool:
        """Save content to file with directory creation"""
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(content)
            return True
        except Exception as e:
            print(f"Failed to save file: {str(e)}")
            return False
