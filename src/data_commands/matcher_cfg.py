from dataclasses import dataclass
from data_commands.database_get import get_data
import duckdb
import pandas as pd

"""
used to compare tbl_1 to tbl_2
filter_columns limits the candidate pool by enforcing value matches between the listed columns
structure: {col_in_left : respective_col_in_right,}
"""

@dataclass
class TargetTableCfg:
    name: str
    upload_columns: list[str]
    join_columns: list[str]
    score_cutoff: int = 80

@dataclass
class TargetTable:
    name: str
    upload_columns: list[str]
    current_df: pd.DataFrame
    join_columns: list[str] # the columns to join current_df to, to exclude existing data
    batch_id: int
    score_cutoff: int = 80

@dataclass
class CandidateCfg:
    left_relation_name: str
    left_column_name: str
    right_relation_name: str
    right_column_name: str
    column_subset: dict[str, str]

@dataclass
class CandidatePairs:
    left_df: pd.DataFrame
    left_column_name: str
    right_df: pd.DataFrame
    right_column_name: str
    column_subset: dict[str, str]
    match_type_id: str

@dataclass
class CandidateUploadCfg:
    candidates_cfg: CandidateCfg
    target_table_cfg: TargetTableCfg

def get_next_batch_id(conn: duckdb.DuckDBPyConnection) -> int:
    batch_id = conn.sql(f"SELECT MAX(batch_id) FROM batches").fetchone()[0]
    if batch_id is None: 
        batch_id = 1 
    else: 
        batch_id += 1
    return batch_id

def load_candidate_pair(conn: duckdb.DuckDBPyConnection, candidate_cfg: CandidateCfg):
    """
    loads data from candidate_cfg, quering the connection to return current left and right df.
    """
    return CandidatePairs(
        left_df=get_data(conn, candidate_cfg.left_relation_name),
        left_column_name=candidate_cfg.left_column_name,
        right_df=get_data(conn, candidate_cfg.right_relation_name),
        right_column_name=candidate_cfg.right_column_name,
        column_subset=candidate_cfg.column_subset,
        match_type_id=f"{candidate_cfg.left_relation_name}_to_{candidate_cfg.right_relation_name}"
    )

def load_target_table(conn: duckdb.DuckDBPyConnection, target_tbl_cfg: TargetTableCfg) -> TargetTable:
    """
    loads data from target_table_config, quering the connection to return current df.
    all other attributes are passed through
    """
    return TargetTable(
        name=target_tbl_cfg.name,
        upload_columns=target_tbl_cfg.upload_columns,
        current_df=get_data(conn, target_tbl_cfg.name),
        join_columns=target_tbl_cfg.join_columns,
        batch_id=get_next_batch_id(conn),
        score_cutoff=target_tbl_cfg.score_cutoff
    )