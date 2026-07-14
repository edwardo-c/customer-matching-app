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
        INSERT INTO parent_accounts (
          parent_account_name, 
          normalized_parent_name, 
          first3_token
        ) 
        VALUES (?, ?, ?)
        """, 
        [name, norm_name, token]
    )

def insert_into_sibling_relationship_table(
        conn: duckdb.DuckDBPyConnection, 
        *,
        target_table: str,
        staging_table_df: pd.DataFrame
    ):
    _df = staging_table_df.copy()
    
    staging_table_df["created_datetime"] = pd.Timestamp.now()
    
    bulk_insert_target_table(
        conn, 
        target_table=target_table, 
        staging_table_df=staging_table_df
    )

def bulk_insert_target_table(
        conn: duckdb.DuckDBPyConnection, 
        *,
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
        
        