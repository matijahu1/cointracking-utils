"""
Adapter Module

Purpose:
- Converts external / raw data into internal Domain objects.
- Handles parsing, normalization, and configuration-specific rules.
- Knows about external formats (CSV columns, JSON keys, etc.).
- Produces objects that are ready for business logic.

Responsibilities:
- Parse strings, decimals, and dates according to config.
- Apply default values and fallbacks.
- Produce a single Domain object (e.g., RawRecord) from a single input row.

Adapter = 1 row → 1 Domain object
"""

from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime
import pandas as pd

from common.config import Config, ConfigProtocol
from common.models import RawRecord, TargetRecord

def parse_decimal(val, decimal_separator=".") -> Decimal:
    if pd.isna(val) or str(val).strip() == "":
        return Decimal("0")
    s = str(val).strip()
    if decimal_separator == ",":
        # "1.234,56" -> "1234.56"
        s = s.replace(".", "").replace(",", ".")
    return Decimal(s)

def parse_datetime(val, date_format: str) -> datetime:
    if isinstance(val, datetime):
        return val
    return datetime.strptime(str(val).strip(), date_format)

def rawrecord_from_series(s: pd.Series, cfg: ConfigProtocol) -> "RawRecord":
    """
    Convert a pandas Series into a RawRecord using parsing and normalization rules from cfg.
    """    
    record = RawRecord(
        type=str(s.get("Type", "")).strip(),
        buy_amount=parse_decimal(s.get("Buy", 0), cfg.get_decimal_separator()),
        buy_currency=str(s.get("Buy Cur.", s.get("Cur.", ""))).strip(),
        sell_amount=parse_decimal(s.get("Sell", 0), cfg.get_decimal_separator()),
        sell_currency=str(s.get("Sell Cur.", s.get("Cur..1", ""))).strip(),
        fee_amount=parse_decimal(s.get("Fee", 0), cfg.get_decimal_separator()),
        fee_currency=str(s.get("Fee Cur.", s.get("Cur..2", ""))).strip(),
        exchange=str(s.get("Exchange", "")).strip(),
        group=str(s.get("Group", "")).strip(),
        comment=str(s.get("Comment", "")).strip(),
        date=parse_datetime(s.get("Date"), cfg.get_date_format()),
        tx_id=str(s.get("Tx-ID", "")).strip(),
    )

    return record

def target_record_from_series(s: pd.Series, cfg: ConfigProtocol) -> "TargetRecord":
    """
    Convert a pandas Series into a TargetRecord using parsing and normalization rules from cfg.
    """    
    record = TargetRecord(
        type=str(s.get("Type", "")).strip(),
        buy_amount=parse_decimal(s.get("Buy", 0), cfg.get_decimal_separator()),
        buy_currency=str(s.get("Buy Cur.", s.get("Cur.", ""))).strip(),
        sell_amount=parse_decimal(s.get("Sell", 0), cfg.get_decimal_separator()),
        sell_currency=str(s.get("Sell Cur.", s.get("Cur..1", ""))).strip(),
        fee_amount=parse_decimal(s.get("Fee", 0), cfg.get_decimal_separator()),
        fee_currency=str(s.get("Fee Cur.", s.get("Cur..2", ""))).strip(),
        exchange=str(s.get("Exchange", "")).strip(),
        group=str(s.get("Group", "")).strip(),
        comment=str(s.get("Comment", "")).strip(),
        date=parse_datetime(s.get("Date"), cfg.get_date_format()),
        balance=parse_decimal(s.get("Balance", 0), cfg.get_decimal_separator()),
        balance_currency=str(s.get("BCur", s.get("BCur", ""))).strip(),
    )

    return record
