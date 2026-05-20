from rapidfuzz import fuzz
import pandas as pd

class MatchingPipeline:
    def __init__(
            self,
            left_df: pd.DataFrame,
            left_column_name: str,
            right_df: pd.DataFrame,
            right_column_name: str,
            column_subset: dict[str, str],
            match_type_id: str,
            score_cutoff: int
        ):
        self.left_df = left_df
        self.left_column_name  = left_column_name

        self.right_df = right_df
        self.right_column_name = right_column_name
        
        self.matched_df: pd.DataFrame | None = None # output

        self.left_columns = [c for c in column_subset.keys()]
        self.right_columns = [c for c in column_subset.values()]

        self.left_filter_criteria: list[tuple] | None = None  
        
        self.score_cutoff = score_cutoff

        self.match_type_id = match_type_id

    @staticmethod
    def build_query_statement(cols: list[str], filter_values: tuple[str]) -> str:
        exprs = []
        for col_name, filter_value in zip(cols, filter_values):
            exprs.append(f"{col_name} == '{filter_value}'") 
        return ' and '.join(exprs)

    def _fuzzy_match(self, row):
        return fuzz.token_set_ratio(
            row[self.left_column_name], 
            row[self.right_column_name]
        ) 

    def fill_match_score(self, left_df: pd.DataFrame, right_df: pd.DataFrame) -> pd.DataFrame:
        """
        given two data frames, compare left against right. create 'score' and fill 
        with rapidfuzz.fuzz.set_token_ratio result
        """
        _left = left_df.copy()
        _df = _left.merge(right_df, how='cross')
        _df['score'] = _df.apply(self._fuzzy_match, axis=1)
        return _df.query(f"score > {self.score_cutoff}")

    def get_candidates(self) -> pd.DataFrame:
        """
        compare left against right where criteria is true for both comparison groups
        """
        frames = []

        for criteria in self.left_filter_criteria:

            left_query_statement = self.build_query_statement(
                cols=self.left_columns, 
                filter_values=criteria
            )
            left_df = self.left_df.query(left_query_statement)

            right_query_statement = self.build_query_statement(
                cols=self.right_columns, 
                filter_values=criteria
            )

            right_df = self.right_df.query(right_query_statement)

            if right_df.empty:
                continue
            else:
                candidate_matches = self.fill_match_score(left_df, right_df)            
                frames.append(candidate_matches)
        
            if len(frames) > 0:
                matched_df = pd.concat(frames)
                matched_df['match_type_id'] = self.match_type_id
                self.matched_df = matched_df
            else:
                self.matched_df = pd.DataFrame()

        return self.matched_df

    def get_left_filter_criteria(self) -> tuple:
        if self.left_filter_criteria == None:
            filter_criteria_df = self.left_df[self.left_columns]
            filter_criteria_df = filter_criteria_df.drop_duplicates()
            self.left_filter_criteria = filter_criteria_df.to_records(index=False).tolist()
        else:
            return self.left_filter_criteria

    def run(self):
        self.get_left_filter_criteria()
        self.get_candidates()