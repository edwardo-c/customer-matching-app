import pandas as pd
import string
import re

SUFFIXES = ['inc', 'llc', 'ltd', 'co']
PATTERN = "|".join(f"\\b" + s + f"\\b" for s in SUFFIXES)

def remove_punctuation(text: str):
    return text.translate(str.maketrans("", "", string.punctuation))

def remove_suffixes(text: str):
    return re.sub(PATTERN, "", text)

def remove_multiple_spaces(text: str):
    return re.sub(r' +', "", text)

def normalize_str(text: str):
    text = text.lower()
    text = remove_punctuation(text)
    text = remove_suffixes(text)
    text = remove_multiple_spaces(text)
    text = text.strip()
    return text

def normalize_customer_name(df: pd.DataFrame, name_col: str) -> pd.DataFrame:
    df["norm_name_col"] = df[name_col].astype(str).apply(normalize_str)
    return df
