import streamlit as st

from config import (APP_PATHS, VENDOR_CUSTOMERS_CFG)
from context import get_app_context
from data_commands.commands import get_data
from refresh.vendor_customers import import_new_vendor_customers
from ui.sibling_candidates import render_sibling_candidates

ctx = get_app_context(APP_PATHS)

st.set_page_config(layout="wide")
st.title("POS Cross Reference")

# ==== Sidebar =====
with st.sidebar:
    if st.button("Load New Vendor Customers"):
        import_new_vendor_customers(VENDOR_CUSTOMERS_CFG, ctx.db_conn)
            
sibling_candidates, history, entities = st.tabs(["Sibling Candidates", "History", "Entities"])

with sibling_candidates:
    render_sibling_candidates(ctx.db_conn)

with history:
    ...

with entities:
    ...


