import streamlit as st
import duckdb
from customer_matching.commands import (
    get_data, 
    get_vw, 
    parse_relationship_results, 
    RELATION_REGISTRY
)

from config import DB_PATH
from ui.forms import render_add_parent_form, render_relationship_form

conn = duckdb.connect(DB_PATH)

st.title("POS Cross Reference")
tab1, tab2, tab3 = st.tabs(["Overview", "Workflow", "Relationships"])

with tab1:
    st.write("Count of unmatched Vendor Customers")
    col1, col2, col3 = st.columns(3)
    col1.metric("Count of Unmatched Vendors", "500", "8%")
    col2.metric("Users", "1,204", "12%")
    col3.metric("Latency", "42ms", "-3%")

with tab2:
    
    tab2_col1, tab2_col2, tab2_col3 = st.columns(3)

    with tab2_col1:
        show_parents = st.checkbox("Show Parent Accounts")
    with tab2_col2:
        show_vendor_customers = st.checkbox("Show Vendor Customers")
    with tab2_col3:
        show_erp_customers = st.checkbox("Show ERP Accounts")

    if show_parents:
        st.caption("Parent Accounts")
        st.dataframe(get_data(conn, "parent_accounts"), hide_index=True, width="stretch")
    if show_vendor_customers:
        st.caption("Vendor Customers")
        st.dataframe(get_data(conn, "vendor_customers"), hide_index=True, width="stretch")
    if show_erp_customers:
        st.caption("Acumatica Accounts")
        st.dataframe(get_data(conn, "erp_accounts"), hide_index=True, width="stretch")
         
with tab3:

    tab3_col1, tab3_col2, tab3_col3 = st.columns(3)
    with tab3_col1:
        show_vendor_cust_to_erp_acct = st.checkbox("Vendor Cust -> ERP")
    with tab3_col2:
        show_parents_to_vendor = st.checkbox("Vendor Cust -> Parents")
    with tab3_col3:
        show_erp_to_parent = st.checkbox("ERP Cust -> Parents")


    if show_vendor_cust_to_erp_acct:
        st.dataframe(get_vw(conn, "vendor_cust_to_erp_cust_vw"), hide_index=True, width="stretch")
    if show_parents_to_vendor:
        st.dataframe(get_vw(conn, "vendor_cust_to_parent_vw"), hide_index=True, width="stretch")
    if show_erp_to_parent:
        st.dataframe(get_vw(conn, "erp_cust_to_parent_vw"), hide_index=True, width="stretch") 

with st.sidebar:
        action = st.selectbox("Action", ("Add Relationship", "Add Parent"))
        
        if action == "Add Parent":
            render_add_parent_form(conn)

        if action == "Add Relationship":
            relationship_type = st.selectbox(
            "Relationship Type", 
            options=RELATION_REGISTRY.keys()
        )

            relationship_cfg = RELATION_REGISTRY[relationship_type]

            results = render_relationship_form(relationship_cfg)
            if results: 
                parse_relationship_results(relationship_cfg.target_table, results, conn)