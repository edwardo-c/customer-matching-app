"""Prepare data grid for vendor siblings"""

import pandas as pd

def add_decisions(df: pd.DataFrame) -> pd.DataFrame:
    """
    add a new column to df called decision at index 0
    raises on duplicate column
    """
    _df = df.copy()
    _df.insert(0, 'decision', None, False)
    return _df

def add_max_min_id_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    add two columns [max_id, min_id], assumes column existence
    """
    _df = df.copy()
    _df["max_id"] = _df[["left_vendor_customer_id", "right_vendor_customer_id"]].max(axis=1)
    _df["min_id"] = _df[["left_vendor_customer_id", "right_vendor_customer_id"]].min(axis=1)
    return _df

def get_sort_value(row: pd.Series):
    """
    provides a priority sorting value, assumes schema
    """
    match_type = row["match_type"]
    has_parent = pd.notna(row["right_parent_account_id"])
    
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

def add_sort_order_column(df: pd.DataFrame) -> pd.DataFrame:
    """add sort_index column"""
    _df = df.copy()
    _df['sort_index'] = _df.apply(get_sort_value, axis=1)
    _df.sort_values(by=['sort_index', 'left_vendor_customer_id'], inplace=True)
    
    return _df

def dedupe(df: pd.DataFrame) -> pd.DataFrame:
    """
    dedupe bi-direction id matching 
    
    dataset contains rows like: id_1 -> id_2 and id_2 -> id_1

    dedupe() corrects this duplication, assumes dataframe is presorted
    """
    return df.drop_duplicates(subset=["max_id", "min_id"], keep="first")

def sort_vendor_siblings(df: pd.DataFrame) -> pd.DataFrame:
    _df = df.copy()
    return _df.sort_values(by=["sort_index", "left_vendor_customer_id"])

def drop_helper_columns(df: pd.DataFrame) -> pd.DataFrame:
    _df = df.copy()
    return df.drop(columns=["max_id", "min_id", "sort_index"])

def prepare_vendor_siblings_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    prepares vendor_siblings_df for user consupmtion

    adds decision column, sorts, and drops duplicates
    """
    df = add_decisions(df)
    df = add_sort_order_column(df)
    df = add_max_min_id_columns(df)
    df = sort_vendor_siblings(df)
    df = dedupe(df)
    df = drop_helper_columns(df)

    return df
