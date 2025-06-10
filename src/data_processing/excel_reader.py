import pandas as pd

def read_names_from_excel(file_path: str, column: str = 'Name') -> list:
    """Read names from Excel column"""
    df = pd.read_excel(file_path)
    return df[column].dropna().tolist()
