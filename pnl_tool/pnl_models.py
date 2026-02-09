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

    coin: str
    side: PositionSide  # LONG or SHORT
    open_datetime: datetime
    amount: Decimal  # Initial amount of the position
    remaining_amount: Decimal  # Amount not yet closed
    open_price: Decimal  # Price at opening
    currency: str  # e.g., "USDT"

    def __repr__(self):
        # Create a clean string similar to your record output
        date_str = self.open_datetime.strftime("%Y-%m-%d %H:%M")
        return (
            f"LOT: {date_str} | {self.side.name:5} | "
            f"Rem: {self.remaining_amount:12.4f} / {self.amount:12.4f} | "
            f"Price: {self.open_price:10.4f} {self.currency}"
        )


@dataclass
class OpenLot:
    """
    Represents an unclosed position (Long or Short) for CSV export.
    """

    coin: str
    side: str  # "LONG" or "SHORT"
    open_datetime: datetime
    remaining_amount: Decimal  # What's still left to close
    open_price: Decimal  # The price when this lot was opened
    currency: str  # e.g., "USDT" or "EUR"
    total_value_at_open: Decimal  # remaining_amount * open_price
