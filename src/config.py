from pathlib import Path
from ui.tabs import CheckboxControlledTabCfg
from ui.sidebar import RelationshipFormCfg

DB_PATH = Path(r"C:\Users\eddiec11us\dev_apps\customer-matching-app\src\data\db.duckdb")
VIEWS_PATH = Path(r"C:\Users\eddiec11us\dev_apps\customer-matching-app\src\schema\views.sql")


WORKFLOW_TAB_CFG = [
    CheckboxControlledTabCfg(
        checkbox_caption="Show Parent Accounts",
        data_caption="Parent Accounts",
        relation_name="parent_accounts",
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
