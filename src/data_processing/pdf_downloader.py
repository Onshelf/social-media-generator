from pathlib import Path
import requests
from urllib.parse import quote

def download_wikipedia_pdf(figure_name: str, save_path: Path, timeout: int = 30) -> Path:
    """
    Downloads Wikipedia page as PDF
    Args:
        figure_name: Name of historical figure
        save_path: Directory where PDF should be saved
        timeout: Download timeout in seconds
    Returns:
        Path to downloaded PDF file
    """
    base_url = "https://en.wikipedia.org/api/rest_v1/page/pdf/"
    encoded_name = quote(figure_name)
    pdf_url = f"{base_url}{encoded_name}"
    
    output_path = save_path / f"{figure_name.replace(' ', '_')}.pdf"
    
    try:
        response = requests.get(pdf_url, timeout=timeout)
        response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            f.write(response.content)
            
        return output_path
        
    except Exception as e:
        print(f"⚠️ Failed to download PDF for {figure_name}: {str(e)}")
        raise
