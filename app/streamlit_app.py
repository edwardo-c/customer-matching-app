import streamlit as st

from config import (APP_PATHS)
from data_commands.context import get_app_context
from data_commands.commands import add_parent, get_data, bulk_insert_relationships

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

# ===== Tabs ======
(
    vendor_to_parent_suggestions, 
    vendor_to_erp_suggestions, 
    vendor_sibling_suggestions,
    history, 
    entities
) = st.tabs([
    "vendor_to_parent_suggestions",
    "vendor_to_erp_suggestions", 
    "vendor_siblings_suggestions",
    "History", 
    "Entities"
])

with vendor_to_parent_suggestions: 
    
    vendor_to_parent_selected: bool = False

    vendor_to_parent_candidates_df = get_data(
        ctx.db_conn, 
        "vendor_to_parent_candidates"
    )

    if vendor_to_parent_candidates_df.empty:
        st.write("Congratulations! No vendor to parent candidate suggestions available")
    else:
        if "vendor_to_parent_table_version" not in st.session_state:
            st.session_state["vendor_to_parent_table_version"] = 0

        selection = st.dataframe(
            vendor_to_parent_candidates_df,
            on_select="rerun",
            selection_mode="multi-row",
            key=f"vendor_to_parent_candidates_df_{st.session_state['vendor_to_parent_table_version']}"
        )

        selected_indices = selection.selection.rows

        if selected_indices:
            st.session_state["selected_vendor_to_parent_df"] = (
                vendor_to_parent_candidates_df
                .iloc[selected_indices]
                [["vendor_customer_id", "parent_account_id"]]
            )
            
            vendor_to_parent_selected = True

        if st.button("accept selected"):
            
            if vendor_to_parent_selected: 
                
                bulk_insert_relationships(
                    ctx.db_conn,
                    target_table="vendor_customer_to_parent_account_map", 
                    parent_child_id_df=st.session_state["selected_vendor_to_parent_df"]
                )

                del st.session_state["selected_vendor_to_parent_df"] 
                st.session_state["vendor_to_parent_table_version"] += 1
                st.rerun()


        if st.button("reject selected"): 
            
            if vendor_to_parent_selected:

                bulk_insert_relationships(
                    ctx.db_conn,
                    target_table="mismatch_vendor_customer_to_parent_account_map", 
                    parent_child_id_df=st.session_state["selected_vendor_to_parent_df"]
                )

                del st.session_state["selected_vendor_to_parent_df"]
                st.session_state["vendor_to_parent_table_version"] += 1          
                st.rerun()

with vendor_to_erp_suggestions:

    vendor_to_erp_candidates_df = get_data(
        ctx.db_conn, 
        "vendor_to_erp_candidates"
    ).reset_index(drop=True)

    if vendor_to_erp_candidates_df.empty:
    
        st.write("Congratulations! No vendor to erp candidate at this time, check back later")
    
    else:
        
        vendor_to_erp_selected: bool = False

        if "vendor_to_erp_table_version" not in st.session_state:
            st.session_state["vendor_to_erp_table_version"] = 0

        selection = st.dataframe(
            vendor_to_erp_candidates_df,
            on_select="rerun",
            selection_mode="multi-row",
            key=f"vendor_to_erp_candidates_table_{st.session_state['vendor_to_erp_table_version']}"
        )

        selected_indices = selection.selection.rows

        if selected_indices:
            st.session_state["selected_vendor_to_erp_ids"] = (
                vendor_to_erp_candidates_df
                .iloc[selected_indices]
                [["vendor_customer_id", "erp_account_id"]]
            )

            vendor_to_erp_selected = True
            

        if st.button("Accept Selected"):
            if vendor_to_erp_selected: 
                
                bulk_insert_relationships(
                    ctx.db_conn,
                    target_table="vendor_customer_to_erp_account_map", 
                    parent_child_id_df=st.session_state["selected_vendor_to_erp_ids"]
                )

                st.session_state["vendor_to_erp_table_version"] += 1
                del st.session_state.selected_vendor_to_erp_ids
                st.rerun()
            
        if st.button("Reject Selected"):
            if vendor_to_erp_selected: 
                
                bulk_insert_relationships(
                    ctx.db_conn,
                    target_table="mismatch_vendor_customer_to_erp_account_map", 
                    parent_child_id_df=st.session_state["selected_vendor_to_erp_ids"]
                )
                
                st.session_state["vendor_to_erp_table_version"] += 1
                del st.session_state.selected_vendor_to_erp_ids
                st.rerun()

with vendor_sibling_suggestions:
    st.write("work in progress, yo")

with history:
    st.write("history here")

with entities:
    st.dataframe(get_data(ctx.db_conn, "parent_accounts"), key="parent_accounts_df")
    st.dataframe(get_data(ctx.db_conn, "vendor_customers"), key="vendor_customers_df")
    st.dataframe(get_data(ctx.db_conn, "erp_accounts"), key="erp_accounts_df")