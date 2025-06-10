from data_processing.excel_reader import get_names_from_excel
from data_processing.file_manager import create_folder_structure
from data_processing.pdf_downloader import download_wikipedia_pdf
from data_processing.pdf_processor import extract_text_from_pdf

def main():
    # Configuration
    INPUT_FILE = "input/Names.xlsx"
    OUTPUT_DIR = "generated_content"
    PLATFORMS = ['Youtube', 'Facebook', 'Tiktok', 'Instagram', 'Blogger', 'Audio']
    
    try:
        # Step 1: Read names
        names = get_names_from_excel(INPUT_FILE, column='Name')
        if not names:
            raise ValueError("No names found in the Excel file")
        
        # Step 2: Process first name
        first_name = names[0]
        print(f"🔄 Processing: {first_name}")
        
        # Step 3: Create folder structure
        root_folder = create_folder_structure(
            base_dir=OUTPUT_DIR,
            name=first_name,
            subfolders=PLATFORMS
        )
        print(f"📁 Created folder structure at: {root_folder}")
        
        # Step 4: Download PDF
        pdf_path = download_wikipedia_pdf(first_name, root_folder)
        print(f"📄 Downloaded Wikipedia PDF to: {pdf_path}")
        
        # Step 5: Extract text from PDF
        extracted_text = extract_text_from_pdf(pdf_path)
        if extracted_text:
            text_file = root_folder / "extracted_text.txt"
            text_file.write_text(extracted_text)
            print(f"✍️ Extracted {len(extracted_text)} characters to: {text_file}")
            
            # (Future integration point)
            # Here you can pass extracted_text to your content generators
            # e.g., generate_story(extracted_text)
            
        print(f"✅ Successfully processed {first_name}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        # Optionally: Add logging here

if __name__ == "__main__":
    main()
