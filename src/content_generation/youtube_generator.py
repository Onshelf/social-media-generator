from pathlib import Path
from typing import Optional
from .openai_client import OpenAIClient  # Keeping your original import

class YouTubePostGenerator:  # Only changed the class name
    def __init__(self, client: OpenAIClient):
        self.client = client  # No changes here

    def generate_post(self, figure_name: str, source_text: str, output_path: Path) -> bool:
        prompt = f"""Create a YouTube video description about {figure_name} with:
1. HOOK: First line makes viewers curious (question or bold statement)
2. DESCRIPTION: 2 short paragraphs (40-60 words each) about their impact
3. CALL-TO-ACTION: "Like 👍 | Subscribe 🔔 | Comment below 💬"
4. STYLE: Conversational, 2-3 relevant emojis
5. HASHTAGS: #{figure_name.replace(' ','')} #History #Biography

SOURCE MATERIAL:
{source_text[:2000]}"""  # Only modified the prompt instructions

        response = self.client.generate_content(
            prompt=prompt,
            model="gpt-4o-mini-2024-07-18",  # Kept your original model
            max_tokens=300  # Kept your original token limit
        )

        if response:
            content = f"▶️ {figure_name} YouTube Description\n\n{response}"  # Changed icon only
            return self.client.save_to_file(content, output_path)
        return False
