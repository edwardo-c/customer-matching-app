import pandas as pd
import string
import re

SUFFIXES = ['inc', 'llc', 'ltd', 'co']
PATTERN = "|".join(f"\\b" + s + f"\\b" for s in SUFFIXES)

def replace_ampersand(text: str) -> str:
    
    text = text.replace("&", "and")
    return text

def remove_punctuation(text: str):
    return text.translate(str.maketrans("", "", string.punctuation))

def remove_suffixes(text: str):
    return re.sub(PATTERN, "", text)

def remove_multiple_spaces(text: str):
    return re.sub(r'  +', "", text)

def normalize_str(text: str):
    text = text.lower()
    text = replace_ampersand(text)
    text = remove_punctuation(text)
    text = remove_suffixes(text)
    text = remove_multiple_spaces(text)
    text = text.strip()
    return text

def normalize_col(df: pd.DataFrame, col_in_name: str, col_out_name: str) -> pd.DataFrame:
    df[col_out_name] = df[col_in_name].astype(str).apply(normalize_str)
    return df
