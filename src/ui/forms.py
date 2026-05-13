import streamlit as st
from customer_matching.commands import add_parent, Relationship


def render_add_parent_form(conn):
    with st.form("add_parent_form"):
        st.write("Add Parent Account")
        parent_name = st.text_input("Name")
        submitted = st.form_submit_button("Add Parent")

        if submitted:
            add_parent(conn, parent_name)
            st.success(f"{parent_name} added")
            st.rerun()

def render_relationship_form(relationship_cfg: Relationship) -> dict[str, int] | None:
        with st.form(f"Relationship form"):
            st.write(f"Add Relationship")
            parent_id = st.text_input(relationship_cfg.parent_display_name + " ID")
            child_id = st.text_input(relationship_cfg.child_display_name + " ID")
            submitted = st.form_submit_button()
            if submitted:
                st.markdown(":green-badge[Sucess]")
                return {'parent_id': parent_id, 'child_id': child_id}