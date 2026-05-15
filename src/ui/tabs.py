import streamlit as st
import duckdb
from dataclasses import dataclass
import pandas as pd

def get_data(conn: duckdb.DuckDBPyConnection, relation: str):
    return conn.table(relation).df()

def get_vw(conn: duckdb.DuckDBPyConnection, view_name: str) -> pd.DataFrame:
    return conn.execute(f"SELECT * FROM {view_name}").df()

READER_FUNC_REGISTRY = {'table': get_data, 'view': get_vw}

@dataclass
class CheckboxControlledTabCfg:
    checkbox_caption: str
    table_caption: str
    table_name: str
    reader_key: str

def render_checkbox_controlled_dataframes(
        cfg: list[CheckboxControlledTabCfg], 
        conn:duckdb.DuckDBPyConnection
    ) -> None:
    cols = [col for col in st.columns(len(cfg))]
    for col, table_option in zip(cols, cfg):
        with col:
            result = st.checkbox(table_option.checkbox_caption)
        if result:
            st.caption(table_option.table_caption)
            st.dataframe(
                READER_FUNC_REGISTRY[table_option.reader_key](
                    conn, 
                    table_option.table_name
                ), 
                hide_index=True, 
                width="stretch"
            )