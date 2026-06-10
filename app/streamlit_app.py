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
    with st.form("new_parent", clear_on_submit=True):
        parent_name = st.text_input("Enter New Parent")

        submitted = st.form_submit_button("Submit")

        if submitted:
            if parent_name:
                st.write(f"Parent {parent_name} submitted")
                add_parent(ctx.db_conn, parent_name)
    
    if st.button("Refresh Vendor Customers"):
        import_new_vendor_customers(VENDOR_CUSTOMERS_CFG, ctx.db_conn)


# ===== Tabs ======
review_queue, history, entities = st.tabs(["Review Queue", "History", "Entities"
])

with review_queue:
    if "candidate_index" not in st.session_state:
        st.session_state.candidate_index = 0

    if "candidate_df" not in st.session_state:
        st.session_state.candidate_df = get_data(
            ctx.db_conn, "potential_vendor_siblings"
        )

    if "max_candidate_idx" not in st.session_state:
        max_idx = st.session_state.candidate_df["candidate_index"].max()
        st.session_state.max_candidate_idx = max_idx
        if max_idx > 0:
            st.session_state.candidate_index = 1

    if "suggested_parents_df" not in st.session_state:
        st.session_state.suggested_parents_df = get_data(
            ctx.db_conn, "suggested_vendor_parents"
        )

    st.subheader(f"Candidate Group")

    col1, col2 = st.columns(2)

    candidates_df = st.session_state.candidate_df[
        st.session_state.candidate_df["candidate_index"] == st.session_state.candidate_index
    ]

    selected_siblings = st.dataframe(
        candidates_df, 
        selection_mode="multi-row", 
        on_select="rerun", 
        key="vendor_customer_candidate_siblings_df"
    )

    selected_siblings_idicies = selected_siblings.selection.rows

    if selected_siblings_idicies != []:

        st.session_state.selected_sibling_ids = tuple(
            candidates_df
            .iloc[selected_siblings_idicies]
            ["vendor_customer_id"]
        )

    # =================== Parent Selection =====================

    st.subheader(f"Suggested Parents")

    selected_parent = st.dataframe(
        st.session_state.suggested_parents_df, 
        selection_mode="single-row", 
        on_select="rerun",
        key="suggested_vendor_parent_df"
    )


    selected_parent_id = list(
        st.session_state.suggested_parents_df
        .iloc[selected_parent.selection.rows]
        ["parent_account_id"]
    )

    if selected_parent_id != []:
        st.session_state.selected_parent_id = selected_parent_id[0]

    with col1:
        if st.button("Previous"):
            if st.session_state.candidate_index > 0:
                st.session_state.candidate_index -= 1
            st.rerun()

    with col2:
        if st.button("Add To Parent"):
            # TODO: enforce suggested parent or other parent is selected

            add_vendor_ids_to_existing_parent_id(
                ctx.db_conn, 
                st.session_state.selected_sibling_ids, 
                st.session_state.selected_parent_id
            )
            
            del st.session_state.selected_sibling_ids
            del st.session_state.selected_parent_id
            
            if st.session_state.candidate_index > st.session_state.max_candidate_idx:
                st.session_state.candidate_index += 1
            
                                          
            st.rerun()


with history:
    st.write("history here")

with entities:
    st.dataframe(get_data(ctx.db_conn, "parent_accounts"), key="parent_accounts_df")
    st.dataframe(get_data(ctx.db_conn, "vendor_customers"), key="vendor_customers_df")
    st.dataframe(get_data(ctx.db_conn, "erp_accounts"), key="erp_accounts_df")