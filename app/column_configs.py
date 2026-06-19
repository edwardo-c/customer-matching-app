import streamlit as st

SUGGESTED_VENDOR_SIBLINGS_CFG = {
  'decision': st.column_config.SelectboxColumn(
      "Decision",
      options=["accept", "reject"], 
      disabled=False,
      width=180
  ),

  'left_vendor_name': st.column_config.TextColumn(
      "Distributor",
      disabled=True
  ),

  'left_raw_vendor_customer_name': st.column_config.TextColumn(
      "Raw Customer Name",
      disabled=True
  ),

  'left_normalized_billing_zip': st.column_config.TextColumn(
      "Normalized Billing Zip",
      disabled=True
  ),

  'left_billing_state': st.column_config.TextColumn(
      "Raw Billing State",
      disabled=True
  ),

  'right_vendor_name': st.column_config.TextColumn(
      "Potential Sibling - Distributor",
      disabled=True
  ),

  'right_raw_vendor_customer_name': st.column_config.TextColumn(
      "Potential Sibling - Raw Customer Name",
      disabled=True
  ),

  'right_normalized_billing_zip': st.column_config.TextColumn(
      "Potential Sibling - Normalized Billing Zip",
      disabled=True
  ),

  'right_billing_state': st.column_config.TextColumn(
      "Potential Sibling - Raw Billing State",
      disabled=True
  ),

  'match_type': st.column_config.TextColumn(
      "Match Type",
      disabled=True
  ),

  'left_vendor_customer_id' : st.column_config.NumberColumn(
      "Customer ID",
      disabled=True
  ),

  'right_vendor_customer_id': st.column_config.NumberColumn(
      "Sibling ID",
      disabled=True
  ),

  'right_normalized_vendor_customer_name': None, 
  'left_normalized_vendor_customer_name': None,
  'right_first3_token': None,
  'right_raw_billing_zip': None,
  'left_first3_token': None,
  'left_raw_billing_zip': None,
  
}
