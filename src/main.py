from data_processing.excel_reader import get_names_from_excel
from data_processing.file_manager import create_folder_structure
from data_processing.pdf_downloader import download_wikipedia_pdf

def main():
    # Configuration
    INPUT_FILE = "input/Names.xlsx"
    OUTPUT_DIR = "generated_content"
    PLATFORMS = ['Youtube', 'Facebook', 'Tiktok', 'Instagram', 'Blogger', 'Audio']
    
    try:
        # Step 1: Read names
        names = read_names_from_excel(INPUT_FILE, column='Name')
        if not names:
            raise ValueError("No names found in the Excel file")
        
        # Step 2: Process first name
        first_name = names[0]
        
        # Step 3: Create folder structure
        root_folder = create_folder_structure(
            base_dir=OUTPUT_DIR,
            name=first_name,
            subfolders=PLATFORMS
        )
        
        # Step 4: Download PDF
        pdf_path = download_wikipedia_pdf(first_name, root_folder)
        print(f"Successfully processed {first_name}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
