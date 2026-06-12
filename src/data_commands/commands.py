import duckdb
import pandas as pd
from data_commands.normalizer import normalize_str
from data_commands.normalizer import first3_token

def get_data(conn: duckdb.DuckDBPyConnection, relation_name: str) -> pd.DataFrame:
    return conn.execute(f"SELECT * FROM {relation_name}").df()

def add_parent(
        conn: duckdb.DuckDBPyConnection, 
        name: str
    ):
    norm_name = normalize_str(name)
    token = first3_token(norm_name)
    conn.execute(
        """
        INSERT INTO parent_accounts (parent_account_name, normalized_parent_name, first3_token) 
        VALUES (?, ?, ?)
        """, 
        [name, norm_name, token]
    )

def gen_vendor_ids_to_parent_id_df(
        parent_id: int, 
        children_ids: tuple[int, ...]
    ) -> pd.DataFrame:
    """
    generates a dataframe where parent_id is repeated per distinct child id
    schema matches vendor_customer_to_parent_account_map schema
    """
    return pd.DataFrame({
        "vendor_customer_id": [child for child in children_ids],
        "parent_account_id": [parent_id] * len(children_ids)
    })
    
def bulk_insert_target_table(
        conn: duckdb.DuckDBPyConnection, 
        target_table: str,
        staging_table_df: pd.DataFrame
    ):
    """
    attempts to insert into target table with rollback safe gaurd
    assumes matching schemas between tables
    """
    conn.register("staging_table", staging_table_df)

    conn.execute("BEGIN TRANSACTION")

    try:
        conn.execute(f"""
            INSERT INTO {target_table} BY NAME
            SELECT *
            FROM staging_table
        """)
        conn.execute("COMMIT")
    except Exception:
        conn.execute("ROLLBACK")
        raise
    finally:
        conn.unregister("staging_table")

def add_vendor_ids_to_existing_parent_id(
        conn: duckdb.DuckDBPyConnection, 
        vendor_customer_ids: tuple[int, ...],
        parent_id: int
    ):

    if parent_id is None:
        raise TypeError("parent_id must be type int, got None")

    _df = gen_vendor_ids_to_parent_id_df(
        parent_id=parent_id, 
        children_ids=vendor_customer_ids
    )
    
    bulk_insert_target_table(
        conn, 
        target_table="vendor_customer_to_parent_account_map",
        staging_table_df=_df
    )
    


