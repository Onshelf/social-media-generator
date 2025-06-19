import pypdf
from pathlib import Path
from typing import Optional, Tuple, List
import logging

class PDFProcessor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def extract_content(self, pdf_path: Path, output_dir: Path) -> Tuple[Optional[str], int, List[Path]]:
        """
        Extracts text and images from a PDF file
        
        Args:
            pdf_path: Path to the PDF file
            output_dir: Directory where extracted content should be saved
            
        Returns:
            Tuple containing (extracted_text, page_count, saved_image_paths)
            Returns (None, 0, []) if extraction fails
        """
        page_count = 0
        saved_images = []
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = pypdf.PdfReader(file)
                page_count = len(pdf_reader.pages)
                text_parts = []
                
                # Create extracted_pics directory if it doesn't exist
                pics_dir = output_dir / "extracted_pics"
                pics_dir.mkdir(exist_ok=True)
                
                for i, page in enumerate(pdf_reader.pages):
                    # Extract text
                    page_text = page.extract_text() or f"<Page {i+1} contains no extractable text>"
                    text_parts.append(page_text)
                    
                    # Extract images
                    if '/XObject' in page['/Resources']:
                        x_object = page['/Resources']['/XObject'].get_object()
                        
                        for obj in x_object:
                            if x_object[obj]['/Subtype'] == '/Image':
                                image = x_object[obj]
                                try:
                                    image_data = image.get_data()
                                    
                                    # Determine image extension
                                    if '/Filter' in image:
                                        if image['/Filter'] == '/FlateDecode':
                                            ext = '.png'
                                        elif image['/Filter'] == '/DCTDecode':
                                            ext = '.jpg'
                                        elif image['/Filter'] == '/JPXDecode':
                                            ext = '.jp2'
                                        else:
                                            ext = '.img'
                                    else:
                                        ext = '.img'
                                    
                                    # Save image directly to extracted_pics folder
                                    image_name = f"{pdf_path.stem}_page{i+1}_{obj[1:]}{ext}"
                                    image_path = pics_dir / image_name
                                    
                                    with open(image_path, 'wb') as img_file:
                                        img_file.write(image_data)
                                    
                                    saved_images.append(image_path)
                                    self.logger.info(f"Saved image: {image_path}")
                                except Exception as img_e:
                                    self.logger.error(f"Failed to extract image: {img_e}")
                
                text = "\n".join(text_parts)
                self.logger.info(f"Successfully processed {pdf_path.name}, pages: {page_count}, images saved: {len(saved_images)}")
                return text, page_count, saved_images
                
        except pypdf.PdfException as e:
            self.logger.error(f"PDF processing error for {pdf_path.name}: {e}")
        except Exception as e:
            self.logger.error(f"Unexpected error processing {pdf_path.name}: {e}")
            
        return None, page_count, saved_images
