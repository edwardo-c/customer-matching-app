import streamlit as st
import duckdb

from config import (
    DB_PATH, 
    WORKFLOW_TAB_CFG, 
    SIDEBAR_RELATIONSHIP_CFG
)
from ui.sidebar import render_add_parent_form, render_relationship_forms
from ui.tabs import render_checkbox_controlled_dataframes

conn = duckdb.connect(DB_PATH)

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
    render_checkbox_controlled_dataframes(WORKFLOW_TAB_CFG, conn)

# ==== Sidebar =====
with st.sidebar:
    
    action = st.selectbox("Action", ("Add Relationship", "Add Parent"))
    
    if action == "Add Parent": render_add_parent_form(conn)
    
    if action == "Add Relationship": 
        render_relationship_forms(SIDEBAR_RELATIONSHIP_CFG, conn)
