import streamlit as st

from config import (APP_PATHS, VENDOR_CUSTOMERS_CFG)
from context import get_app_context
from data_commands.commands import get_data, bulk_insert_target_table, resolve_accepted_sibling_pair, add_parent
from refresh.vendor_customers import import_new_vendor_customers
import pandas as pd
from column_configs import VENDOR_CUSTOMER_SIBLING_CANDIDATES_CFG
from data_commands.df_preppers import prep_vendor_customer_sibling_candidates_df


ctx = get_app_context(APP_PATHS)

st.set_page_config(layout="wide")
st.title("POS Cross Reference")

# ==== Sidebar =====
with st.sidebar:
    if st.button("Load New Vendor Customers"):
        import_new_vendor_customers(VENDOR_CUSTOMERS_CFG, ctx.db_conn)
        st.session_state.vendor_customer_sibling_candidates_df_version += 1
        st.rerun()
            
review_queue, history, entities = st.tabs(["Review Queue", "History", "Entities"])

with review_queue:

    with st.expander("Add New Parent"):
        with st.form("add new parent"):
            new_parent = st.text_input("enter new parent")
            submitted = st.form_submit_button(label="submit")
            if submitted:
                add_parent(ctx.db_conn, new_parent)
    
    with st.expander("View Potential Siblings"):

        if "vendor_customer_sibling_candidates_df_version" not in st.session_state:
            st.session_state.vendor_customer_sibling_candidates_df_version = 0

        if "vendor_customer_sibling_candidates_df" not in st.session_state:
            _vcsc = get_data(ctx.db_conn, "vendor_customer_sibling_candidates_ui")
            _vcsc = prep_vendor_customer_sibling_candidates_df(_vcsc)
            st.session_state.vendor_customer_sibling_candidates_df = _vcsc

        if "selected_sibling_candidate_ids_df" not in st.session_state:
            st.session_state.selected_sibling_candidate_ids_df = pd.DataFrame(
                columns=['left_vendor_customer_id','right_vendor_customer_id']
            )

        decisions_df = st.data_editor(
            st.session_state.vendor_customer_sibling_candidates_df,
            column_config=VENDOR_CUSTOMER_SIBLING_CANDIDATES_CFG,
            key=f"vendor_customer_sibling_candidates_df_{st.session_state.vendor_customer_sibling_candidates_df_version}",
            hide_index=True,
        )

        # if st.button("submit relationships"):
        #     siblings_ids_to_process_df = (
        #         decisions_df
        #         [decisions_df['decision'].notna()]
        #         [['left_vendor_customer_id', 'right_vendor_customer_id']]
        #     )

        #     resolve_accepted_sibling_pair(
        #         ctx.db_conn, 
        #         sibling_ids_df=siblings_ids_to_process_df
        #     )


    # with st.expander("View Vendor Customer To Existing Parent Suggestions"):

    #     accepted, rejected = st.columns(2)
        
    #     if "vendor_customer_to_parent_suggestion_version" not in st.session_state:
    #         st.session_state.vendor_customer_to_parent_suggestion_version = 0

    #     if "vendor_customer_to_parent_suggestion_df" not in st.session_state:
    #         st.session_state.vendor_customer_to_parent_suggestion_df = get_data(
    #             ctx.db_conn, relation_name="vendor_customer_to_parent_suggestions"
    #         )

    #     if "selected_vendor_customer_to_parent_df" not in st.session_state:
    #         st.session_state.selected_vendor_customer_to_parent_df = pd.DataFrame(
    #             columns=[VendorCustomerToParentMap.VENDOR_CUSTOMER_ID, VendorCustomerToParentMap.PARENT_ACCOUNT_ID]
    #         )

    #     vendor_customer_to_parent_row_selection = st.dataframe(
    #         st.session_state.vendor_customer_to_parent_suggestion_df,
    #         selection_mode="multi-row",
    #         on_select="rerun",
    #         key=f"vendor_customer_to_parent_suggestion_df_{st.session_state.vendor_customer_to_parent_suggestion_version}"
    #     )

    #     if vendor_customer_to_parent_row_selection.selection.rows != []:
    #         selected_rows = vendor_customer_to_parent_row_selection.selection.rows
    #         st.session_state.selected_vendor_customer_to_parent_df = (
    #             st.session_state.vendor_customer_to_parent_suggestion_df
    #             .iloc[selected_rows]
    #             [[VendorCustomerToParentMap.VENDOR_CUSTOMER_ID, VendorCustomerToParentMap.PARENT_ACCOUNT_ID]]
    #         )

    #     with accepted:
    #         if st.button("accept"):
    #             bulk_insert_target_table(
    #                 ctx.db_conn,
    #                 target_table=VendorCustomerToParentMap.TABLE,
    #                 staging_table_df=st.session_state.selected_vendor_customer_to_parent_df
    #             )
    #             del st.session_state.selected_vendor_customer_to_parent_df
    #             del st.session_state.vendor_customer_to_parent_suggestion_df
    #             increment_table_versions()
    #             st.rerun()
            
    #     with rejected:
    #         if st.button("reject"):
    #             bulk_insert_target_table(
    #                 ctx.db_conn,
    #                 target_table=RejectedVendorCustomerToParentMap.TABLE,
    #                 staging_table_df=st.session_state.selected_vendor_customer_to_parent_df
    #             )
    #             del st.session_state.selected_vendor_customer_to_parent_df
    #             del st.session_state.vendor_customer_to_parent_suggestion_df
    #             increment_table_versions()
    #             st.rerun()

    

with history:
    st.write("history here")

with entities:
    st.dataframe(get_data(ctx.db_conn, "resolved_customers"), key="resolved_customers_df")
    st.dataframe(get_data(ctx.db_conn, "vendor_customers"), key="vendor_customers_df")


