from pathlib import Path
from typing import Optional
from .openai_client import OpenAIClient

class LegacyStoryGenerator:
    def __init__(self, openai_client: OpenAIClient):
        self.client = openai_client

    def generate_legacy_story(self, figure_name: str, text: str, output_path: Path) -> bool:
        prompt = f"""Create a YouTube documentary-style script about {figure_name}'s lasting impact:

Source Material:
{text}

Requirements:
1. Narrative Arc:
   - Opening hook: Pose an intriguing question about their legacy
   - Act 1: Early life and challenges [Visual: Period recreations]
   - Act 2: Key contributions [B-roll: Historical documents]
   - Act 3: Modern-day impact [Visual: Contemporary applications]

2. Content Rules:
   - Emphasize human elements over dates
   - Include 3 "impact moments" with [Visual] cues
   - End with reflection prompt: "How has {figure_name} shaped your world?"

3. Production Notes:
   - Target length: 10 minutes (1500 words)
   - Pace: 140WPM with dramatic pauses
   - Suggested music: Epic historical score"""

        response = self.client.generate_content(
            prompt=prompt,
            content_type="legacy_story",
            temperature=0.8
        )
        
        if response:
            processed = f"# {figure_name}'s Legacy Documentary\n\n{response}\n\n" \
                      f"PRODUCTION CHECKLIST:\n" \
                      f"- Verify historical accuracy of visuals\n" \
                      f"- Include {figure_name}'s portrait in closing credits\n" \
                      f"- Add 'Learn More' links in description"
            return self.client.save_to_file(processed, output_path)
        return False
