import duckdb
import pandas as pd
from data_commands.normalizer import normalize_str
from data_commands.normalizer import first3_token
from data_commands.db_schema import RelationshipMapTable

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

def drop_from_relationship_map(
        conn: duckdb.DuckDBPyConnection, 
        target_table_map: type[RelationshipMapTable],
        staging_table_df: pd.DataFrame
    ):
    """
    attempts to drop rows from target table that overlap with rows in staging_table 
    with rollback safe gaurd
    assumes matching schemas between tables
    """
    conn.register("staging_table", staging_table_df)

    conn.execute("BEGIN TRANSACTION")

    try:
        conn.execute(f"""
            DELETE FROM {target_table_map.TABLE} main
            USING staging_table s
            WHERE main.{target_table_map.SOURCE} = s.{target_table_map.SOURCE}
            AND main.{target_table_map.TARGET} = s.{target_table_map.TARGET};
        """)
        conn.execute("COMMIT")
    except Exception:
        conn.execute("ROLLBACK")
        raise
    finally:
        conn.unregister("staging_table")




def extract_parent_id(
        conn: duckdb.DuckDBPyConnection, 
        vendor_customer_id: int
    ) -> int | None:
    
    """
    get parent id for the provided vendor customer id
    returns None if vendor id is not mapped to a parent id
    """

    SQL_VENDOR_CUSTOMER_PARENT = """
    SELECT
    parent_account_id
    FROM vendor_customer_to_parent_account_map
    WHERE vendor_customer_id = ?
    """

    df = conn.execute(SQL_VENDOR_CUSTOMER_PARENT, [vendor_customer_id]).df()
    
    if df.empty:
        return None
    else:
        breakpoint()
        return df.at[0, 'parent_account_id'].item()


def resolve_accepted_sibling_pair(
        conn: duckdb.DuckDBPyConnection,
        *,
        sibling_ids_df: pd.DataFrame,
        left_id_col_name: str = "left_vendor_customer_id",
        right_id_col_name: str = "right_vendor_customer_id"
    ):
    
    zipped_ids = zip(
        sibling_ids_df[left_id_col_name], 
        sibling_ids_df[right_id_col_name]
    )
    
    missing_parents = []

    for pair in zipped_ids:
        
        left_parent_id = extract_parent_id(conn, pair[0])
        right_parent_id = extract_parent_id(conn, pair[1])
        
        