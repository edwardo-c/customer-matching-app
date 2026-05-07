import pandas as pd
from pathlib import Path


def load_data(file_path: Path) -> pd.DataFrame:
    """
    reads dataframe from file_path
    currently only supports .xlsx files with default params 
    (header = 0, sheet = 0, use all cols, etc)
    """
    return pd.read_excel(str(file_path))