import duckdb
import streamlit as st
from dataclasses import dataclass
import duckdb


# ========= ADD RELATIONSHIP ==============

@dataclass
class RelationshipFormCfg:
    option_display_name: str
    target_table: str
    parent_display_name: str
    parent_api_name: str
    child_display_name: str
    child_api_name: str

def parse_relationship_results(
        relationship_cfg: RelationshipFormCfg, 
        *,
        parent_id: int,
        child_id: int,
        conn: duckdb.DuckDBPyConnection):

    conn.execute(
        f"""
        INSERT INTO 
        {relationship_cfg.target_table} 
        ({relationship_cfg.parent_api_name}, {relationship_cfg.child_api_name}) 
        VALUES (?, ?)
        """,  
        [parent_id, child_id]
    )

def render_relationship_forms(
        relationship_map: dict[str, RelationshipFormCfg],
        conn: duckdb.DuckDBPyConnection
    ) -> dict[str, int] | None:

    options = [opt for opt in relationship_map.keys()]

    selection = st.selectbox(label="Select Relationship to Add", options=options)

    selection_cfg = relationship_map.get(selection)

    with st.form(key=f"{selection}"):
        st.write(f"Add Relationship")
        parent_id = st.text_input(selection_cfg.parent_display_name)
        child_id = st.text_input(selection_cfg.child_display_name)
        submitted = st.form_submit_button()
        if submitted:
            parse_relationship_results(
                selection_cfg, 
                parent_id=parent_id, 
                child_id=child_id, 
                conn=conn
            )


