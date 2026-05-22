from data_commands.context import AppContext
from data_commands.matcher_cfg import CandidateUploadCfg, load_candidate_pair, load_target_table
from data_commands.matcher import MatchingPipeline
from dataclasses import dataclass
from datetime import datetime
import duckdb
import pandas as pd

@dataclass
class AppRefreshCfg:
    vendor_to_erp_candidates_cfg: CandidateUploadCfg

def insert_batch(conn: duckdb.DuckDBPyConnection, row: list) -> None:
    conn.execute("INSERT INTO batches BY POSITION (rows_added, target_table, upload_datetime) VALUES (?, ?, ?)", row)

def load_candidates_table(
        ctx: AppContext,
        cfg: CandidateUploadCfg
    ):

    mp = MatchingPipeline(
        candidates=load_candidate_pair(ctx.db_conn, cfg.candidates_cfg), 
        target=load_target_table(ctx.db_conn, cfg.target_table_cfg)
    )

    if not mp.new_candidates_df.empty:

        insert_batch(ctx.db_conn, [
            len(mp.new_candidates_df), 
            mp.target.name, 
            datetime.now()
        ])

        new_candidates_df = mp.new_candidates_df

        ctx.db_conn.register("new_candidates_df", new_candidates_df)

        ctx.db_conn.execute(
            f"""
            INSERT INTO {mp.target.name} BY NAME
            SELECT * FROM new_candidates_df
            """
        )

def load_suggested_parent_table():
    ...


def refresh_app(ctx: AppContext, cfg: AppRefreshCfg):
    load_candidates_table(ctx, cfg.vendor_to_erp_candidates_cfg)