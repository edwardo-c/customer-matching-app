"""refresh views when new columns/views are added"""
import duckdb
from config import DB_PATH, VIEWS_PATH

def refresh_views():
    conn = duckdb.connect(DB_PATH)
    conn.execute(VIEWS_PATH.read_text(encoding="utf-8"))

if __name__ == "__main__":
    refresh_views()



