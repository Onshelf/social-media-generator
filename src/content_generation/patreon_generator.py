from pathlib import Path
from typing import Optional
from .openai_client import OpenAIClient

class PatreonPostGenerator:
    def __init__(self, client: OpenAIClient):
        self.client = client

    def generate_post(self, figure_name: str, source_text: str, output_path: Path) -> bool:
        prompt = f"""Create an exclusive Patreon post about {figure_name} with:
1. TITLE: Catchy and intriguing (max 100 characters)
2. INTRODUCTION: Personal note to patrons (1 paragraph)
3. EXCLUSIVE CONTENT: 3-4 detailed paragraphs with insights not available publicly
4. BEHIND-THE-SCENES: 1 paragraph about research process
5. CALL-TO-ACTION: Ask for support and feedback
6. STYLE: Warm, personal, and patron-focused
7. TIER MENTION: [For $5+ patrons] tag for special content

SOURCE MATERIAL:
{source_text[:2000]}"""

        response = self.client.generate_content(
            prompt=prompt,
            model="gpt-4",
            max_tokens=600  # Longer for Patreon's detailed format
        )

        if response:
            content = f"🎭 Patreon Exclusive: {figure_name}\n\n{response}"
            return self.client.save_to_file(content, output_path)
        return False
