import streamlit as st
import duckdb
from dataclasses import dataclass
import pandas as pd
from typing import Callable

def get_data(conn: duckdb.DuckDBPyConnection, relation: str):
    return conn.table(relation).df()

def get_vw(conn: duckdb.DuckDBPyConnection, view_name: str) -> pd.DataFrame:
    return conn.execute(f"SELECT * FROM {view_name}").df()

READER_FUNC_REGISTRY = {'table': get_data, 'view': get_vw}

@dataclass
class CheckboxControlledTabCfg:
    checkbox_caption: str
    data_caption: str
    relation_name: str
    relation_type: str
    reader_func: None | Callable = None

    def __post_init__(self):
        if self.relation_type not in (READER_FUNC_REGISTRY.keys()):
            raise KeyError(f"relation type must equal 'table' or 'view'")
        self.reader_func = READER_FUNC_REGISTRY[self.relation_type]

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
                table_option.reader_func(
                    conn, 
                    table_option.relation_name
                ), 
                hide_index=True, 
                width="stretch"
            )