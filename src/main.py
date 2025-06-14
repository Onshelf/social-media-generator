#!/usr/bin/env python3
"""
Social Media Content Generator for Historical Figures
Generates YouTube scripts, Facebook posts, and blog articles
"""

import sys
from pathlib import Path
from data_processing.excel_reader import get_names_from_excel
from data_processing.file_manager import create_folder_structure
from data_processing.pdf_downloader import download_wikipedia_pdf
from data_processing.pdf_processor import PDFProcessor
from content_generation.openai_client import OpenAIClient
from content_generation.story_generator import LegacyStoryGenerator
from content_generation.post_generator import LegacyPostGenerator
from content_generation.blog_generator import LegacyBlogGenerator

# Configuration
CONFIG = {
    "input_file": "inputs/names_list.xlsx",
    "output_dir": "outputs",
    "platforms": ["YouTube", "Facebook", "Blog"],
    "openai_key": "your-api-key-here",  # Replace with actual key
    "max_figures": 3  # Safety limit
}

def process_figure(figure_name: str, openai_client: OpenAIClient, output_base: Path) -> bool:
    """Process a single historical figure through the pipeline"""
    try:
        print(f"\n{'='*50}")
        print(f"🔄 Processing: {figure_name}")
        print(f"{'='*50}")
        
        # Setup directories
        figure_dir = output_base / figure_name.replace(" ", "_")
        figure_dir.mkdir(parents=True, exist_ok=True)
        
        # 1. Download Wikipedia PDF
        print("📥 Downloading Wikipedia content...")
        pdf_path = download_wikipedia_pdf(figure_name, figure_dir)
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF download failed for {figure_name}")
        
        # 2. Extract text
        print("🔍 Extracting text content...")
        pdf_processor = PDFProcessor()
        extracted_text, page_count = pdf_processor.extract_text(pdf_path)
        if not extracted_text:
            raise ValueError(f"No text extracted (pages: {page_count})")
        print(f"📝 Extracted {len(extracted_text.split())} words from {page_count} pages")
        
        # 3. Initialize generators
        generators = {
            "YouTube": LegacyStoryGenerator(openai_client),
            "Facebook": LegacyPostGenerator(openai_client),
            "Blog": LegacyBlogGenerator(openai_client)
        }
        
        # 4. Generate content
        print("🎨 Generating content...")
        results = []
        
        if "YouTube" in CONFIG["platforms"]:
            output_path = figure_dir / "YouTube/documentary_script.txt"
            success = generators["YouTube"].generate_legacy_story(
                figure_name, extracted_text, output_path)
            results.append(("YouTube", success))
        
        if "Facebook" in CONFIG["platforms"]:
            output_path = figure_dir / "Facebook/legacy_post.txt"
            success = generators["Facebook"].generate_post(
                figure_name, extracted_text, output_path)
            results.append(("Facebook", success))
        
        if "Blog" in CONFIG["platforms"]:
            output_path = figure_dir / "Blog/impact_article.txt"
            success = generators["Blog"].generate_blog(
                figure_name, extracted_text, output_path)
            results.append(("Blog", success))
        
        # Print results
        print("\n📊 Generation Results:")
        for platform, success in results:
            print(f"{'✅' if success else '❌'} {platform}")
        
        return all(success for _, success in results)
    
    except Exception as e:
        print(f"⚠️ Error processing {figure_name}: {str(e)}", file=sys.stderr)
        return False

def main():
    try:
        # Initialize clients
        print("🚀 Initializing systems...")
        openai_client = OpenAIClient(api_key=CONFIG["openai_key"])
        
        # 1. Read names
        print("\n📖 Reading input file...")
        names = get_names_from_excel(CONFIG["input_file"])
        if not names:
            raise ValueError("No names found in Excel file")
        names = names[:CONFIG["max_figures"]]
        print(f"🧑‍🤝‍🧑 Found {len(names)} figures to process")
        
        # 2. Create output directory
        output_base = Path(CONFIG["output_dir"])
        output_base.mkdir(exist_ok=True)
        
        # 3. Process figures
        success_count = 0
        for name in names:
            if process_figure(name, openai_client, output_base):
                success_count += 1
        
        # Final report
        print("\n" + "="*50)
        print(f"🏁 Completed processing {success_count}/{len(names)} figures")
        print(f"📂 Output directory: {output_base.resolve()}")
        
    except Exception as e:
        print(f"\n🔥 Critical error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
