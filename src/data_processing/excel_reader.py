# src/data_processing/excel_reader.py
import pandas as pd
from typing import List

def get_names_from_excel(file_path: str, column: str = "Name") -> List[str]:
    """Read names from specified Excel column"""
    df = pd.read_excel(file_path)
    return df[column].dropna().tolist()
