from pathlib import Path
from ui.tabs import CheckboxControlledTabCfg
from ui.sidebar import RelationshipFormCfg
from data_commands.refresh import AppRefreshCfg

from enum import Enum
from data_commands.context import AppPaths

from data_commands.matcher_cfg import (
    CandidateUploadCfg, 
    CandidateCfg, 
    TargetTableCfg
)


APP_PATHS = AppPaths(
    db_path = Path(r"C:\Users\eddiec11us\dev_apps\customer-matching-app\src\data\db.duckdb"),
    vendor_customers_path = Path(r"\\peernet\DavWWWRoot\Reporting\POS DATA\2025 - 2026 POS Pivot Incentive Comp.xlsx")
)

CANDIDATES_TAB_CFG = [
    CheckboxControlledTabCfg(
        checkbox_caption="Show Vendor Customer to ERP Account Candidates",
        data_caption="Vendor Customer to ERP Account Candidates",
        relation_name="vendor_customer_to_erp_account_candidate_vw"
    ),
]

class TableNames(Enum):
    parents = "parent_accounts"
    vendor_customers = "vendor_customers"
    erp_accounts = "erp_accounts"


APP_DATA_REFRESH_CFG = AppRefreshCfg(
    vendor_to_erp_candidates_cfg = CandidateUploadCfg(
        candidates_cfg=CandidateCfg(
            left_relation_name=TableNames.vendor_customers.name,
            left_column_name="normalized_vendor_customer_name",
            right_relation_name=TableNames.erp_accounts.name,
            right_column_name="normalized_erp_account_name",
            column_subset={
                "vendor_customer_billing_state":"erp_account_billing_state",
                "vendor_customer_billing_zip": "erp_account_billing_zip"
            }
        ),
        target_table_cfg=TargetTableCfg(
            name="vendor_customer_to_erp_account_candidate_map",
            upload_columns=['vendor_customer_id', 'erp_account_id','score', 'status'],
            join_columns=['vendor_customer_id', 'erp_account_id'],
            score_cutoff=80        
        )
    )
)

SIDEBAR_RELATIONSHIP_CFG = {
    "Vendor Customer ➡️ Parent Account": RelationshipFormCfg(
        option_display_name="Vendor Customer to Parent Account Relationship",
        target_table="vendor_customer_to_parent_account_map",
        parent_display_name="Parent Account ID",
        parent_api_name="parent_account_id",
        child_display_name="Vendor Customer ID",
        child_api_name="vendor_customer_id"
    ),
    "ERP Account ➡️ Parent Account": RelationshipFormCfg(
        option_display_name="ERP Account To Parent Account Relationship",
        target_table="erp_account_to_parent_account_map",
        parent_display_name="Parent Account ID",
        parent_api_name="parent_account_id",
        child_display_name="ERP Account ID",
        child_api_name="erp_account_id"
    ),
    "Vendor Customer ➡️ ERP Account": RelationshipFormCfg(
        option_display_name="Vendor Customer To ERP Account Relationship",
        target_table="vendor_customer_to_erp_account_map",
        parent_display_name="ERP Account ID",
        parent_api_name="erp_account_id",
        child_display_name="Vendor Customer ID",
        child_api_name="vendor_customer_id"
    )
}


# WORKFLOW_TAB_CFG = [
#     CheckboxControlledTabCfg(
#         checkbox_caption="Show Parent Accounts",
#         data_caption="Parent Accounts",
#         relation_name=TableNames.parents.value,
#     ),
#     CheckboxControlledTabCfg(
#         checkbox_caption="Show Vendor Customers",
#         data_caption="Vendor Customers",
#         relation_name="workflow_vendor_customers_mapping_vw",
#     ),
#     CheckboxControlledTabCfg(
#         checkbox_caption="Show ERP Accounts",
#         data_caption="ERP Accounts",
#         relation_name="workflow_erp_accounts_vw",
#     )
# ]






