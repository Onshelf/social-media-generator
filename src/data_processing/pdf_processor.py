import PyPDF2
from pathlib import Path
from typing import Optional, Tuple
import logging

class PDFProcessor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def extract_text(self, pdf_path: Path) -> Tuple[Optional[str], int]:
        """
        Extracts text from a PDF file with proper error handling
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Tuple containing (extracted_text, page_count)
            Returns (None, 0) if extraction fails
        """
        page_count = 0  # Initialize page_count
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                page_count = len(pdf_reader.pages)  # Get actual page count
                text = "\n".join(
                    page.extract_text() or f"<Page {i+1} contains no extractable text>"
                    for i, page in enumerate(pdf_reader.pages)
                )
                
                self.logger.info(f"Successfully processed {pdf_path.name}, pages: {page_count}")
                return text, page_count
                
        except PyPDF2.PdfReadError as e:
            self.logger.error(f"PDF reading error for {pdf_path.name}: {e}")
        except Exception as e:
            self.logger.error(f"Unexpected error processing {pdf_path.name}: {e}")
            
        return None, page_count  # Returns 0 if exception occurred

    def save_text(self, text: str, output_path: Path) -> bool:
        """Saves extracted text to a file"""
        try:
            output_path.write_text(text)
            self.logger.info(f"Saved extracted text to {output_path}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to save text to {output_path}: {e}")
            return False
