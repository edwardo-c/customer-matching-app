from pathlib import Path
from data_commands.context import AppPaths
from refresh.vendor_customers import Col, VendorCustomerCfg

APP_PATHS = AppPaths(
    db_path = Path(r"C:\Users\eddiec11us\dev_apps\customer-matching-app\src\data\db.duckdb")
)

VENDOR_CUSTOMERS_CFG = VendorCustomerCfg(
    path=Path(r"\\peernet\DavWWWRoot\Reporting\POS DATA\2025 - 2026 POS Pivot Incentive Comp.xlsx"),
    sheet="POS - 2025 to 2026",
    schema=[
        Col(name="Customer",rename="vendor_name"),
        Col(name="Sold To Name",  rename="raw_vendor_customer_name"),
        Col(name="Bill To Zip",   rename="billing_zip"),
        Col(name="Bill To State", rename="billing_state"),
    ],
    sql_path=Path(r"C:\Users\eddiec11us\dev_apps\customer-matching-app\src\sql\vendor_customers_staging.sql")
)


