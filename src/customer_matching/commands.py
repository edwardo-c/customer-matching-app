import duckdb
import pandas as pd
from customer_matching.normalizer import normalize_str
from typing import Callable
from dataclasses import dataclass


def get_data(conn: duckdb.DuckDBPyConnection, relation: str):
    return conn.table(relation).df()

def get_vw(conn: duckdb.DuckDBPyConnection, view_name: str) -> pd.DataFrame:
    return conn.execute(f"SELECT * FROM {view_name}").df()

def add_parent(conn: duckdb.DuckDBPyConnection, name: str):
    norm_name = normalize_str(name)
    conn.execute(
        "INSERT INTO parent_accounts (parent_account_name, normalized_parent_name) VALUES (?, ?)", 
        [name, norm_name]
    )

# ============ Adding relationships ===================

@dataclass
class Relationship:
    target_table: str
    parent_display_name: str
    child_display_name: str

RELATION_REGISTRY = {
    "Vendor Customer To Parent Account": Relationship(
        target_table = "vendor_customer_to_parent_account_map",
        parent_display_name="Parent Account",
        child_display_name="Vendor Customer"
    ),
    "ERP Account To Parent Account": Relationship(
        target_table="erp_account_to_parent_account_map", 
        parent_display_name="Parent Account", 
        child_display_name="Vendor Customer"
    ),
    "Vendor Customer To ERP Account": Relationship(
        target_table="vendor_cust_to_erp_account_map", 
        parent_display_name="Parent Account", 
        child_display_name="Vendor Customer"
    ),
}

def parse_relationship_results(
        target_table: str, 
        results_map: dict[str, int],
        conn: duckdb.DuckDBPyConnection):

    conn.execute(
        f"""
        INSERT INTO {target_table} VALUES (?, ?)
        """, 
        [results_map["child_id"], results_map["parent_id"]]
    )

