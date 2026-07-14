import pandas as pd

class DecisionOption:
    COL_NAME = 'Decision'
    ACCEPTED = "accept"
    REJECTED = "reject"

class SiblingTableConfig:
    LEFT_COL = 'left_vendor_customer_id'
    RIGHT_COL = 'right_vendor_customer_id'
    ACCEPTED = "vendor_customer_sibling_map"
    REJECTED = "rejected_vendor_customer_sibling_map"

def extract_accepted_siblings_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns only accept subset from the dataframe
    """
    if df.empty:
        return df
    else:
        _df = df.copy()
        _df = _df[_df[DecisionOption.COL_NAME] == DecisionOption.ACCEPTED]
        return _df[[SiblingTableConfig.LEFT_COL, SiblingTableConfig.RIGHT_COL]]
    
def extract_rejected_siblings_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns only reject subset from the dataframe
    """
    if df.empty:
        return df
    else:
        _df = df.copy()
        _df = _df[_df[DecisionOption.COL_NAME] == DecisionOption.ACCEPTED]
        return _df[[SiblingTableConfig.LEFT_COL, SiblingTableConfig.RIGHT_COL]]

def add_decision_col(df: pd.DataFrame) -> pd.DataFrame:
    """Inserts a Decision column at index 0"""
    _df = df.copy()
    _df.insert(0, DecisionOption.COL_NAME, None)
    return _df

def get_empty_sibling_decision_table() -> pd.DataFrame:
    return pd.DataFrame(
        columns=[SiblingTableConfig.LEFT_COL, SiblingTableConfig.RIGHT_COL]
    )

def extract_all_decisions(df: pd.DataFrame) -> pd.DataFrame:
    return df[df[DecisionOption.COL_NAME].notna()]