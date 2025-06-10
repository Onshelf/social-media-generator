import os
from pathlib import Path

def create_folder_structure(base_dir: str, name: str, subfolders: list) -> Path:
    """Create platform subfolders"""
    root = Path(base_dir) / name
    root.mkdir(parents=True, exist_ok=True)
    
    for platform in subfolders:
        (root / platform).mkdir(exist_ok=True)
    
    return root
