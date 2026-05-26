import streamlit as st
import duckdb
from dataclasses import dataclass
from typing import Callable
from data_commands.database_get import get_data

@dataclass
class CheckboxControlledTabCfg:
    checkbox_caption: str
    data_caption: str
    relation_name: str

def render_checkbox_controlled_dataframes(
        cfg: list[CheckboxControlledTabCfg], 
        conn:duckdb.DuckDBPyConnection
    ) -> None:
    cols = [col for col in st.columns(len(cfg))]
    for col, table_option in zip(cols, cfg):
        with col:
            result = st.checkbox(table_option.checkbox_caption)
        if result:
            st.caption(table_option.data_caption)
            st.dataframe(
                get_data(conn, table_option.relation_name), 
                hide_index=True, 
                width="stretch",
                on_select='rerun',
                selection_mode="single-row"
            )


