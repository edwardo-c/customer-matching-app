import pandas as pd
import string
import re
import logging
"""
replace dashes with a space, then clear consecutive spaces
"""

STOP_WORDS = [
    'the', 'a', 'an', "dll",
    'inc', 'llc', 'corp', 'company', 'co', 'ltd', 'holdings', 'group'
]

PATTERN = "|".join(f"\\b" + s + f"\\b" for s in STOP_WORDS)

def convert_to_spaces(text: str) -> str:
    CHARS = ["-", "/", ]
    for c in CHARS:
        t = text.replace(c, " ")
    return t

def replace_ampersand(text: str) -> str:
    text = text.replace("&", "and")
    return text

def remove_punctuation(text: str)  -> str:
    return text.translate(str.maketrans("", "", string.punctuation))

def remove_suffixes(text: str)  -> str:
    return re.sub(PATTERN, "", text)

def remove_multiple_spaces(text: str)  -> str:
    return re.sub(r'  +', " ", text)

def normalize_str(text: str):
    if isinstance(text, str):
        text = text.lower()
        text = replace_ampersand(text)
        text = convert_to_spaces(text)
        text = remove_punctuation(text)
        text = remove_suffixes(text)
        text = remove_multiple_spaces(text)
        text = text.strip()
        return text
    else:
        logging.error(f"{text} is not type str, skipping normalization")
        return None

def add_normalized_name_col(
        *, 
        df: pd.DataFrame, 
        col_in_name: str, 
        col_out_name: str
    ) -> pd.DataFrame:
    """
    normalize specified column 
    return DataFrame with col_out_name added holding normalized values
    and "is_str" used for debugging, normalization is only applied to str data types
    """
    df[col_out_name] = df[col_in_name].astype(str).apply(normalize_str)
    return df

def add_first3_token(
        *,
        df: pd.DataFrame, 
        col_in_name: str, 
        col_out_name: str
    ):
    
    df[col_out_name] = df[col_in_name].apply(lambda x: x.replace(" ", "")[0:3])
    return df

