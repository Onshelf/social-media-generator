from openai import OpenAI
from pathlib import Path
from typing import Optional

class OpenAIClient:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def generate_content(self, prompt: str, content_type: str, **kwargs) -> Optional[str]:
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": f"You are a {content_type} writer."},
                    {"role": "user", "content": prompt}
                ],
                **kwargs
            )
            return response.choices[0].message.content
        except Exception:
            return None

    def save_to_file(self, content: str, output_path: Path) -> bool:
        try:
            output_path.write_text(content)
            return True
        except Exception:
            return False
