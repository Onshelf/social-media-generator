from pathlib import Path
from typing import Optional
from .openai_client import OpenAIClient

class XPostGenerator:
    def __init__(self, client: OpenAIClient):
        self.client = client

    def generate_post(self, figure_name: str, source_text: str, output_path: Path) -> bool:
        prompt = f"""Create an X (Twitter) post about {figure_name} with:
1. CONTENT: 1-2 concise paragraphs (240-280 characters total)
2. HOOK: Start with an attention-grabbing statement
3. STYLE: Conversational, use 1-2 relevant emojis
4. HASHTAGS: #{figure_name.replace(' ','')} #History #Facts
5. MENTION: Include @HistoryFacts if relevant

SOURCE MATERIAL:
{source_text[:2000]}"""

        response = self.client.generate_content(
            prompt=prompt,
            model="gpt-4",
            max_tokens=150  # Shorter for Twitter's character limit
        )

        if response:
            content = f"🐦 X Post: {figure_name}\n\n{response}"
            return self.client.save_to_file(content, output_path)
        return False
