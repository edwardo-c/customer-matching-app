"""
compare 
vc to vc
vc to erp
erp to erp
vc to parent
erp to parent
"""

"""dispatches match groups to be processed through fuzzy matching"""

"""
data is loaded, normalized, then matched, then candidates are loaded
"""

import duckdb
from pathlib import Path
from dataclasses import dataclass
from src.load_helpers import AppPaths


# @dataclass(frozen=True)
# class Context:
#     db_conn: duckdb.DuckDBPyConnection

# def get_context(app_paths: AppPaths) -> Context:
#     return Context(
#         db_conn=duckdb.connect(app_paths.db_path)
#     )

# def execute_sql(conn: duckdb.DuckDBPyConnection, sql_path: Path) -> None:
#     conn.execute(sql_path.read_text(encoding="utf-8"))



# # ================================================================

# 

# @dataclass
# class AppDataFrames:
#     vendor_customers: pd.DataFrame
#     erp_accounts: pd.DataFrame

# def get_dataframes(conn: duckdb.DuckDBPyConnection) -> AppDataFrames:
#     return AppDataFrames(
#         vendor_customers=conn.execute("SELECT * FROM vendor_customers").df(),
#         erp_customers=conn.execute("SELECT * FROM erp_accounts").df()
#     )




# ================================================================


# def refresh_candidates_table(conn: duckdb.DuckDBPyConnection) -> None:
#     # get data


#     # run through matcher object
    
#     # populate table
#     ...

# def load_app(app_paths: AppPaths) -> Context:
#     """
#     refreshes data sources, return app context 
#     """
    
#     ctx = get_context(app_paths)

#     # TODO: load from POS file

#     # TODO: load from erp
    
#     refresh_candidates_table()
    

#     return ctx