from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from pnl_tool.pnl_models import PositionSide


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
    lpn: str
    tx_id: str

    @classmethod
    def from_ct_row(cls, row: dict) -> "RawRecord":
        return cls(
            type=row.get("Type", ""),
            buy_amount=Decimal(row.get("Buy") or "0"),
            buy_currency=row.get("Cur.") or "",
            sell_amount=Decimal(row.get("Sell") or "0"),
            sell_currency=row.get("Cur..1") or "",
            fee_amount=Decimal(row.get("Fee") or "0"),
            fee_currency=row.get("Cur..2") or "",
            exchange=row.get("Exchange") or "",
            group=row.get("Group") or "",
            comment=row.get("Comment") or "",
            date=datetime.strptime(row["Date"], "%Y-%m-%d %H:%M:%S"),
            lpn=row.get("LPN") or "",
            tx_id=row.get("Tx-ID") or "",
        )

    def __repr__(self) -> str:
        # Feste Breiten für die Spalten sorgen für das Tabellen-Layout
        date_str = self.date.strftime("%Y-%m-%d %H:%M") if self.date else "N/A"
        return (
            f"{date_str:<17} | {self.type:<10} | "
            f"{self.buy_amount:>10} {self.buy_currency:<5} | "
            f"{self.sell_amount:>10} {self.sell_currency:<5} | "
            f"{self.exchange:<12}"
        )


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


@dataclass
class PnLResult:
    """Represents a single match between a sale and a purchase lot."""

    coin: str
    side: PositionSide  # LONG or SHORT
    open_date: datetime
    close_date: datetime
    amount: Decimal
    open_price: Decimal
    close_price: Decimal
    currency: str
    pnl: Decimal
    method: str

    # Potentially a method to convert to CSV-ready list
    def to_list(self) -> list:
        # Implementation for the exporter
        pass
