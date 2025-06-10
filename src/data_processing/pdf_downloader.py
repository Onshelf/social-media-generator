import requests
from pathlib import Path

def download_wikipedia_pdf(page_title: str, save_dir: Path) -> Path:
    """Download Wikipedia PDF for a given title"""
    url = f"https://en.wikipedia.org/api/rest_v1/page/pdf/{page_title.replace(' ', '_')}"
    response = requests.get(url)
    response.raise_for_status()
    
    pdf_path = save_dir / f"{page_title}.pdf"
    pdf_path.write_bytes(response.content)
    
    return pdf_path
