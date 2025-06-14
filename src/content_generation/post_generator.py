from pathlib import Path
from typing import Optional
from .openai_client import OpenAIClient

class LegacyPostGenerator:
    def __init__(self, openai_client: OpenAIClient):
        self.client = openai_client
        self.negative_prompts = [
            "NO dates or years",
            "NO complex statistics",
            "NO long paragraphs",
            "NO technical jargon",
            "NO vague calls-to-action"
        ]

    def generate_post(self, figure_name: str, text: str, output_path: Path, post_type: str = "educational") -> bool:
        prompt = f"""Create a Facebook post about {figure_name}'s historical impact:
        
Source Content:
{text}

Requirements:
1. Structure:
   - Attention-grabbing first line
   - 2-3 short paragraphs
   - Emoji every 2-3 sentences
   - Clear call-to-action

2. Style:
   - {self._get_style_guide(post_type)}
   - Hashtags: {self._get_hashtags(post_type)}
   - Character limit: 1000

3. Avoid:
   - {"\n   - ".join(self.negative_prompts)}"""

        response = self.client.generate_content(
            prompt=prompt,
            content_type="facebook_post",
            temperature=0.9,
            max_tokens=500
        )

        if response and (post := response.choices[0].message.content):
            return self._save_post(post, output_path, figure_name)
        return False

    # ... (keep all your existing helper methods)
