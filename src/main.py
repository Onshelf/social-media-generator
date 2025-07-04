#!/usr/bin/env python3
"""
Social Media Content Generator - YouTube Dual Output
"""

import sys
from pathlib import Path
from typing import List
from data_processing.excel_reader import get_names_from_excel
from data_processing.file_manager import create_folder_structure
from data_processing.pdf_downloader import download_wikipedia_pdf
from data_processing.pdf_processor import PDFProcessor
from content_generation.openai_client import OpenAIClient
from content_generation.youtube_generator import YouTubePostGenerator
from content_generation.story_generator import LegacyStoryGenerator  # For YouTube stories
from content_generation.post_generator import LegacyPostGenerator
from content_generation.blog_generator import LegacyBlogGenerator

CONFIG = {
    "input_file": "/content/social-media-generator/input/Names.xlsx",
    "output_dir": "outputs",
    "platforms": ["YouTube", "Facebook", "Blog"],
    "openai_key": "your-api-key-here",
    "model": "gpt-4",
    "max_figures": 5,
    "min_text_length": 500,
    "timeout": 30
}

def process_figure(figure_name: str, client: OpenAIClient) -> bool:
    """Process a single historical figure with dual YouTube output"""
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
        
        if not extracted_text or len(extracted_text.split()) < CONFIG["min_text_length"]:
            print(f"⚠️ Insufficient content ({len(extracted_text.split()) if extracted_text else 0} words)")
            return False

        # 4. Initialize generators
        generators = {
            "YouTube": {
                "post": YouTubePostGenerator(client),
                "story": LegacyStoryGenerator(client)
            },
            "Facebook": LegacyPostGenerator(client),
            "Blog": LegacyBlogGenerator(client)
        }

        # 5. Generate content
        results = []
        youtube_dir = figure_dir / "YouTube"
        
        # Generate YouTube content (both post and story)
        try:
            # Generate YouTube post
            post_success = generators["YouTube"]["post"].generate_post(
                figure_name=figure_name,
                source_text=extracted_text,
                output_path=youtube_dir / "post.txt"
            )
            results.append(("YouTube Post", post_success))
            
            # Generate YouTube story
            story_success = generators["YouTube"]["story"].generate_story(
                figure_name=figure_name,
                source_text=extracted_text,
                output_path=youtube_dir / "story.txt"
            )
            results.append(("YouTube Story", story_success))
        except Exception as e:
            print(f"   YouTube generation failed: {str(e)}")
            results.append(("YouTube Post", False))
            results.append(("YouTube Story", False))

        # Generate other platform content
        for platform in ["Facebook", "Blog"]:
            output_file = figure_dir / platform / "content.txt"
            try:
                if platform == "Facebook":
                    success = generators[platform].generate_post(
                        figure_name=figure_name,
                        source_text=extracted_text,
                        output_path=output_file
                    )
                elif platform == "Blog":
                    success = generators[platform].generate_article(
                        figure_name=figure_name,
                        source_text=extracted_text,
                        output_path=output_file
                    )
                results.append((platform, success))
            except Exception as e:
                print(f"   {platform} generation failed: {str(e)}")
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
        print("🚀 Initializing Content Generator")
        
        client = OpenAIClient(api_key=CONFIG["openai_key"])
        
        names = get_names_from_excel(CONFIG["input_file"])
        if not names:
            raise ValueError("No names found in input file")
        names = names[:CONFIG["max_figures"]]
        print(f"🧑‍🤝‍🧑 Found {len(names)} figures to process")

        success_count = 0
        for name in names:
            if process_figure(name, client):
                success_count += 1

        print("\n" + "="*50)
        print(f"🏁 Completed processing {success_count}/{len(names)} figures")
        print(f"📂 Output directory: {Path(CONFIG['output_dir']).resolve()}")
        
        return 0 if success_count == len(names) else 1
        
    except Exception as e:
        print(f"\n🔥 Critical Error: {str(e)}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
