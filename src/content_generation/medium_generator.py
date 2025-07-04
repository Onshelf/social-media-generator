from pathlib import Path
from typing import Optional
from .openai_client import OpenAIClient

class MediumPostGenerator:
    def __init__(self, client: OpenAIClient):
        self.client = client

    def generate_post(self, figure_name: str, source_text: str, output_path: Path) -> bool:
        """Generate a Medium article (using generate_post for consistency)"""
        prompt = f"""Create a Medium article about {figure_name} with:
1. HEADLINE: Catchy but sophisticated title (Max 100 chars)
2. SUBHEADER: Engaging preview text
3. INTRODUCTION: Personal anecdote or thought-provoking question
4. MAIN CONTENT: 3-5 sections with subheadings (600-800 words total)
5. KEY INSIGHTS: Bullet points of unique perspectives
6. CONCLUSION: Powerful closing thought + call-to-action
7. STYLE: Journalistic yet conversational, use Medium formatting
8. TAGS: {figure_name.replace(' ','')}, history, biography, education

SOURCE MATERIAL:
{source_text[:2000]}"""

        response = self.client.generate_content(
            prompt=prompt,
            model="gpt-4",
            max_tokens=1200
        )

        if response:
            content = f"📝 Medium Article: {figure_name}\n\n{response}"
            return self.client.save_to_file(content, output_path)
        return False
