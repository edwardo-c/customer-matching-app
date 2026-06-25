"""primary runner for initiating app"""
import duckdb
from pathlib import Path
import os
from config import APP_PATHS

def construct_sql_paths(
        base_path: Path, 
        files: list[str],
        dir: str
    ) -> list[Path]:
    """
    construct base_path/dir/file01, file02 ... paths
    raises on invalid path
    """
    files = []
    for f in files:
        p = Path(base_path / dir / f)
        if not p.exists():
            raise FileNotFoundError(f"path: {p} does not exist")
        else:
            files.append[p]
    return files

def initialize_app_schema():
    if APP_PATHS.db_path.exists(): os.remove(str(APP_PATHS.db_path))

    conn = duckdb.connect(APP_PATHS.db_path)

    tables_paths = construct_sql_paths(
        base_path=APP_PATHS.db_path, 
        files=APP_PATHS.sql_table_files, 
        dir='tables'
    )

    view_paths = construct_sql_paths(
        base_path=APP_PATHS.db_path, 
        files=APP_PATHS.sql_views_files, 
        dir='views'
    )
    
    sql_paths = tables_paths + view_paths

    for sp in sql_paths:
        conn.execute(sp.read_text(encoding="utf-8"))

if __name__ == "__main__":
    initialize_app_schema()




