import streamlit as st

from config import (
    APP_PATHS, 
    MATCH_CFG,
    WORKFLOW_TAB_CFG, 
    SIDEBAR_RELATIONSHIP_CFG
)
from ui.sidebar import render_add_parent_form, render_relationship_forms
from ui.tabs import render_checkbox_controlled_dataframes
from data_commands.context import get_app_context
from data_commands.refresh import refresh_app_data

ctx = get_app_context(APP_PATHS)
st.set_page_config(layout="wide")
st.title("POS Cross Reference")


# ===== Tabs ======
overview, workflow, candidates = st.tabs(["Overview", "Workflow", "Candidates"])

with overview:
    st.write("Count of unmatched Vendor Customers")
    col1, col2, col3 = st.columns(3)
    col1.metric("Count of Unmatched Vendors", "500", "8%")
    col2.metric("Users", "1,204", "12%")
    col3.metric("Latency", "42ms", "-3%")

with workflow:
    render_checkbox_controlled_dataframes(WORKFLOW_TAB_CFG, ctx.db_conn)

with candidates:
    st.write("candidates workflow")

# ==== Sidebar =====
with st.sidebar:
    if st.button("Refresh All Data"):  refresh_app_data(ctx, MATCH_CFG)

    action = st.selectbox("Action", ("Add Relationship", "Add Parent"))
    
    if action == "Add Parent": render_add_parent_form(ctx.db_conn)
    
    if action == "Add Relationship": 
        render_relationship_forms(SIDEBAR_RELATIONSHIP_CFG, ctx.db_conn)
