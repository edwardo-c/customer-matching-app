import streamlit as st

from config import (
    APP_PATHS, 
    APP_DATA_REFRESH_CFG,
    CANDIDATES_TAB_CFG, 
    SIDEBAR_RELATIONSHIP_CFG
)
from ui.sidebar import render_add_parent_form, render_relationship_forms
from ui.tabs import render_checkbox_controlled_dataframes
from data_commands.context import get_app_context

from data_commands.refresh import refresh_app

ctx = get_app_context(APP_PATHS)

st.set_page_config(layout="wide")
st.title("POS Cross Reference")

# ===== Tabs ======
candidates, history = st.tabs(["Candidates", "History"])

# with workflow:
#     render_checkbox_controlled_dataframes(WORKFLOW_TAB_CFG, ctx.db_conn)

with candidates:
    render_checkbox_controlled_dataframes(CANDIDATES_TAB_CFG, ctx.db_conn)

with history:
    st.dataframe(ctx.db_conn.sql("SELECT * FROM batches").df())

# ==== Sidebar =====
with st.sidebar:
    if st.button("Refresh All Data"):  refresh_app(ctx, APP_DATA_REFRESH_CFG)

    action = st.selectbox("Action", ("Add Relationship", "Add Parent"))
    
    if action == "Add Parent": render_add_parent_form(ctx.db_conn)
    
    if action == "Add Relationship": 
        render_relationship_forms(SIDEBAR_RELATIONSHIP_CFG, ctx.db_conn)
