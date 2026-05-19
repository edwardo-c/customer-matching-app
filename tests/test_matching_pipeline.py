import pandas as pd
from customer_matching.matcher import MatchingPipeline
from customer_matching.normalizer import normalize_col

# mock of vendor_customers
_LEFT = pd.DataFrame(
    {
        'id':    [1,2,3,4],
        'name':  ['ademco', 'ADEMCO INC', 'vital tech inc', 'virtual technology'],
        'state': ['IL', 'IL', 'WI', 'WI'],
        'zip':   ['60504', '60504', '31233', '98100']
     }
)
LEFT = normalize_col(df=_LEFT, col_in_name='name', col_out_name="normalized_name")

# mock of erp_accounts
_RIGHT = pd.DataFrame(
    {
        'id':    [1,2,3,4],
        'name':  ['Center Stage', 'Ademco LLC', 'Vital Tech Inc.', 'BestPurchase'],
        'state': ['IL', 'IL', 'WI', 'WI'],
        'zip':   ['60504', '60504', '31233', '31233']
     }
)
RIGHT = normalize_col(df=_RIGHT, col_in_name='name', col_out_name="normalized_name")

# ================== TESTS ===========================

def test_build_query_statement():

    result = MatchingPipeline.build_query_statement(
        cols=['col_a', 'col_b', 'col_c'],
        filter_values=('filter_a', 'filter_b', 'filter_c')
    )
    
    expected = "col_a == 'filter_a' and col_b == 'filter_b' and col_c == 'filter_c'"
    assert result == expected


def test_matching_pipeline():
    matcher = MatchingPipeline(
        left_df=LEFT,
        left_column_name="normalized_name",
        right_df=RIGHT,
        right_column_name="normalized_name",
        column_subset={'state': 'state', 'zip': 'zip'}
    )

    matcher.run()
    
    breakpoint()
