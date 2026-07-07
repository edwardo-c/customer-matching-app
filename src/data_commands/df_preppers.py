import pandas as pd

def prep_vendor_customer_sibling_candidates_df(
        raw_df: pd.DataFrame
    ):
    """
    prepares vendor_customer_sibling_candidates_df for ui
    """
    _df = raw_df.copy()
    _df.insert(0, "Decision", None)
    _df.sort_values(by=["priority", "left_raw_vendor_customer_name"], inplace=True)
    return _df