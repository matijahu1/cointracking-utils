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
    tx_id: str
