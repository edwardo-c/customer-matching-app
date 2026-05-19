from pathlib import Path
from ui.tabs import CheckboxControlledTabCfg
from ui.sidebar import RelationshipFormCfg
from loaders import MatchCfg
from enum import Enum
from load_helpers import AppPaths


APP_PATHS = AppPaths(
    db_path = Path(r"C:\Users\eddiec11us\dev_apps\customer-matching-app\src\data\db.duckdb"),
    views_path = Path(r"C:\Users\eddiec11us\dev_apps\customer-matching-app\src\schema\views.sql"),
    vendor_customers = Path(r"\\peernet\DavWWWRoot\Reporting\POS DATA\2025 - 2026 POS Pivot Incentive Comp.xlsx")
)




class TableNames(Enum):
    parents = "parent_accounts"
    vendor_customers = "vendor_customers"
    erp_accounts = "erp_accounts"

CANDIDATES_CFG = [
    # compare vendor to erp customers
    MatchCfg(
        left_table_name=TableNames.vendor_customers.value,
        left_column_name="normalized_customer_name",
        right_table_name=TableNames.erp_accounts.value,
        right_column_name="normalized_erp_account_name",
        column_subset=["billing_state", "billing_zip"]
    )
]


WORKFLOW_TAB_CFG = [
    CheckboxControlledTabCfg(
        checkbox_caption="Show Parent Accounts",
        data_caption="Parent Accounts",
        relation_name=TableNames.parents.value,
        relation_type="table"
    ),
    CheckboxControlledTabCfg(
        checkbox_caption="Show Vendor Customers",
        data_caption="Vendor Customers",
        relation_name="workflow_vendor_customers_mapping_vw",
        relation_type="view"
    ),
    CheckboxControlledTabCfg(
        checkbox_caption="Show ERP Accounts",
        data_caption="ERP Accounts",
        relation_name="workflow_erp_accounts_vw",
        relation_type="view"
    )
]

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


