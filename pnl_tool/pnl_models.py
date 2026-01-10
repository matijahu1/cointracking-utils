from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum, auto


class PositionSide(Enum):
    LONG = auto()
    SHORT = auto()


@dataclass
class AssetLot:
    """
    Represents an opening transaction that is waiting to be closed.
    """

    symbol: str
    side: PositionSide  # LONG or SHORT
    open_datetime: datetime
    amount: Decimal  # Initial amount of the position
    remaining_amount: Decimal  # Amount not yet closed
    open_price: Decimal  # Price at opening
    currency: str  # e.g., "USDT"


@dataclass
class PnLResult:
    """Represents a single match between a sale and a purchase lot."""

    symbol: str
    open_date: datetime
    close_date: datetime
    amount: Decimal
    open_price: Decimal
    close_price: Decimal
    currency: str
    pnl: Decimal

    # Potentially a method to convert to CSV-ready list
    def to_list(self) -> list:
        # Implementation for the exporter
        pass


@dataclass
class OpenLotExport:
    """
    Represents an unclosed position (Long or Short) for CSV export.
    """

    symbol: str
    side: str  # "LONG" or "SHORT"
    open_datetime: datetime
    remaining_amount: Decimal  # What's still left to close
    open_price: Decimal  # The price when this lot was opened
    currency: str  # e.g., "USDT" or "EUR"
    total_value_at_open: Decimal  # remaining_amount * open_price
