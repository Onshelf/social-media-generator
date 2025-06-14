from pathlib import Path
from typing import Optional
from .openai_client import OpenAIClient

class LegacyStoryGenerator:
    def __init__(self, openai_client: OpenAIClient):
        self.client = openai_client

    def generate_legacy_story(self, figure_name: str, text: str, output_path: Path) -> bool:
        prompt = f"""Create a YouTube documentary-style script about {figure_name}'s lasting impact..."""  # Keep your exact prompt
        
        response = self.client.generate_content(
            prompt=prompt,
            content_type="legacy_story",
            temperature=0.8
        )
        
        if response:
            return self.client.save_to_file(response, output_path)
        return False
