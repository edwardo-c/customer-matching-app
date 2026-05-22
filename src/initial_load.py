"""primary runner for initiating app"""
import duckdb
from pathlib import Path
import os
import pandas as pd
from data_commands.normalizer import normalize_col, add_first3_token
from config import APP_PATHS

if APP_PATHS.db_path.exists(): os.remove(str(APP_PATHS.db_path))

conn = duckdb.connect(APP_PATHS.db_path)

# INITIALIZE SCHEMA
conn.execute(Path(r"C:\Users\eddiec11us\dev_apps\customer-matching-app\src\sql\tables.sql").read_text(encoding="utf-8"))
conn.execute(Path(r"C:\Users\eddiec11us\dev_apps\customer-matching-app\src\sql\views.sql").read_text(encoding="utf-8"))

# NORMALIZE VENDOR_CUSTOMER NAMES
vendor_cust_df = pd.read_excel(r"C:\Users\eddiec11us\dev_apps\customer-matching-app\src\data\raw\almo_04_2026.xlsx")

vendor_cust_normalized_df = normalize_col(
    df=vendor_cust_df, 
    col_in_name="raw_vendor_customer_name", 
    col_out_name="normalized_vendor_customer_name"
)

vendor_cust_normalized_df = add_first3_token(
    df=vendor_cust_normalized_df,
    col_in_name="normalized_vendor_customer_name",
    col_out_name="vendor_customer_first3_token"
)

conn.execute("INSERT INTO vendor_customers BY NAME SELECT * FROM vendor_cust_normalized_df")

# NORMALIZE ERP CUSTOMER NAMES
erp_cust_df = pd.read_excel(r"C:\Users\eddiec11us\dev_apps\customer-matching-app\src\data\raw\erp_05_2026.xlsx")

erp_cust_normalized_df = normalize_col(
    df=erp_cust_df, 
    col_in_name="erp_account_name", 
    col_out_name="normalized_erp_account_name"
)

erp_cust_normalized_df = add_first3_token(
    df=erp_cust_normalized_df, 
    col_in_name="normalized_erp_account_name", 
    col_out_name="erp_name_first3_token"
)

conn.execute("INSERT INTO erp_accounts BY NAME SELECT * FROM erp_cust_normalized_df")




