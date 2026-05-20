from dataclasses import dataclass
import duckdb
from pathlib import Path

@dataclass
class AppPaths:
    db_path: Path
    views_path: Path
    vendor_customers_path: Path

def get_app_context(app_paths: AppPaths):
    return AppContext(
        db_conn=duckdb.connect(app_paths.db_path)
    )

@dataclass
class AppContext:
    db_conn: duckdb.DuckDBPyConnection
