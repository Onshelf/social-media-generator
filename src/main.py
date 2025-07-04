#!/usr/bin/env python3
"""
Social Media Content Generator - Full Version with LinkedIn
"""

import sys
from pathlib import Path
from typing import List, Tuple
from data_processing.excel_reader import get_names_from_excel
from data_processing.file_manager import create_folder_structure
from data_processing.pdf_downloader import download_wikipedia_pdf
from data_processing.pdf_processor import PDFProcessor
from content_generation.openai_client import OpenAIClient
from content_generation.youtube_generator import YouTubePostGenerator
from content_generation.story_generator import LegacyStoryGenerator
from content_generation.x_generator import XPostGenerator
from content_generation.linkedin_generator import LinkedInPostGenerator
from content_generation.patreon_generator import PatreonPostGenerator
from content_generation.post_generator import LegacyPostGenerator
from content_generation.blog_generator import LegacyBlogGenerator

CONFIG = {
    "input_file": "/content/social-media-generator/input/Names.xlsx",
    "output_dir": "outputs",
    "platforms": ["YouTube", "X", "Facebook", "LinkedIn", "Patreon", "Blog"],
    "openai_key": "your-api-key-here",
    "model": "gpt-4",
    "max_figures": 5,
    "min_text_length": 500,
    "linkedin_min_length": 600,
    "patreon_min_length": 800,
    "timeout": 30,
    "x_char_limit": 280
}

def validate_content(extracted_text: str, platform: str = None) -> bool:
    """Validate extracted content meets platform requirements"""
    if not extracted_text:
        print("❌ No text extracted from PDF")
        return False
    
    word_count = len(extracted_text.split())
    min_length = {
        "LinkedIn": CONFIG["linkedin_min_length"],
        "Patreon": CONFIG["patreon_min_length"],
    }.get(platform, CONFIG["min_text_length"])
    
    if word_count < min_length:
        print(f"❌ Insufficient content for {platform if platform else 'processing'} "
              f"({word_count} words, need {min_length})")
        return False
    
    print(f"✓ Content validated ({word_count} words)")
    return True

def generate_youtube_content(
    figure_name: str,
    extracted_text: str,
    youtube_dir: Path,
    post_generator: YouTubePostGenerator,
    story_generator: LegacyStoryGenerator
) -> List[Tuple[str, bool]]:
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

def process_figure(figure_name: str, client: OpenAIClient) -> bool:
    """Process a single figure across all platforms"""
    try:
        print(f"\n{'='*50}")
        print(f"🔄 Processing: {figure_name}")
        print(f"{'='*50}")

        # 1. Create folder structure
        figure_dir = create_folder_structure(
            base_dir=Path(CONFIG["output_dir"]),
            figure_name=figure_name,
            platforms=CONFIG["platforms"]
        )

        # 2. Download and process PDF
        pdf_path = download_wikipedia_pdf(
            figure_name=figure_name,
            save_path=figure_dir,
            timeout=CONFIG["timeout"]
        )
        
        # 3. Extract content
        processor = PDFProcessor()
        extracted_text, _, extracted_images = processor.extract_content(pdf_path, figure_dir)
        
        if extracted_images:
            print(f"📸 Saved {len(extracted_images)} images to {figure_dir/'extracted_pics'}")
        
        if not validate_content(extracted_text):
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
            "Blog": LegacyBlogGenerator(client)
        }

        # 5. Generate content
        results = []
        youtube_dir = figure_dir / "YouTube"
        
        # Generate YouTube content (both post and story)
        results.extend(generate_youtube_content(
            figure_name=figure_name,
            extracted_text=extracted_text,
            youtube_dir=youtube_dir,
            post_generator=generators["YouTube"]["post"],
            story_generator=generators["YouTube"]["story"]
        ))

        # Generate other platform content
        for platform in ["X", "Facebook", "LinkedIn", "Patreon", "Blog"]:
            output_file = figure_dir / platform / "content.txt"
            
            try:
                # Skip if platform has special length requirements
                if platform in ["LinkedIn", "Patreon"] and not validate_content(extracted_text, platform):
                    results.append((platform, False))
                    continue
                
                success = generators[platform].generate_post(
                    figure_name=figure_name,
                    source_text=extracted_text,
                    output_path=output_file
                ) if platform != "Blog" else generators[platform].generate_article(
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
        print(f"⚠️ Error processing {figure_name}: {str(e)}", file=sys.stderr)
        return False

def main():
    """Main execution function"""
    try:
        print("🚀 Social Media Content Generator")
        print(f"📌 Target Platforms: {', '.join(CONFIG['platforms'])}")
        print(f"   - YouTube: Generates both post.txt and story.txt")
        
        # 1. Initialize OpenAI client
        client = OpenAIClient(api_key=CONFIG["openai_key"])
        
        # 2. Get names from input file
        names = get_names_from_excel(CONFIG["input_file"])
        if not names:
            raise ValueError("No names found in input file")
        names = names[:CONFIG["max_figures"]]
        print(f"\n🧑‍🤝‍🧑 Found {len(names)} figures to process")
        print(f"🔍 First figure: {names[0]}")

        # 3. Process each figure
        success_count = 0
        for i, name in enumerate(names, 1):
            print(f"\n📌 Processing figure {i}/{len(names)}")
            if process_figure(name, client):
                success_count += 1

        # 4. Final report
        print("\n" + "="*50)
        print(f"🏁 Processing Complete")
        print(f"✅ Successful: {success_count}/{len(names)} figures")
        print(f"📂 Output Directory: {Path(CONFIG['output_dir']).resolve()}")
        
        return 0 if success_count == len(names) else 1
        
    except Exception as e:
        print(f"\n🔥 Critical Error: {str(e)}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
