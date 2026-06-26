from pathlib import Path
from context import AppPaths
from refresh.vendor_customers import VendorCustomerCfg, VendorCustomerSchema

APP_PATHS = AppPaths(
    db_path = Path(r"C:\Users\eddiec11us\dev_apps\customer-matching-app\src\data\db.duckdb"), 
    sql_base_path = Path(r"C:\Users\eddiec11us\dev_apps\customer-matching-app\src\sql"),
        sql_table_files=[
        '01_base_tables.sql',
        '02_relationship_tables.sql'
    ], 
    sql_views_files = [
        '01_base_views.sql',
        '02_vendor_customer_pair_views.sql',
        '03_vendor_customer_to_erp_account_views.sql'
        '04_parent_suggestion_views.sql',
        '05_unresolved_groups.sql',
    ],
)

VENDOR_CUSTOMERS_CFG = VendorCustomerCfg(
    path=Path(r"\\peernet\DavWWWRoot\Reporting\POS DATA\2025 - 2026 POS Pivot Incentive Comp.xlsx"),
    sheet="POS - 2025 to 2026",
    schema=VendorCustomerSchema(
        vendor_name="Customer",
        raw_vendor_customer_name="Sold To Name",
        raw_billing_zip="Bill To Zip",
        billing_state="Bill To State",
        period_date="Period Date"
    ),
    sql_path=Path(r"C:\Users\eddiec11us\dev_apps\customer-matching-app\src\sql\vendor_customers_staging.sql")
)


