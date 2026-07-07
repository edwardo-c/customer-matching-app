import streamlit as st

VENDOR_CUSTOMER_SIBLING_CANDIDATES_CFG = {
    'Decision': st.column_config.SelectboxColumn(
      "Decision",
      options=["accept", "reject"], 
      disabled=False,
      width=180
  ),

    'left_vendor_customer_id' : None,

    'left_vendor_name': st.column_config.TextColumn(
      "Distributor",
      disabled=True
    ),

    'left_raw_vendor_customer_name': st.column_config.TextColumn(
      "Customer Name",
      disabled=True
    ),

    'left_billing_state': st.column_config.TextColumn(
      "Billing State",
      disabled=True
    ),

    'left_normalized_billing_zip': st.column_config.TextColumn(
      "Billing Zip",
      disabled=True
    ),

    # RIGHT =====================
    'right_vendor_customer_id': None,

    'right_vendor_name': st.column_config.TextColumn(
      "Sibling Candidate - Distributor",
      disabled=True
    ),

    'right_raw_vendor_customer_name': st.column_config.TextColumn(
      "Sibling Candidate - Customer Name",
      disabled=True
    ),

    'right_billing_state': st.column_config.TextColumn(
      "Sibling Candidate - Billing State",
      disabled=True
    ),

    'right_normalized_billing_zip': st.column_config.TextColumn(
      "Sibling Candidate - Billing Zip",
      disabled=True
    ),

    'priority': None
}
