from pathlib import Path
from typing import Optional
from .openai_client import OpenAIClient

class LegacyBlogGenerator:
    def __init__(self, client: OpenAIClient):
        self.client = client

    def generate_post(self, figure_name: str, source_text: str, output_path: Path) -> bool:
        """
        Generate a long-form blog article (using generate_post name for consistency)
        while maintaining article-style content quality.
        """
        prompt = f"""Create a comprehensive blog article about {figure_name} with these sections:
        
1. TITLE: SEO-optimized and intriguing (Max 80 characters)
2. INTRODUCTION: Hook with a surprising fact or question
3. BODY: 3-5 well-researched sections with subheadings
4. KEY INSIGHTS: Bullet points of important takeaways
5. CONCLUSION: Thought-provoking summary and call-to-action
6. STYLE: Engaging yet authoritative, suitable for educated audience
7. FORMATTING: Use Markdown with proper headings and lists
8. WORD COUNT: 800-1200 words
9. TAGS: {figure_name.replace(' ','')}, history, biography, education

SOURCE MATERIAL:
{source_text[:2000]}"""

        response = self.client.generate_content(
            prompt=prompt,
            model="gpt-4",
            max_tokens=1500  # Longer for detailed articles
        )

        if response:
            content = f"✍️ Blog Article: {figure_name}\n\n{response}"
            return self.client.save_to_file(content, output_path)
        return False

    # Alias for backward compatibility
    generate_article = generate_post
