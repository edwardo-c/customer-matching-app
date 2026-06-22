"""Prepare data grid for vendor siblings"""

import pandas as pd

def drop_helper_columns(df: pd.DataFrame) -> pd.DataFrame:
    _df = df.copy()
    return df.drop(columns=["max_id", "min_id", "has_parent", "sort_index",])

def dedupe(df: pd.DataFrame) -> pd.DataFrame:
    """
    dedupe bi-direction id matching 
    
    dataset contains rows like: id_1 -> id_2 and id_2 -> id_1

    dedupe() corrects this duplication, assumes dataframe is presorted
    """
    _df = df.copy()

    _df.drop_duplicates(subset=["max_id", "min_id"], keep="first")

    mask = _df["has_parent"]

    deduped_true_rows = _df.loc[mask].drop_duplicates(
        subset=["left_vendor_customer_id", "right_parent_account_id"], 
        keep="first"
    )

    unchanged_false_rows = _df.loc[~mask]

    return pd.concat([deduped_true_rows, unchanged_false_rows], ignore_index=True)

def sort_vendor_siblings(df: pd.DataFrame) -> pd.DataFrame:
    _df = df.copy()
    return _df.sort_values(by=["sort_index", "left_vendor_customer_id"])

def get_sort_value(row: pd.Series):
    """
    provides a priority sorting value, assumes schema
    """
    match_type = row["match_type"]
    has_parent = row["has_parent"]
    
    match (match_type, has_parent):
        case ("token_zip", True):
            return 1
    
        case ("token_zip", False):
            return 2
        
        case ("zip_only", True):
            return 3
    
        case ("zip_only", False):
            return 4
    
        case ("token_only", True):
            return 5
    
        case ("token_only", False):
            return 6

def add_columns(df: pd.DataFrame) -> pd.DataFrame:
    _df = df.copy()

    _df.insert(0, 'decision', None, False)

    _df["max_id"] = _df[["left_vendor_customer_id", "right_vendor_customer_id"]].max(axis=1)
    _df["min_id"] = _df[["left_vendor_customer_id", "right_vendor_customer_id"]].min(axis=1)

    _df['has_parent'] = pd.notna(_df[['right_parent_account_id']])

    _df['sort_index'] = _df.apply(get_sort_value, axis=1)

    return _df

def prepare_vendor_siblings_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    prepares vendor_siblings_df for user consupmtion

    adds decision column, sorts, and drops duplicates
    """

    df = add_columns(df)
    df = sort_vendor_siblings(df)
    df = dedupe(df)
    df = drop_helper_columns(df)

    return df
