from pathlib import Path
from typing import Optional
from .openai_client import OpenAIClient

class LegacyBlogGenerator:
    def __init__(self, client: OpenAIClient):
        self.client = client

    def generate_article(self, figure_name: str, source_text: str, output_path: Path) -> bool:
        prompt = f"""Write a professionally formatted blog article about {figure_name} with this structure:

# [Catchy, SEO-Optimized Title]

**Lead Paragraph** (1-2 sentences that hook the reader and state the article's focus)

## Early Life and Influences
- Place of birth and family background
- Key childhood experiences
- Education and early mentors

## Major Achievements
- Breakthrough discoveries/inventions
- Career milestones (bullet points)
- Awards and recognitions

## Challenges Faced
- Personal/professional obstacles
- Societal barriers overcome
- Controversies addressed

## Lasting Legacy
- Impact on their field
- Modern applications of their work
- Why they remain relevant today

**Conclusion** (Call-to-action prompting reader engagement)

Formatting Requirements:
- Proper Markdown formatting (headers, lists, bold for emphasis)
- 3-5 internal subheadings (## level)
- 1-2 relevant quotes from primary sources
- Transitional phrases between sections
- Target length: 800-1200 words

Source Material:
{source_text[:4000]}"""

        response = self.client.generate_content(
            prompt=prompt,
            model="gpt-4o-mini-2024-07-18",
            max_tokens=1500,
            temperature=0.6
        )

        if response:
            formatted_content = f"""<!-- Generated Blog Article: {figure_name} -->
{response}

<div class="article-footer">
    <p><em>This historical profile was generated using verified sources and AI assistance. 
    Last updated: {datetime.now().strftime('%B %d, %Y')}</em></p>
</div>"""
            return self.client.save_to_file(formatted_content, output_path)
        return False
