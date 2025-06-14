from pathlib import Path
from typing import Optional
from .openai_client import OpenAIClient

class LegacyPostGenerator:
    def __init__(self, client: OpenAIClient):
        self.client = client

    def generate_post(self, figure_name: str, source_text: str, output_path: Path) -> bool:
        prompt = f"""Create a Facebook post about {figure_name} with:
1. HOOK: Start with a question
2. BODY: 2 short paragraphs (40-60 words each)
3. STYLE: Conversational, use emojis
4. HASHTAGS: #{figure_name.replace(' ','')} #History #Legacy

SOURCE MATERIAL:
{source_text[:2000]}"""

        response = self.client.generate_content(
            prompt=prompt,
            model="gpt-4o-mini-2024-07-18",
            max_tokens=300
        )

        if response:
            content = f"👍 {figure_name} Facebook Post\n\n{response}"
            return self.client.save_to_file(content, output_path)
        return False
