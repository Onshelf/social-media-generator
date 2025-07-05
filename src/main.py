#!/usr/bin/env python3
"""
Social Media Content Generator - Modular Version
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.config.config_manager import ConfigManager
from src.processing.figure_processor import FigureProcessor
from src.data_processing.excel_reader import get_names_from_excel
from src.content_generation.openai_client import OpenAIClient

def main():
    """Main execution function"""
    try:
        config_manager = ConfigManager()
        
        print("🚀 Social Media Content Generator")
        print(f"📌 Target Platforms: {', '.join(config_manager.get_platforms())}")
        print(f"   - YouTube: Generates both post.txt and story.txt")
        
        # Rest of your main() function remains the same...
        # 1. Initialize OpenAI client
        client = OpenAIClient(api_key=config_manager.get_openai_key())
        
        # 2. Get names from input file
        names = get_names_from_excel(config_manager.get_input_file())
        if not names:
            raise ValueError("No names found in input file")
        names = names[:config_manager.get_max_figures()]
        print(f"\n🧑‍🤝‍🧑 Found {len(names)} figures to process")
        print(f"🔍 First figure: {names[0]}")

        # 3. Process each figure
        figure_processor = FigureProcessor(config_manager)
        success_count = 0
        for i, name in enumerate(names, 1):
            print(f"\n📌 Processing figure {i}/{len(names)}")
            if figure_processor.process_figure(name, client):
                success_count += 1

        # 4. Final report
        print("\n" + "="*50)
        print(f"🏁 Processing Complete")
        print(f"✅ Successful: {success_count}/{len(names)} figures")
        print(f"📂 Output Directory: {config_manager.get_output_dir().resolve()}")
        
        return 0 if success_count == len(names) else 1
        
    except Exception as e:
        print(f"\n🔥 Critical Error: {str(e)}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
