"""primary runner for initiating app"""
import duckdb
from pathlib import Path
import os
import pandas as pd
from customer_matching.normalizer import normalize_col

def refresh_app():
    if DB_PATH.exists(): os.remove(str(DB_PATH))

    conn = duckdb.connect(DB_PATH)

    # INITIALIZE SCHEMA
    conn.execute(Path(r"C:\Users\eddiec11us\dev_apps\customer-matching-app\src\customer_matching\database\schema.sql").read_text(encoding="utf-8"))
    conn.execute(Path(r"C:\Users\eddiec11us\dev_apps\customer-matching-app\src\customer_matching\database\views.sql").read_text(encoding="utf-8"))

    # NORMALIZE VENDOR_CUSTOMER NAMES
    vendor_cust_df = pd.read_excel(r"C:\Users\eddiec11us\dev_apps\customer-matching-app\src\data\raw\almo_04_2026.xlsx")
    vendor_cust_normalized_df = normalize_col(vendor_cust_df, "raw_vendor_customer_name", "normalized_customer_name")
    conn.execute("INSERT INTO vendor_customers BY NAME SELECT * FROM vendor_cust_normalized_df")


    # NORMALIZE ERP CUSTOMER NAMES
    erp_cust_df = pd.read_excel(r"C:\Users\eddiec11us\dev_apps\customer-matching-app\src\data\raw\erp_05_2026.xlsx")
    erp_cust_normalized_df = normalize_col(erp_cust_df, "erp_account_name", "normalized_erp_account_name")
    conn.execute("INSERT INTO erp_accounts BY NAME SELECT * FROM erp_cust_normalized_df")




