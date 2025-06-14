class LegacyBlogGenerator(BlogPostGenerator):
    def generate_legacy_article(self, figure_name: str, text: str, output_path: Path) -> bool:
        """
        Create a comprehensive blog article about a figure's historical impact
        """
        prompt = f"""Write an in-depth blog article titled:
"How {figure_name} Changed the Course of History"

Source Material:
{text}

Article Structure:
1. Introduction:
   - Present-day relevance hook
   - Thesis: Their most significant contribution

2. Body Sections:
   - Early Life (Formative experiences)
   - Breakthrough Moment (Turning point)
   - Lasting Impact (Modern applications)
   - Controversies/Challenges (Balanced perspective)

3. Conclusion:
   - "The World Without" thought experiment
   - Further reading/resources

Style Guidelines:
- Academic but accessible tone (Grade 10 reading level)
- Include 3-5 pull quotes from historians
- Use "{figure_name}" consistently (no surname-only references)"""

        response = self.client.generate_content(
            prompt=prompt,
            content_type="legacy_article",
            temperature=0.6,
            max_tokens=2500
        )

        if response and (article := response.choices[0].message.content):
            return self._save_legacy_article(article, output_path, figure_name)
        return False

    def _save_legacy_article(self, article: str, path: Path, name: str) -> bool:
        processed = f"# How {name} Changed History\n\n{article}\n\n" \
                  f"RESEARCH NOTES:\n" \
                  f"- Verify all historical quotes\n" \
                  f"- Include bibliography of 3+ sources\n" \
                  f"- Add timeline infographic suggestion"
        return self.client.save_to_file(processed, path)
