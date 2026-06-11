from pathlib import Path
from data_commands.context import AppPaths
from refresh.vendor_customers import VendorCustomerCfg, VendorCustomerSchema

APP_PATHS = AppPaths(
    db_path = Path(r"C:\Users\eddiec11us\dev_apps\customer-matching-app\src\data\db.duckdb")
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


