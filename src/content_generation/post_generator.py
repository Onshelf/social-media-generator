class LegacyPostGenerator(FacebookPostGenerator):
    def generate_legacy_post(self, figure_name: str, text: str, output_path: Path) -> bool:
        """
        Create an engaging Facebook post about a historical figure's influence
        """
        prompt = f"""Compose a Facebook post highlighting {figure_name}'s enduring influence:

Source Content:
{text}

Post Guidelines:
1. Structure:
   - Opening: "Did you know...?" fact
   - Middle: Their most surprising contribution
   - Close: Poll question ("Which innovation impacts you most?")

2. Style:
   - Conversational but respectful tone
   - 2-3 relevant emojis (e.g., 🌍 for global impact)
   - Hashtags: #{figure_name.replace(' ','')} #HistoryMakers #HumanLegacy

3. Special Rules:
   - Feature one little-known fact
   - Include a "This Day in History" callback
   - Add museum/archive link if available"""

        response = self.client.generate_content(
            prompt=prompt,
            content_type="legacy_post",
            temperature=0.7,
            max_tokens=400
        )

        if response and (post := response.choices[0].message.content):
            return self._save_legacy_post(post, output_path, figure_name)
        return False

    def _save_legacy_post(self, post: str, path: Path, name: str) -> bool:
        processed = f"// {name}'s Legacy Post\n\n{post}\n\n" \
                  f"ENGAGEMENT TIPS:\n" \
                  f"- Post on {name}'s birthday\n" \
                  f"- Tag relevant historical societies\n" \
                  f"- Use 'Throwback Thursday' hashtag"
        return self.client.save_to_file(processed, path)
