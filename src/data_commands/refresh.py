from data_commands.context import AppContext
from data_commands.matcher_cfg import MatcherCfg, load_matcher_objects, MatcherObj
from data_commands.matcher import MatchingPipeline

def refresh_app_data(
        ctx: AppContext,
        match_cfgs: list[MatcherCfg]
    ):

    for cfg in match_cfgs:
        matcher_obj: MatcherObj = load_matcher_objects(cfg, ctx.db_conn)

        mp = MatchingPipeline(
            left_df=matcher_obj.left_df,
            left_column_name=matcher_obj.left_column_name,
            right_df=matcher_obj.right_df,
            right_column_name=matcher_obj.right_column_name,
            column_subset=matcher_obj.column_subset,
            match_type_id=matcher_obj.match_type_id,
            score_cutoff=matcher_obj.score_cutoff
        )

        mp.run()

        """
        data filling properly for vc to erp
        """

        breakpoint()