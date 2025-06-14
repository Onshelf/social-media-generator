class LegacyStoryGenerator(StoryGenerator):
    def generate_legacy_story(self, figure_name: str, text: str, output_path: Path) -> bool:
        """
        Generate a compelling video script about a historical figure's impact
        """
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
        
        if response and (story := response.choices[0].message.content):
            return self._save_legacy_story(story, output_path, figure_name)
        return False

    def _save_legacy_story(self, story: str, path: Path, name: str) -> bool:
        processed = f"# {name}'s Legacy Documentary\n\n{story}\n\n" \
                  f"PRODUCTION CHECKLIST:\n" \
                  f"- Verify historical accuracy of visuals\n" \
                  f"- Include {name}'s portrait in closing credits\n" \
                  f"- Add 'Learn More' links in description"
        return self.client.save_to_file(processed, path)
