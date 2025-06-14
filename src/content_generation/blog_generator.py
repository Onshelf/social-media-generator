from pathlib import Path
from typing import Optional
from .openai_client import OpenAIClient

class LegacyBlogGenerator:
    def __init__(self, openai_client: OpenAIClient):
        self.client = openai_client
        self.negative_prompts = [
            "NO keyword stuffing",
            "NO duplicate content",
            "NO unverified claims",
            "NO complex jargon without explanation",
            "NO passive voice"
        ]

    def generate_blog(self, figure_name: str, text: str, output_path: Path, seo_keyword: str = "") -> bool:
        """Generate an SEO-optimized blog article about a historical figure"""
        # First format the negative prompts
        formatted_negatives = "\n- ".join(self.negative_prompts)
        
        prompt = f"""Write a comprehensive blog article titled:
"How {figure_name} Changed the Course of History"

Source Material:
{text}

Article Structure:
1. Introduction:
   - Present-day relevance hook
   - Thesis statement about their impact

2. Body Sections:
   - Early Life (formative experiences)
   - Breakthrough Moment
   - Lasting Legacy
   - Challenges Faced

3. Conclusion:
   - Why their work still matters today
   - Further reading suggestions

SEO Requirements:
- Primary keyword: {seo_keyword or figure_name.lower()}
- Subheadings every 300 words
- Readability: 8th grade level

Avoid:
- {formatted_negatives}"""

        response = self.client.generate_content(
            prompt=prompt,
            content_type="blog_post",
            temperature=0.7,
            max_tokens=2000
        )

        if response and (blog := response.choices[0].message.content):
            return self._save_blog(blog, output_path, figure_name)
        return False

    def _save_blog(self, content: str, path: Path, name: str) -> bool:
        """Save blog post with SEO metadata"""
        formatted = f"# How {name} Changed History\n\n{content}\n\n" \
                   f"SEO CHECKLIST:\n" \
                   f"- Word count: {len(content.split())}\n" \
                   f"- Readability score: Target 60+\n" \
                   f"- Internal links: Add 2-3"
        path.write_text(formatted)
        return path.exists()
