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
        """Generate a Facebook post about a historical figure's impact"""
        # Create formatted negative prompts first
        formatted_negatives = "\n   - ".join(self.negative_prompts)
        
        prompt = f"""Create a Facebook post about {figure_name}'s historical impact:
        
## Source Content:
{text}

## Requirements:
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
   - {formatted_negatives}"""

        response = self.client.generate_content(
            prompt=prompt,
            content_type="facebook_post",
            temperature=0.9,
            max_tokens=500
        )

        if response and (post := response.choices[0].message.content):
            return self._save_post(post, output_path, figure_name)
        return False

    def _get_style_guide(self, post_type: str) -> str:
        styles = {
            "educational": "Fact-based but conversational tone",
            "inspirational": "Motivational and uplifting",
            "promotional": "Highlight benefits without being salesy"
        }
        return styles.get(post_type, "Conversational tone")

    def _get_hashtags(self, post_type: str) -> str:
        tags = {
            "educational": "#DidYouKnow #LearnEveryday",
            "inspirational": "#Motivation #PositiveVibes",
            "promotional": "#SpecialOffer #NewFeature"
        }
        return tags.get(post_type, "#Interesting #Facts")

    def _save_post(self, post: str, path: Path, name: str) -> bool:
        """Save post with Facebook-specific formatting"""
        processed = f"// {name}'s Historical Impact Post\n\n{post}\n\n" \
                   f"POSTING TIPS:\n" \
                   f"- Best time: {self._best_posting_time()}\n" \
                   f"- Suggested image: Historical portrait or artifact"
        path.write_text(processed)
        return path.exists()

    def _best_posting_time(self) -> str:
        return "Weekdays 1-3 PM"
