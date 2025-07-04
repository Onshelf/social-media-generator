from pathlib import Path
from typing import Optional
from .openai_client import OpenAIClient

class KofiPostGenerator:
    def __init__(self, client: OpenAIClient):
        self.client = client

    def generate_post(self, figure_name: str, source_text: str, output_path: Path) -> bool:
        prompt = f"""Create a Ko-fi post about {figure_name} with:
1. TITLE: Whimsical yet intriguing (Max 80 chars)
2. INTRODUCTION: Personal thank-you to supporters
3. EXCLUSIVE CONTENT: 2-3 paragraphs of patron-only insights
4. CREATOR NOTES: Behind-the-scenes about your research process
5. TIER BENEFITS: What different supporter levels get (3 tiers)
6. STYLE: Warm, intimate, and appreciative
7. EMOJIS: Light use of 🎨☕️✨ in headers
8. CTA: Clear support request with "Buy Me a Coffee" alternative

SOURCE MATERIAL:
{source_text[:2000]}"""

        response = self.client.generate_content(
            prompt=prompt,
            model="gpt-4",
            max_tokens=500  # Shorter but more personal
        )

        if response:
            content = f"☕ Ko-fi Post: {figure_name}\n\n{response}"
            return self.client.save_to_file(content, output_path)
        return False
