from pathlib import Path
from typing import Optional
from .openai_client import OpenAIClient

class LegacyStoryGenerator:
    def __init__(self, client: OpenAIClient):
        self.client = client

    def generate_story(self, figure_name: str, source_text: str, output_path: Path) -> bool:
        prompt = f"""Write a compelling historical narrative about {figure_name} structured as follows:

1. THE HOOK (1 paragraph):
Begin with a dramatic moment that captures {figure_name}'s essence

2. THE BACKGROUND (2 paragraphs):
- Childhood and formative experiences
- Historical context of their era

3. THE STRUGGLE (3 paragraphs):
- Key challenges they faced
- Their innovative solutions
- Major obstacles overcome

4. THE LEGACY (2 paragraphs):
- Lasting impact on their field
- How their work affects us today

Maintain these stylistic elements:
- Vivid, descriptive language
- Historical accuracy
- Emotional resonance
- Theme of perseverance

Source Material:
{source_text[:3000]}"""

        response = self.client.generate_content(
            prompt=prompt,
            model="gpt-4o-mini-2024-07-18",
            max_tokens=1200,
            temperature=0.7
        )

        if response:
            structured_content = f"""HISTORICAL NARRATIVE: {figure_name}
            
{response}

---            
This story was generated from verified historical sources."""
            return self.client.save_to_file(structured_content, output_path)
        return False
