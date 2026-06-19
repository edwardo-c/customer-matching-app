import streamlit as st

from config import (APP_PATHS, VENDOR_CUSTOMERS_CFG)
from data_commands.context import get_app_context
from data_commands.commands import get_data, bulk_insert_target_table, resolve_accepted_sibling_pair, add_parent
from refresh.vendor_customers import import_new_vendor_customers
from data_commands.db_schema import VendorCustomerToParentMap, RejectedVendorCustomerToParentMap
import pandas as pd
from column_configs import SUGGESTED_VENDOR_SIBLINGS_CFG

ctx = get_app_context(APP_PATHS)

st.set_page_config(layout="wide")
st.title("POS Cross Reference")

# ==== Sidebar =====
with st.sidebar:
    if st.button("Load New Vendor Customers"):
        import_new_vendor_customers(VENDOR_CUSTOMERS_CFG, ctx.db_conn)
            
review_queue, history, entities, manual_adjustments = st.tabs(
    ["Review Queue", "History", "Entities", "Manual Adjustments"]
)

with review_queue:
    with st.expander("View Vendor Customer To Existing Parent Suggestions"):

        accepted, rejected = st.columns(2)
        
        if "vendor_customer_to_parent_suggestion_version" not in st.session_state:
            st.session_state.vendor_customer_to_parent_suggestion_version = 0

        if "vendor_customer_to_parent_suggestion_df" not in st.session_state:
            st.session_state.vendor_customer_to_parent_suggestion_df = get_data(
                ctx.db_conn, relation_name="vendor_customer_to_parent_suggestions"
            )

        if "selected_vendor_customer_to_parent_df" not in st.session_state:
            st.session_state.selected_vendor_customer_to_parent_df = pd.DataFrame(
                columns=[VendorCustomerToParentMap.VENDOR_CUSTOMER_ID, VendorCustomerToParentMap.PARENT_ACCOUNT_ID]
            )

        vendor_customer_to_parent_row_selection = st.dataframe(
            st.session_state.vendor_customer_to_parent_suggestion_df,
            selection_mode="multi-row",
            on_select="rerun",
            key=f"vendor_customer_to_parent_suggestion_df_{st.session_state.vendor_customer_to_parent_suggestion_version}"
        )

        if vendor_customer_to_parent_row_selection.selection.rows != []:
            selected_rows = vendor_customer_to_parent_row_selection.selection.rows
            st.session_state.selected_vendor_customer_to_parent_df = (
                st.session_state.vendor_customer_to_parent_suggestion_df
                .iloc[selected_rows]
                [[VendorCustomerToParentMap.VENDOR_CUSTOMER_ID, VendorCustomerToParentMap.PARENT_ACCOUNT_ID]]
            )

        with accepted:
            if st.button("accept"):
                bulk_insert_target_table(
                    ctx.db_conn,
                    target_table=VendorCustomerToParentMap.TABLE,
                    staging_table_df=st.session_state.selected_vendor_customer_to_parent_df
                )
                del st.session_state.selected_vendor_customer_to_parent_df
                del st.session_state.vendor_customer_to_parent_suggestion_df
                st.session_state.vendor_customer_to_parent_suggestion_version += 1
                st.rerun()
            
        with rejected:
            if st.button("reject"):
                bulk_insert_target_table(
                    ctx.db_conn,
                    target_table=RejectedVendorCustomerToParentMap.TABLE,
                    staging_table_df=st.session_state.selected_vendor_customer_to_parent_df
                )
                del st.session_state.selected_vendor_customer_to_parent_df
                del st.session_state.vendor_customer_to_parent_suggestion_df
                st.session_state.vendor_customer_to_parent_suggestion_version += 1
                st.rerun()

    with st.expander("View Potential Siblings"):
        
        if "suggested_vendor_siblings_version" not in st.session_state:
            st.session_state.suggested_vendor_siblings_version = 0

        if "suggested_vendor_siblings_df" not in st.session_state:
            _suggested_vendor_siblings_df = get_data(
                ctx.db_conn, "suggested_vendor_siblings"
            )
            
            _suggested_vendor_siblings_df.insert(0, 'decision', None)

            st.session_state.suggested_vendor_siblings_df = _suggested_vendor_siblings_df

        if "selected_siblings_ids_df" not in st.session_state:
            st.session_state.selected_siblings_ids_df = pd.DataFrame(
                columns=['left_vendor_customer_id','right_vendor_customer_id']
            )

        decisions_df = st.data_editor(
            st.session_state.suggested_vendor_siblings_df,
            column_config=SUGGESTED_VENDOR_SIBLINGS_CFG,
            key=f"suggested_vendor_siblings_df_{st.session_state.suggested_vendor_siblings_version}",
            hide_index=True,
        )

        if st.button("submit relationships"):
            siblings_ids_to_process_df = (
                decisions_df
                [decisions_df['decision'].notna()]
                [['left_vendor_customer_id', 'right_vendor_customer_id']]
            )

            resolve_accepted_sibling_pair(
                ctx.db_conn, 
                sibling_ids_df=siblings_ids_to_process_df
            )

with history:
    st.write("history here")

with entities:
    st.dataframe(get_data(ctx.db_conn, "parent_accounts"), key="parent_accounts_df")
    st.dataframe(get_data(ctx.db_conn, "vendor_customers_vw"), key="vendor_customers_df")
    st.dataframe(get_data(ctx.db_conn, "erp_accounts"), key="erp_accounts_df")


with manual_adjustments:
    with st.form("add new parent"):
        new_parent = st.text_input("enter new parent")
        submitted = st.form_submit_button(label="submit")
        if submitted:
            add_parent(ctx.db_conn, new_parent)
