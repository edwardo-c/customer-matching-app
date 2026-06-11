"""load only new vendor customer names"""

from pathlib import Path
import pandas as pd
from dataclasses import dataclass, field
import duckdb
from data_commands.normalizer import add_normalized_name_col, add_first3_token
from refresh.cleaner import add_cleaned_zip_col
from data_commands.commands import bulk_insert_target_table

@dataclass(frozen=True)
class VendorCustomerSchema:
    """
    User provides name of the column to be renamed as the attribute name
    """
    vendor_name: str
    raw_vendor_customer_name: str
    raw_billing_zip: str
    billing_state: str
    period_date: str

@dataclass(frozen=True)
class VendorCustomerCfg:
    path: Path
    sheet: str
    sql_path: Path
    schema: VendorCustomerSchema
    rename_map: dict[str, str] = field(default_factory=dict)
    expected_cols: list[str] = field(default_factory=list)

    def __post_init__(self):
        _rename_map = {}
        _expected_cols = []
        for k, v in vars(self.schema).items():
            _rename_map[v] = k
            _expected_cols.append(v)

        object.__setattr__(self, "rename_map", _rename_map)
        object.__setattr__(self, "expected_cols", _expected_cols)


def validate_schema(
        *,
        current_cols: list[str], 
        expected_cols: list[str]
    ) -> None:
    """
    Confirm all columns in expected schema exist in current cols
    raises on missing column
    """
    for col in expected_cols:
        if col not in current_cols:
            raise KeyError(f"missing expected column: {col}")

def import_new_vendor_customers(
        cfg: VendorCustomerCfg, 
        conn: duckdb.DuckDBPyConnection
    ):
    """
    Primary runner for importing new vendor customers to db
    
    raises on missing expected columns

    adds normalized columns [normalized_vendor_customer_name, normalized_billing_zip, first3_token]
    """
    df = pd.read_excel(str(cfg.path), sheet_name=cfg.sheet)

    validate_schema(
        current_cols=list(df.columns), 
        expected_cols=cfg.expected_cols
    )

    df = df.rename(columns=cfg.rename_map)

    df = df[df["raw_vendor_customer_name"].isna() == False]

    # drop duplicates handled in sql EXCEPT

    df = add_cleaned_zip_col(
        df=df,
        col_in_name="raw_billing_zip", 
        col_out_name="normalized_billing_zip"
    )

    df = add_normalized_name_col(
        df=df, 
        col_in_name="raw_vendor_customer_name", 
        col_out_name="normalized_vendor_customer_name"
    )

    df = add_first3_token(
        df=df, 
        col_in_name="normalized_vendor_customer_name",
        col_out_name="first3_token"
    )

    conn.register("raw_vendor_customer_staging", df)

    bulk_insert_target_table(
        conn, 
        "vendor_customers", 
        conn.sql(cfg.sql_path.read_text(encoding="utf-8")).df()
    )

    # TODO: insert into Batches