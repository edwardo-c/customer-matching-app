from pathlib import Path
from ui.tabs import CheckboxControlledTabCfg
from ui.sidebar import RelationshipFormCfg

DB_PATH = Path(
    r"C:\Users\eddiec11us\dev_apps\customer-matching-app\src\data\db.duckdb"
)

WORKFLOW_TAB_CFG = [
    CheckboxControlledTabCfg(
        checkbox_caption="Show Parent Accounts",
        table_caption="Parent Accounts",
        table_name="parent_accounts",
        reader_key="table"
    ),
    CheckboxControlledTabCfg(
        checkbox_caption="Show Vendor Customers",
        table_caption="Vendor Customers",
        table_name="vendor_customers",
        reader_key="table"
    ),
    CheckboxControlledTabCfg(
        checkbox_caption="Show ERP Accounts",
        table_caption="ERP Accounts",
        table_name="erp_accounts",
        reader_key="table"
    )
]

RELATIONSHIP_TAB_CFG = [
    CheckboxControlledTabCfg(
        checkbox_caption="Show Vendor Cust -> ERP",
        table_caption="Vendor Customers to ERP Accounts",
        table_name="vendor_customter_to_erp_account_vw",
        reader_key="view"
    ),
    CheckboxControlledTabCfg(
        checkbox_caption="Show Vendor Cust -> Parents",
        table_caption="Vendor Customer to Parent Accounts",
        table_name="vendor_customer_to_parent_account_vw",
        reader_key="view"
    ),
    CheckboxControlledTabCfg(
        checkbox_caption="Show ERP Cust -> Parents",
        table_caption="ERP Accounts to Parent Accounts",
        table_name="erp_account_to_parent_account_vw",
        reader_key="view"
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
