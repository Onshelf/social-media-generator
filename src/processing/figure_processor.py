from pathlib import Path
from typing import Dict, List, Tuple

from data_processing.file_manager import create_folder_structure
from data_processing.pdf_downloader import download_wikipedia_pdf
from data_processing.pdf_processor import PDFProcessor
from content_generation.youtube_generator import YouTubePostGenerator
from content_generation.story_generator import LegacyStoryGenerator
from content_generation.x_generator import XPostGenerator
from content_generation.linkedin_generator import LinkedInPostGenerator
from content_generation.patreon_generator import PatreonPostGenerator
from content_generation.medium_generator import MediumPostGenerator
from content_generation.kofi_generator import KofiPostGenerator
from content_generation.post_generator import LegacyPostGenerator
from content_generation.blog_generator import LegacyBlogGenerator

from config.config_manager import ConfigManager
from utils.content_validator import ContentValidator

class FigureProcessor:
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.validator = ContentValidator()

    def generate_youtube_content(self, figure_name: str, extracted_text: str, youtube_dir: Path, 
                               post_generator, story_generator) -> List[Tuple[str, bool]]:
        """Generate both post and story for YouTube"""
        results = []
        
        # Generate YouTube post (description)
        post_file = youtube_dir / "post.txt"
        try:
            success = post_generator.generate_post(
                figure_name=figure_name,
                source_text=extracted_text,
                output_path=post_file
            )
            results.append(("YouTube Post", success))
        except Exception as e:
            print(f"❌ YouTube Post failed: {str(e)}")
            results.append(("YouTube Post", False))
        
        # Generate YouTube story (script)
        story_file = youtube_dir / "story.txt"
        try:
            success = story_generator.generate_story(
                figure_name=figure_name,
                source_text=extracted_text,
                output_path=story_file
            )
            results.append(("YouTube Story", success))
        except Exception as e:
            print(f"❌ YouTube Story failed: {str(e)}")
            results.append(("YouTube Story", False))
        
        return results

    def process_figure(self, figure_name: str, client) -> bool:
        """Process a single figure across all platforms"""
        try:
            print(f"\n{'='*50}")
            print(f"🔄 Processing: {figure_name}")
            print(f"{'='*50}")

            # 1. Create folder structure
            figure_dir = create_folder_structure(
                base_dir=self.config_manager.get_output_dir(),
                figure_name=figure_name,
                platforms=self.config_manager.get_platforms()
            )

            # 2. Download and process PDF
            pdf_path = download_wikipedia_pdf(
                figure_name=figure_name,
                save_path=figure_dir,
                timeout=self.config_manager.get_timeout()
            )
            
            # 3. Extract content (single validation)
            processor = PDFProcessor()
            extracted_text, _, extracted_images = processor.extract_content(pdf_path, figure_dir)
            
            if extracted_images:
                print(f"📸 Saved {len(extracted_images)} images to {figure_dir/'extracted_pics'}")
            
            # Validate content once and get word count
            is_valid, word_count = self.validator.validate_content(extracted_text)
            if not is_valid:
                return False

            # 4. Initialize all generators
            generators = {
                "YouTube": {
                    "post": YouTubePostGenerator(client),
                    "story": LegacyStoryGenerator(client)
                },
                "X": XPostGenerator(client),
                "Facebook": LegacyPostGenerator(client),
                "LinkedIn": LinkedInPostGenerator(client),
                "Patreon": PatreonPostGenerator(client),
                "Medium": MediumPostGenerator(client),
                "Ko-fi": KofiPostGenerator(client),
                "Blog": LegacyBlogGenerator(client)
            }

            # 5. Generate content
            results = []
            youtube_dir = figure_dir / "YouTube"
            
            # Generate YouTube content (both post and story)
            results.extend(self.generate_youtube_content(
                figure_name=figure_name,
                extracted_text=extracted_text,
                youtube_dir=youtube_dir,
                post_generator=generators["YouTube"]["post"],
                story_generator=generators["YouTube"]["story"]
            ))

            # Generate other platform content
            for platform in ["X", "Facebook", "LinkedIn", "Patreon", "Medium", "Ko-fi", "Blog"]:
                output_file = figure_dir / platform / "content.txt"
                
                try:
                    # Check platform requirements using pre-calculated word count
                    if not self.validator.check_platform_requirements(platform, word_count, self.config_manager):
                        results.append((platform, False))
                        continue
                    
                    # Handle Blog separately since it uses generate_article
                    if platform == "Blog":
                        success = generators[platform].generate_article(
                            figure_name=figure_name,
                            source_text=extracted_text,
                            output_path=output_file
                        )
                    else:
                        success = generators[platform].generate_post(
                            figure_name=figure_name,
                            source_text=extracted_text,
                            output_path=output_file
                        )
                    
                    results.append((platform, success))
                except Exception as e:
                    print(f"❌ {platform} generation failed: {str(e)}")
                    results.append((platform, False))

            print("\n📊 Generation Results:")
            for platform, success in results:
                print(f"   {platform.ljust(12)}: {'✅' if success else '❌'}")
            
            return all(success for _, success in results)

        except Exception as e:
            print(f"⚠️ Error processing {figure_name}: {str(e)}")
            return False
