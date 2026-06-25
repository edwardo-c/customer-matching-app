from dataclasses import dataclass
import duckdb
from pathlib import Path

@dataclass
class AppPaths:
    db_path: Path
    sql_base_path: Path
    sql_table_files: list[str]
    sql_views_files: list[str]

def get_app_context(app_paths: AppPaths):
    return AppContext(
        db_conn=duckdb.connect(app_paths.db_path)
    )

@dataclass
class AppContext:
    db_conn: duckdb.DuckDBPyConnection

