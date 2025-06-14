#!/usr/bin/env python3
"""
Social Media Content Generator for Historical Figures
Generates YouTube scripts, Facebook posts, and blog articles about impactful people
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

# Configuration - in production, use environment variables or config files
CONFIG = {
    "input_file": "inputs/names_list.xlsx",      # Excel file with historical figures
    "output_dir": "outputs",                     # Base output directory
    "platforms": ["YouTube", "Facebook", "Blog"],# Content types to generate
    "openai_key": "your-api-key-here",           # Replace with your actual key
    "max_figures": 3                             # Limit number of figures to process
}

def setup_directories(base_dir: Path, name: str) -> Path:
    """Create folder structure for a historical figure"""
    figure_dir = base_dir / name.replace(" ", "_")
    figure_dir.mkdir(parents=True, exist_ok=True)
    
    # Create platform subdirectories
    for platform in CONFIG["platforms"]:
        (figure_dir / platform).mkdir(exist_ok=True)
    
    return figure_dir

def process_figure(figure_name: str, generators: dict, output_base: Path) -> bool:
    """Process a single historical figure"""
    try:
        print(f"\n{'='*50}")
        print(f"Processing: {figure_name}")
        print(f"{'='*50}")
        
        figure_dir = setup_directories(output_base, figure_name)
        
        # Step 1: Download Wikipedia PDF
        print("📥 Downloading Wikipedia content...")
        pdf_path = download_wikipedia_pdf(figure_name, figure_dir)
        if not pdf_path.exists():
            raise FileNotFoundError(f"Failed to download PDF for {figure_name}")
        
        # Step 2: Extract text
        print("🔍 Extracting text content...")
        pdf_processor = PDFProcessor()
        extracted_text, page_count = pdf_processor.extract_text(pdf_path)
        if not extracted_text:
            raise ValueError("No text extracted from PDF")
        print(f"📝 Extracted {len(extracted_text.split())} words from {page_count} pages")
        
        # Step 3: Generate content
        print("🎨 Generating social media content...")
        results = []
        
        # YouTube Documentary
        if "YouTube" in CONFIG["platforms"]:
            output_path = figure_dir / "YouTube/documentary_script.txt"
            success = generators["story"].generate_legacy_story(
                figure_name, extracted_text, output_path)
            results.append(("YouTube", success))
        
        # Facebook Post
        if "Facebook" in CONFIG["platforms"]:
            output_path = figure_dir / "Facebook/legacy_post.txt"
            success = generators["post"].generate_legacy_post(
                figure_name, extracted_text, output_path)
            results.append(("Facebook", success))
        
        # Blog Article
        if "Blog" in CONFIG["platforms"]:
            output_path = figure_dir / "Blog/impact_article.txt"
            success = generators["blog"].generate_legacy_article(
                figure_name, extracted_text, output_path)
            results.append(("Blog", success))
        
        # Print results
        print("\n📊 Generation Results:")
        for platform, success in results:
            print(f"{'✅' if success else '❌'} {platform.ljust(10)} → {output_path.parent}")
        
        return all(success for _, success in results)
    
    except Exception as e:
        print(f"⚠️ Error processing {figure_name}: {str(e)}")
        return False

def main():
    try:
        # Initialize clients
        print("🚀 Initializing content generators...")
        openai_client = OpenAIClient(api_key=CONFIG["openai_key"])
        generators = {
            "story": LegacyStoryGenerator(openai_client),
            "post": LegacyPostGenerator(openai_client),
            "blog": LegacyBlogGenerator(openai_client)
        }
        
        # Step 1: Read names
        print("\n📊 Reading historical figures list...")
        names = get_names_from_excel(CONFIG["input_file"])
        if not names:
            raise ValueError("No names found in Excel file")
        
        # Limit number of figures to process
        names = names[:CONFIG["max_figures"]]
        print(f"🧑‍🤝‍🧑 Found {len(names)} figures to process")
        
        # Step 2: Create output base
        output_base = Path(CONFIG["output_dir"])
        output_base.mkdir(exist_ok=True)
        
        # Process each figure
        success_count = 0
        for name in names:
            if process_figure(name, generators, output_base):
                success_count += 1
        
        # Final report
        print("\n" + "="*50)
        print(f"🏁 Processing complete! Success rate: {success_count}/{len(names)} figures")
        print(f"📂 Output directory: {output_base.resolve()}")
        
    except Exception as e:
        print(f"\n🔥 Critical error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
