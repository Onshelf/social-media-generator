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

    def generate_post(self, figure_name: str, text: str, output_path: Path) -> bool:
        formatted_negatives = "\n- ".join(self.negative_prompts)
        prompt = f"""Create a Facebook post about {figure_name}'s historical impact:
        
Source Content:
{text}

Requirements:
1. Structure:
   - Attention-grabbing first line
   - 2-3 short paragraphs
   - Emoji every 2-3 sentences
   - Clear call-to-action

2. Style:
   - Conversational but respectful tone
   - Hashtags: #{figure_name.replace(' ','')} #HistoryMakers #HumanLegacy
   - Character limit: 1000

3. Avoid:
   - {formatted_negatives}"""

        response = self.client.generate_content(
            prompt=prompt,
            content_type="facebook_post",
            temperature=0.9,
            max_tokens=500
        )

        if response:
            processed = f"// {figure_name}'s Historical Impact Post\n\n{response}\n\n" \
                       f"POSTING TIPS:\n" \
                       f"- Best time: Weekdays 1-3 PM\n" \
                       f"- Suggested image: Historical portrait or artifact"
            return self.client.save_to_file(processed, output_path)
        return False
