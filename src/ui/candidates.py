import streamlit as st
import duckdb
from dataclasses import dataclass
from data_commands.database_get import get_data
import pandas as pd
from enum import Enum



# @dataclass
# class SelectedSiblings:
#     ...

# def get_potential_parents_df(
#         candidate: SelectedCandidate,
#         conn:duckdb.DuckDBPyConnection
#     ) -> pd.DataFrame: 
#     return conn.execute(
#         """
#         SELECT * FROM parent_accounts 
#         WHERE parent_name_first3_token = ?
#         """, 
#         [candidate.first3_token]
#     ).df()


class Workflow(Enum):
    caption = "Select Workflow"
    vendor_siblings = "Vendor Customer Siblings"
    vendor_to_erp = "Vendor Customers to ERP"


@dataclass
class SelectedCandidate:
    first3_token: int
    state: str
    zip: str
    count_of_potential_siblings: int
    count_of_parents_with_same_token: int

def get_vendor_customer_siblings_df(
        *, 
        candidate: SelectedCandidate,
        conn:duckdb.DuckDBPyConnection
    ) -> pd.DataFrame:
    return conn.execute(
        """
        SELECT * 
        FROM vendor_customers 
        WHERE vendor_customer_first3_token = ?
        AND vendor_customer_billing_state = ?
        AND vendor_customer_billing_zip = ?
        """, [candidate.first3_token, candidate.state, candidate.zip]
    ).df()


def get_vendor_sibling_selection(
        *, 
        candidate: SelectedCandidate,
        conn:duckdb.DuckDBPyConnection
    ) -> str:
    ...

def render_vendor_sibling_workflow(conn:duckdb.DuckDBPyConnection):

    df = get_data(conn, "suggested_vendor_customer_parents_vw")
    
    st.write("Select to view potential siblings")
    
    selected = st.dataframe(
        df, 
        hide_index=True, 
        width="stretch",
        on_select='rerun',
        selection_mode="single-row"
    )
    
    if selected["selection"]["rows"] != []:
        selected_candidate = SelectedCandidate(
            **df.iloc[selected["selection"]["rows"][0]].to_dict()
        )

        # get selection
        get_vendor_customer_siblings_df(candidate=selected_candidate, conn=conn)

        # process selection

        breakpoint()

def render_vendor_cust_to_erp_workflow(conn:duckdb.DuckDBPyConnection):
    ...

def render_candidate_tab(conn:duckdb.DuckDBPyConnection):
    
    selected_workflow = st.selectbox(
        Workflow.caption.value, 
        [Workflow.vendor_siblings.value, Workflow.vendor_to_erp.value]
    )
    
    if selected_workflow == Workflow.vendor_siblings.value: 
        render_vendor_sibling_workflow(conn)
    
    if selected_workflow == Workflow.vendor_to_erp.value: 
        render_vendor_cust_to_erp_workflow(conn)
    
    # ============================== TO BE ABSTRACTED =============================

    # if st.checkbox("view potential vendor customer parents"):
            
    #         if selected_candidate.count_of_parents_with_same_token > 0:
    #             st.write("view candidate parents")
    #             get_potential_parents_df(selected_candidate, conn)


    #             st.write("view vendor customer siblings")
    #             st.dataframe(
    #                 get_vendor_customer_siblings_df(candidate=selected_candidate, conn=conn), 
    #                 selection_mode="multi-row",
    #                 on_select="rerun"
    #             )
            
    #         if selected_candidate.count_of_potential_siblings > 0:
    #             st.write("view vendor customer siblings")
    #             confirmed_siblings = st.dataframe(
    #                 get_vendor_customer_siblings_df(candidate=selected_candidate, conn=conn), 
    #                 selection_mode="multi-row",
    #                 on_select="rerun"
    #             )

    #             selected_siblings = confirmed_siblings["selection"]["rows"]

    #             if selected_siblings != []:

    #                 with st.form("Add siblings"):
    #                     options = ["New Parent", "Existing Parent"]
    #                     add_to = st.selectbox(
    #                         label="Add selected siblings to siblings to...", 
    #                         options=options
    #                     )

    #                     if add_to == options[0]:
    #                         st.write("enter new parent name")
                        
    #                     if add_to == options[1]:
    #                         st.write("enter existing parent id")

    #                     st.form_submit_button(label="submit")
                
    #             breakpoint()
