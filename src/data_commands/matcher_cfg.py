from dataclasses import dataclass
from data_commands.database_get import get_data
import duckdb
import pandas as pd

"""
column_subset = filter criteria - 
values must match between these columns in order to be considered
a candidate
"""

@dataclass
class MatcherCfg:
    left_relation_name: str
    left_column_name: str
    right_relation_name: str
    right_column_name: str
    column_subset: dict[str, str]
    score_cutoff: int = 80

@dataclass
class MatcherObj:
    left_df: pd.DataFrame
    left_column_name: str
    right_df: pd.DataFrame
    right_column_name: str
    column_subset: dict[str, str]
    match_type_id: str
    score_cutoff: int = 80

def load_matcher_objects(cfg: MatcherCfg, conn: duckdb.DuckDBPyConnection) -> MatcherObj:
    """
    accepts raw matcher configs and prepares them to a matcher object, 
    primary dataclass used in matcher.MatchingPipeline
    """
    return MatcherObj(
        left_df=get_data(conn, cfg.left_relation_name),
        left_column_name=cfg.left_column_name,
        right_df=get_data(conn, cfg.right_relation_name),
        right_column_name=cfg.right_column_name,
        column_subset=cfg.column_subset,
        match_type_id=f"{cfg.left_relation_name}_to_{cfg.right_relation_name}",
        score_cutoff=cfg.score_cutoff
    )