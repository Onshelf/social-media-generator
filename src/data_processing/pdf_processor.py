import PyPDF2
from pathlib import Path
from typing import Optional

def extract_text_from_pdf(pdf_path: Path) -> Optional[str]:
    """
    Extracts all text from a PDF file
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Extracted text as string, or None if failed
    """
    try:
        text = ""
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return None
