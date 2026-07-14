import streamlit as st
import duckdb
from data_commands.commands import get_data, bulk_insert_target_table
import pandas as pd
from column_configs import VENDOR_CUSTOMER_SIBLING_CANDIDATES_CFG
from data_commands.schema_manager import (
    add_decision_col, 
    extract_all_decisions,
    extract_accepted_siblings_df,
    extract_rejected_siblings_df,
    SiblingTableConfig,
    get_empty_sibling_decision_table
)

class SiblingCandidateState:
    VERSION = "vendor_customer_sibling_candidates_df_version"
    DF = "vendor_customer_sibling_candidates_df_"
    VIEW = "vendor_customer_sibling_candidates_ui"
    ACCEPTED_DF = "sibling_candidate_ids_df"
    REJECTED_DF = "rejected_sibling_Candidate_ids_df"

def render_sibling_candidates(conn: duckdb.DuckDBPyConnection):
    
    if SiblingCandidateState.VERSION not in st.session_state:
        st.session_state[SiblingCandidateState.VERSION] = 0

    if SiblingCandidateState.DF not in st.session_state:
        _ui_df = get_data(conn, SiblingCandidateState.VIEW)
        _ui_df = add_decision_col(_ui_df)
        _ui_df.sort_values(by=["priority", "left_raw_vendor_customer_name"], inplace=True)
        st.session_state[SiblingCandidateState.DF] = _ui_df

    if SiblingCandidateState.ACCEPTED_DF not in st.session_state:
        st.session_state[SiblingCandidateState.ACCEPTED_DF] = get_empty_sibling_decision_table()

    if SiblingCandidateState.REJECTED_DF not in st.session_state:
        st.session_state[SiblingCandidateState.REJECTED_DF] = get_empty_sibling_decision_table()

    if st.button("submit"):
        if not st.session_state[SiblingCandidateState.ACCEPTED_DF].empty:
            bulk_insert_target_table(
                conn, 
                target_table=SiblingTableConfig.ACCEPTED, 
                staging_table_df=st.session_state[SiblingCandidateState.ACCEPTED_DF]
            )
            del st.session_state[SiblingCandidateState.ACCEPTED_DF]

        if not st.session_state[SiblingCandidateState.REJECTED_DF].empty:
            bulk_insert_target_table(
                conn, 
                target_table=SiblingTableConfig.REJECTED,
                staging_table_df=st.session_state[SiblingCandidateState.REJECTED_DF]
            )
            del st.session_state[SiblingCandidateState.REJECTED_DF]
        
        st.session_state[SiblingCandidateState.VERSION] += 1

    decisions_df: pd.DataFrame = st.data_editor(
        st.session_state[SiblingCandidateState.DF],
        column_config=VENDOR_CUSTOMER_SIBLING_CANDIDATES_CFG,
        key=f"{SiblingCandidateState.DF}{st.session_state[SiblingCandidateState.VERSION]}",
        hide_index=True,
    )

    if extract_all_decisions(decisions_df).empty:
        st.warning("Update Decision column")
    else:
        st.session_state[SiblingCandidateState.ACCEPTED_DF] = extract_accepted_siblings_df(
            decisions_df
        )

        st.session_state[SiblingCandidateState.REJECTED_DF] = extract_rejected_siblings_df(
            decisions_df
        )


