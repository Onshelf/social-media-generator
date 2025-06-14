from pathlib import Path
from typing import List

def create_folder_structure(base_dir: Path, figure_name: str, platforms: List[str]) -> Path:
    """
    Creates folder structure for a historical figure
    Returns Path to the figure's main directory
    """
    figure_dir = base_dir / figure_name.replace(" ", "_")
    figure_dir.mkdir(parents=True, exist_ok=True)
    
    for platform in platforms:
        (figure_dir / platform).mkdir(exist_ok=True)
    
    return figure_dir
