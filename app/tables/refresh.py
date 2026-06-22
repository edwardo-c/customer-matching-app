import streamlit as st

def increment_table_versions():
    st.session_state.vendor_customer_to_parent_suggestion_version += 1
    st.session_state.suggested_vendor_siblings_version += 1