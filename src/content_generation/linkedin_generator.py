from pathlib import Path
from typing import Optional
from .openai_client import OpenAIClient

class LinkedInPostGenerator:
    def __init__(self, client: OpenAIClient):
        self.client = client

    def generate_post(self, figure_name: str, source_text: str, output_path: Path) -> bool:
        prompt = f"""Create a professional LinkedIn post about {figure_name} with:
1. HEADLINE: Attention-grabbing professional title (Max 120 characters)
2. INTRODUCTION: 1-2 sentences establishing relevance to business/leadership
3. KEY INSIGHTS: 3-5 bullet points of career lessons/achievements
4. PROFESSIONAL IMPACT: 1 paragraph on industry influence
5. CALL-TO-ACTION: Thought-provoking question for discussion
6. STYLE: Professional yet engaging, use 1-2 relevant emojis
7. HASHTAGS: #{figure_name.replace(' ','')} #Leadership #CareerGrowth #IndustryTrends

SOURCE MATERIAL:
{source_text[:2000]}"""

        response = self.client.generate_content(
            prompt=prompt,
            model="gpt-4",
            max_tokens=350  # Longer than Twitter, shorter than blog
        )

        if response:
            content = f"💼 LinkedIn Post: {figure_name}\n\n{response}"
            return self.client.save_to_file(content, output_path)
        return False
