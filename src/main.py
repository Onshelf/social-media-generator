#!/usr/bin/env python3
"""
Social Media Content Generator - Fully Functional Version
"""

import sys
from pathlib import Path
from datetime import datetime
from data_processing.excel_reader import get_names_from_excel
from data_processing.file_manager import create_folder_structure
from data_processing.pdf_downloader import download_wikipedia_pdf
from data_processing.pdf_processor import PDFProcessor
from content_generation.openai_client import OpenAIClient
from content_generation.story_generator import LegacyStoryGenerator
from content_generation.post_generator import LegacyPostGenerator
from content_generation.blog_generator import LegacyBlogGenerator

CONFIG = {
    "input_file": "input/Names.xlsx",
    "output_dir": "outputs",
    "platforms": ["YouTube", "Facebook", "Blog"],
    "openai_key": "Your_API",
    "model": "gpt-4o-mini-2024-07-18",
    "max_figures": 5,
    "min_text_length": 500,
    "timeout": 30
}

def process_figure(figure_name: str, client: OpenAIClient) -> bool:
    """Process a single historical figure"""
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
        
        extracted_text, _ = PDFProcessor().extract_text(pdf_path)
        if len(extracted_text.split()) < CONFIG["min_text_length"]:
            print(f"⚠️ Insufficient content ({len(extracted_text.split())} words)")
            return False

        # 3. Initialize generators
        generators = {
            "YouTube": LegacyStoryGenerator(client).generate_story,
            "Facebook": LegacyPostGenerator(client).generate_post,
            "Blog": LegacyBlogGenerator(client).generate_article
        }

        # 4. Generate content
        results = []
        for platform, generate_func in generators.items():
            output_file = figure_dir / platform / "content.txt"
            
            try:
                success = generate_func(
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
            print(f"   {platform.ljust(8)}: {'✅' if success else '❌'}")
        
        return all(success for _, success in results)

    except Exception as e:
        print(f"⚠️ Error processing {figure_name}: {str(e)}", file=sys.stderr)
        return False

def main():
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
