import pandas as pd
import duckdb

def get_data(conn: duckdb.DuckDBPyConnection, relation_name: str) -> pd.DataFrame:
    return conn.execute(f"SELECT * FROM {relation_name}").df()