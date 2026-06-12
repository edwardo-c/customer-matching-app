import streamlit as st

from config import (APP_PATHS, VENDOR_CUSTOMERS_CFG)
from data_commands.context import get_app_context
from data_commands.commands import add_parent, get_data, add_vendor_ids_to_existing_parent_id
from refresh.vendor_customers import import_new_vendor_customers

ctx = get_app_context(APP_PATHS)

st.set_page_config(layout="wide")
st.title("POS Cross Reference")

# ==== Sidebar =====
with st.sidebar:    
    if st.button("Refresh Vendor Customers"):
        import_new_vendor_customers(VENDOR_CUSTOMERS_CFG, ctx.db_conn)


# ===== Tabs ======
review_queue, history, entities = st.tabs(["Review Queue", "History", "Entities"])

with review_queue:
    if "sibling_batch_index" not in st.session_state:
        st.session_state.sibling_batch_index = 0
    
    if "selected_siblings_ids" not in st.session_state:
        st.session_state.selected_siblings_ids = []

    if "selected_parent_id" not in st.session_state:
        st.session_state.selected_parent_id = None

    next, previous, accept = st.columns(3)

    # ==== Group Navigation ===== #
    with next: 
        if st.button("next group"):
            st.session_state.sibling_batch_index += 1
    
    with previous:
        if st.button("previous group"):
            st.session_state.sibling_batch_index -= 1

    # ==== Parent Workflow ==== #

    add_new_parent, suggested_parents = st.columns(2)

    if "suggested_parents_df" not in st.session_state:
        st.session_state.suggested_parents_df = get_data(
            ctx.db_conn, "suggested_vendor_parents"
        )

    with add_new_parent:
        with st.form("new_parent", clear_on_submit=True):
            parent_name = st.text_input("Enter New Parent")

            if st.form_submit_button("submit"):
                if parent_name:
                    st.write(f"Parent {parent_name} submitted")
                    add_parent(ctx.db_conn, parent_name)

    with suggested_parents:
        st.caption("Suggested Parents")

        st.caption("toggle suggested parents or all parents (sorted by newest to oldest)")

        selected_parent = st.dataframe(
            st.session_state.suggested_parents_df, 
            selection_mode="single-row", 
            on_select="rerun",
            key="suggested_vendor_parent_df"
        )
        
        parent_idx = selected_parent.selection.rows
        if parent_idx != []:
           parent_id = int(st.session_state.suggested_parents_df.iloc[parent_idx]["parent_account_id"].item())
           st.session_state.selected_parent_id = parent_id


    with accept:
        if st.button("submit relationship"):
            add_vendor_ids_to_existing_parent_id(
                ctx.db_conn, 
                st.session_state.selected_siblings_ids,
                st.session_state.selected_parent_id    
            )
            del st.session_state.selected_siblings_ids
            del st.session_state.selected_parent_id

    # =================================================

    if "potential_vendor_siblings" not in st.session_state:
        st.session_state.potential_vendor_siblings = get_data(
            ctx.db_conn, "potential_vendor_siblings"
        )
    
    siblings = st.dataframe(
        st.session_state.potential_vendor_siblings[
            st.session_state.potential_vendor_siblings["group_index"] == st.session_state.sibling_batch_index
        ],
        selection_mode="multi-row", 
        on_select="rerun",
        key="siblings_df"
    )

    selected_siblings_idicies = siblings.selection.rows

    if selected_siblings_idicies != []:
        st.session_state.selected_siblings_ids = tuple(
            st.session_state.potential_vendor_siblings
            .iloc[selected_siblings_idicies]
            ["vendor_customer_id"]
        )

with history:
    st.write("history here")

with entities:
    st.dataframe(get_data(ctx.db_conn, "parent_accounts"), key="parent_accounts_df")
    st.dataframe(get_data(ctx.db_conn, "vendor_customers"), key="vendor_customers_df")
    st.dataframe(get_data(ctx.db_conn, "erp_accounts"), key="erp_accounts_df")