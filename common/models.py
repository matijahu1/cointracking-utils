

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

@dataclass(frozen=True)
class RawRecord:
    type: str
    buy_amount: Decimal
    buy_currency: str
    sell_amount: Decimal
    sell_currency: str
    fee_amount: Decimal
    fee_currency: str
    exchange: str
    group: str
    comment: str
    date: datetime
    tx_id: str

@dataclass(frozen=True)
class TargetRecord:
    type: str
    buy_amount: Decimal
    buy_currency: str
    sell_amount: Decimal
    sell_currency: str
    fee_amount: Decimal
    fee_currency: str
    exchange: str
    group: str
    comment: str
    date: datetime
    balance: Decimal
    balance_currency: str
