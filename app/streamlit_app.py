import streamlit as st

from config import (APP_PATHS)
from data_commands.context import get_app_context
from data_commands.commands import add_parent, get_data, bulk_insert_relationships

ctx = get_app_context(APP_PATHS)

st.set_page_config(layout="wide")
st.title("POS Cross Reference")

# ==== Sidebar =====
with st.sidebar:
    with st.form("my_form", clear_on_submit=True):
        parent_name = st.text_input("Enter New Parent")
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.write(f"Parent {parent_name} submitted")
            add_parent(ctx.db_conn, parent_name)

# ===== Tabs ======
vendor_to_parent_suggestions, vendor_to_erp_suggestions, history, entities = st.tabs([
    "vendor_to_parent_suggestions",
    "vendor_to_erp_suggestions", 
    "History", 
    "Entities"
])

with vendor_to_parent_suggestions: 
    vendor_to_parent_candidates_df = get_data(ctx.db_conn, "vendor_to_parent_candidates")
    selection = st.dataframe(
        vendor_to_parent_candidates_df,
        on_select="rerun",
        selection_mode="multi-row")

    # selected_indices = selection.selection.rows

    # if selected_indices:
    #     selected_parent_child_id_df = (
    #         vendor_to_parent_candidates_df
    #         .iloc[selected_indices]
    #         [["vendor_customer_id", "parent_account_id"]]
    #     )

    #     if st.button("accept selected"):
    #         bulk_insert_relationships(
    #             ctx.db_conn,
    #             target_table="vendor_customer_to_parent_account_map", 
    #             parent_child_id_df=selected_parent_child_id_df
    #         )
            
    #     if st.button("reject selected"):
    #                     bulk_insert_relationships(
    #             ctx.db_conn,
    #             target_table="mismatch_vendor_customer_to_parent_account_map", 
    #             parent_child_id_df=selected_parent_child_id_df
    #         )

with vendor_to_erp_suggestions:
    vendor_to_erp_candidates_df = get_data(ctx.db_conn, "vendor_to_erp_candidates")

    selection = st.dataframe(
        vendor_to_erp_candidates_df,
        on_select="rerun",
        selection_mode="multi-row",
        key="vendor_to_erp_candidates_table"
    )

    selected_indices = selection.selection.rows

    if selected_indices:
        st.session_state["selected_vendor_to_erp_ids"] = (
            vendor_to_erp_candidates_df
            .iloc[selected_indices]
            [["vendor_customer_id", "erp_account_id"]]
        )

        if st.button("accept vendor to erp relationship"):
            bulk_insert_relationships(
                ctx.db_conn,
                target_table="vendor_customer_to_erp_account_map", 
                parent_child_id_df=st.session_state["selected_vendor_to_erp_ids"]
            )
            
        if st.button("reject vendor to erp relationship"):
            bulk_insert_relationships(
                ctx.db_conn,
                target_table="mismatch_vendor_customer_to_erp_account_map", 
                parent_child_id_df=st.session_state["selected_vendor_to_erp_ids"]
            )


with history:
    st.write("history here")

with entities:
    st.dataframe(get_data(ctx.db_conn, "parent_accounts"))
    st.dataframe(get_data(ctx.db_conn, "vendor_customers"))
    st.dataframe(get_data(ctx.db_conn, "erp_accounts"))