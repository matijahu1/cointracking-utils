"""
Mapper Module

Purpose:
- Orchestrates the conversion of multiple external data rows into Domain objects.
- Delegates row-level parsing to the Adapter.
- Knows about batch structures (DataFrame, list of dicts, etc.).
- Produces a collection of Domain objects ready for business logic.

Responsibilities:
- Iterate over multiple rows.
- Call adapter functions for each row.
- Return a list of Domain objects (e.g., List[RawRecord]).
- Does NOT implement any business logic.

Mapper = many rows → list of Domain objects
"""

import pandas as pd

from .adapters import rawrecord_from_series, target_record_from_series
from .config import ConfigProtocol
from .models import RawRecord, TargetRecord


def dataframe_to_raw_records(df: pd.DataFrame, cfg: ConfigProtocol) -> list[RawRecord]:
    """
    Convert a DataFrame to a list of RawRecord objects using the adapter.
    """
    records = []  # prepare empty list to collect RawRecords

    # iterate over each row in the DataFrame
    for index, row in df.iterrows():
        # convert a single row to RawRecord
        record = rawrecord_from_series(row, cfg)
        # add the RawRecord to the list
        records.append(record)

    return records


def dataframe_to_target_records(
    df: pd.DataFrame, cfg: ConfigProtocol
) -> list[TargetRecord]:
    """
    Convert a DataFrame to a list of TargetRecord objects using the adapter.
    """
    records = []

    for index, row in df.iterrows():
        record = target_record_from_series(row, cfg)
        records.append(record)

    return records


def normalize_ct_columns(df: pd.DataFrame) -> pd.DataFrame:
    rename_map = {
        "Cur.": "Buy Cur.",
        "Cur..1": "Sell Cur.",
        "Cur..2": "Fee Cur.",
    }
    # nur vorhandene Spalten umbenennen
    existing = {k: v for k, v in rename_map.items() if k in df.columns}
    df = df.rename(columns=existing)
    return df


def target_records_to_dataframe(records: list[TargetRecord]) -> pd.DataFrame:
    rows = []

    for r in records:
        rows.append(
            {
                "Type": r.type,
                "Buy": r.buy_amount,
                "BuyCur": r.buy_currency,
                "Sell": r.sell_amount,
                "SellCur": r.sell_currency,
                "Fee": r.fee_amount,
                "FeeCur": r.fee_currency,
                "Exchange": r.exchange,
                "Group": r.group,
                "Comment": r.comment or "",
                "Date": r.date,
                "Balance": r.balance,
            }
        )

    return pd.DataFrame(rows)


def raw_records_to_dataframe(records: list[RawRecord]) -> pd.DataFrame:
    return pd.DataFrame(records)
