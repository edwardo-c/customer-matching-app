from rapidfuzz import fuzz
import pandas as pd
from data_commands.matcher_cfg import CandidatePairs, TargetTable
import math

class MatchingPipeline:
    def __init__(
            self,
            candidates: CandidatePairs,
            target: TargetTable
        ):

        self.candidates = candidates
        self.target = target
        self.candidates_df: pd.DataFrame | None = None
        self._new_candidates_df: pd.DataFrame | None = None

    @property
    def new_candidates_df(self):
        if self._new_candidates_df is None:
            self.run()
        return self._new_candidates_df

    @staticmethod
    def drop_existing_candidates(
            left_df: pd.DataFrame, 
            right_df: pd.DataFrame,
            on_columns: list[str]
        ) -> pd.DataFrame:
        merged = left_df.merge(right_df[on_columns], indicator=True, how="left", on=on_columns)
        except_df = merged.query("_merge == 'left_only'")
        return except_df.drop(columns='_merge')

    @staticmethod
    def keep_upload_df_columns(
            upload_df: pd.DataFrame, 
            keep_cols: list[str]
        ) -> pd.DataFrame:

        existing_columns = (upload_df.columns)
        for c in keep_cols:
            if c not in existing_columns:
                upload_df[c] = "pending"
        return upload_df[keep_cols]

    def build_upload_df(self):
        _df = self.candidates_df.copy().query(f"score > {self.target.score_cutoff}")
        _df = self.keep_upload_df_columns(_df, self.target.upload_columns)
        _df = self.drop_existing_candidates(
            _df, 
            self.target.current_df, 
            self.target.join_columns
        )
        _df = self.add_static_column(_df, "batch_id", self.target.batch_id)

        self._new_candidates_df = _df
        return self._new_candidates_df

    @staticmethod
    def build_query_statement(cols: list[str], filter_values: tuple[str]) -> str:
        exprs = []
        for col_name, filter_value in zip(cols, filter_values):
            exprs.append(f"{col_name} == '{filter_value}'") 
        return ' and '.join(exprs)

    @staticmethod
    def get_filter_criteria(df: pd.DataFrame) -> list[tuple]:
        """
        converts a dataframe into a list of tuples for each unique combination
        """
        return df.drop_duplicates().to_records(index=False).tolist()

    @staticmethod
    def add_static_column(df:pd.DataFrame, name: str, val: str) -> pd.DataFrame:
        df[name] = val
        return df

    @staticmethod
    def fill_match_score(
            left_df: pd.DataFrame, 
            left_candidate_col_name: str,
            right_df: pd.DataFrame,
            right_candidate_col_name: str
        ) -> pd.DataFrame:
        """
        given two data frames, compare left against right. create 'score' and fill 
        with rapidfuzz.fuzz.set_token_ratio result
        """
        _left = left_df.copy()
        
        _df: pd.DataFrame = _left.merge(right_df, how='cross')
        
        _df['score'] = _df.apply(
            lambda row: 
                math.trunc(fuzz.token_set_ratio(
                    row[left_candidate_col_name], 
                    row[right_candidate_col_name]
                ) * 100) / 100,
        axis=1)

        return _df

    def build_candidates_df(self):

        left_cols = [c for c in self.candidates.column_subset.keys()]
        right_cols = [c for c in self.candidates.column_subset.values()]

        filters = self.get_filter_criteria(self.candidates.left_df[left_cols])

        frames = []

        for f in filters:
            left_df = self.candidates.left_df.query(self.build_query_statement(cols=left_cols, filter_values=f))
            right_df= self.candidates.right_df.query(self.build_query_statement(cols=right_cols, filter_values=f))
            
            if not right_df.empty:
                frames.append(self.fill_match_score(
                    left_df, self.candidates.left_column_name,
                    right_df, self.candidates.right_column_name
                    )
                )
        
        if len(frames) > 0:
            candidates_df = self.add_static_column(
                pd.concat(frames), 
                "match_type_id", 
                self.candidates.match_type_id
            )
        else:
            candidates_df = pd.DataFrame()

        self.candidates_df = candidates_df

        return candidates_df

    def run(self):
        self.build_candidates_df()
        self.build_upload_df()