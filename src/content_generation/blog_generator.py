from pathlib import Path
from datetime import datetime
from typing import Optional, Union
import logging
from .openai_client import OpenAIClient  # Relative import

class LegacyBlogGenerator:
    """Generates professional blog articles with consistent formatting"""
    
    def __init__(self, client: OpenAIClient):
        self.client = client
        self.logger = logging.getLogger(__name__)
        self.max_source_chars = 3000  # Truncate long source texts
        self.default_model = "gpt-4"

    def generate_article(self, figure_name: str, source_text: str, output_path: Union[str, Path]) -> bool:
        """Main generation method matching your existing interface"""
        try:
            output_path = Path(output_path) if isinstance(output_path, str) else output_path
            output_path.parent.mkdir(parents=True, exist_ok=True)

            prompt = self._build_prompt(figure_name, source_text)
            response = self._get_ai_response(prompt)
            
            if not self._validate_response(response):
                return False
                
            return self._save_output(
                content=response,
                figure_name=figure_name,
                output_path=output_path
            )
            
        except Exception as e:
            self.logger.error(f"Blog generation failed: {str(e)}")
            return False

    def _build_prompt(self, figure_name: str, source_text: str) -> str:
        """Constructs the detailed generation prompt"""
        return f"""Write a comprehensive blog article about {figure_name} with this exact structure:

# [Engaging Title]

**Introduction** (1-2 paragraphs establishing significance)

## Early Life and Background
- Key formative experiences
- Education and influences

## Major Achievements
- Breakthrough contributions
- Important milestones

## Challenges Faced
- Obstacles overcome
- Controversies addressed

## Lasting Legacy
- Impact on their field
- Modern relevance

**Conclusion** (Memorable summary)

Requirements:
- Strict Markdown formatting
- 800-1200 words
- 3-5 subheadings
- 2-3 relevant quotes
- Academic tone

Source Context:
{source_text[:self.max_source_chars]}"""

    def _get_ai_response(self, prompt: str) -> Optional[str]:
        """Handles the AI API communication"""
        try:
            return self.client.generate_content(
                prompt=prompt,
                model=self.default_model,
                max_tokens=1500,
                temperature=0.7
            )
        except Exception as e:
            self.logger.error(f"API request failed: {str(e)}")
            return None

    def _validate_response(self, response: Optional[str]) -> bool:
        """Validates the generated content"""
        if not response:
            self.logger.error("Empty response received")
            return False
            
        word_count = len(response.split())
        if word_count < 500:  # Minimum word count
            self.logger.warning(f"Insufficient content: {word_count} words")
            return False
            
        return True

    def _save_output(self, content: str, figure_name: str, output_path: Path) -> bool:
        """Handles file output with proper formatting"""
        try:
            formatted = f"""<!-- Generated Blog Article: {figure_name} -->
{content}

<div class="article-footer">
    <p><em>Generated on {datetime.now().strftime('%Y-%m-%d')}</em></p>
</div>"""
            output_path.write_text(formatted, encoding='utf-8')
            return True
        except Exception as e:
            self.logger.error(f"Failed to save article: {str(e)}")
            return False
