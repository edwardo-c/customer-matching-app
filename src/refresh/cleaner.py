import pandas as pd
import re

US_RE = r"^\d{5}"
CA_RE = r'^([ABCEGHJ-NPRSTVXY]\d[ABCEGHJ-NPRSTV-Z])\s?(\d[ABCEGHJ-NPRSTV-Z]\d)\s*$'

def add_cleaned_zip_col(
        *, 
        df: pd.DataFrame,
        col_in_name: str,
        col_out_name: str
    ) -> pd.DataFrame:
    """
    add a new column called (col_out_name) contianing the cleaned zip code from df[in_name].
    """
    _df = df.copy()
    _df[col_out_name] = _df[col_in_name].astype('string').apply(clean_zip)
    return _df

def clean_zip(s: str) -> str:
    """
    wrapper for a simplified .apply() call
    """

    return extract_zip_code(clean_string(s))

def clean_string(s: str) -> str:
    if isinstance(s, str):
        normalized = s.upper().strip().replace(".0", "").replace("-", "").zfill(5)
        return normalized[0] + normalized[1:].replace(" ", "")
    else:
        return ""

def extract_zip_code(zip_code: str) -> str:
    """
    returns a 5 digit us zip or 6 character canadian zip from an alphanumeric string
    returns empty string if no match is found
    """
    us_match = re.match(US_RE, zip_code)
    ca_match = re.match(CA_RE, zip_code)

    if not us_match is None:
        return us_match[0]
    elif not ca_match is None:
        return ca_match[0]
    else:
        return None


