"""load only new vendor customer names"""

from pathlib import Path
import pandas as pd
from dataclasses import dataclass, field
import duckdb
from data_commands.normalizer import normalize_col
from src.refresh.cleaner import clean_zip_col

@dataclass
class Col:
    name: str
    rename: str

@dataclass(frozen=True)
class VendorCustomerCfg:
    path: Path
    sheet: str
    schema: list[Col]
    sql_path: Path
    expected_cols: list[str] = field(default_factory=list)
    rename_map: dict[str, str] = field(default_factory=dict)
    final_schema: list[str] = field(default_factory=list)
    normalize_col_in: str = "raw_vendor_customer_name"
    normalize_col_out: str = "normalized_vendor_customer_name"
    register_as: str = "vendor_customer_staging"
    zip_col_name: str = "billing_zip"

    def __post_init__(self):
        _final_schema = []
        _expected_cols = []
        _rename_map = {}
        for c in self.schema:
            _expected_cols.append(c.name)
            _final_schema.append(c.rename)
            _rename_map[c.name] = c.rename

        object.__setattr__(self, "rename_map", _rename_map)
        object.__setattr__(self, "final_schema", _final_schema)
        object.__setattr__(self, "expected_cols", _expected_cols)

def read_dot_sql(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def _validate_schema(
        *,
        current_cols: list[str], 
        expected_cols: list[Col]
    ) -> None:
    """Confirm all columns in expected schema exist in current cols"""
    for col in expected_cols:
        if col not in current_cols:
            raise KeyError(f"missing expected column: {col}")

def import_new_vendor_customers(cfg: VendorCustomerCfg, conn: duckdb.DuckDBPyConnection):
    """
    Primary runner for importing new vendor customers to db, drops rows where name is na
    """
    df = pd.read_excel(str(cfg.path), sheet_name=cfg.sheet)

    _validate_schema(
        current_cols=list(df.columns), 
        expected_cols=cfg.expected_cols
    )

    df = df.rename(columns=cfg.rename_map)[cfg.final_schema].drop_duplicates()

    df = clean_zip_col(cfg.zip_col_name, df)

    df = df[df["raw_vendor_customer_name"].isna() == False]

    norm_df = normalize_col(
        df=df, 
        col_in_name=cfg.normalize_col_in, 
        col_out_name=cfg.normalize_col_out
    )

    conn.register(cfg.register_as, norm_df)

    new_vendor_customers = conn.sql(cfg.sql_path.read_text(encoding="utf-8")).df()

    breakpoint()