from datetime import datetime
from decimal import Decimal

from common.models.records import RawRecord, TargetRecord

COINTRACKING_DATE_FORMATS = (
    "%Y-%m-%d %H:%M:%S",  # International / ISO
    "%d.%m.%Y %H:%M:%S",  # Deutsch
)


def parse_date(date_str: str) -> datetime:
    """
    Konvertiert einen Datums-String aus CoinTracking CSVs in ein datetime-Objekt.
    Unterstützt verschiedene länderspezifische Formate.
    """
    if not date_str:
        raise ValueError("Datum-String ist leer")

    for fmt in COINTRACKING_DATE_FORMATS:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue

    raise ValueError(f"Zeitformat unbekannt oder nicht unterstützt: {date_str}")


def sort_target_records(records: list[TargetRecord]) -> None:
    records.sort(
        key=lambda r: (
            r.type,
            r.buy_currency,
            r.sell_currency,
            r.fee_currency,
            r.exchange,
            r.group,
            r.date,
        )
    )


def to_decimal(value: str) -> Decimal:
    """
    Converts a string to a Decimal object.
    Returns Decimal(0) if the string is empty or whitespace.
    """
    if not value or value.strip() == "":
        return Decimal(0)

    # Handle European comma format if necessary
    return Decimal(value.replace(",", "."))


def sort_records_for_aggregation(records: list[RawRecord]) -> None:
    """Sort logic specific to the Aggregation Tool."""
    records.sort(
        key=lambda r: (
            r.exchange,
            r.group,
            r.type,
            r.buy_currency,
            r.sell_currency,
            r.fee_currency,
            r.date,
        )
    )


def sort_records_for_calculation(records: list[RawRecord]) -> None:
    """Sort logic specific to the Calculation Tool."""
    records.sort(
        key=lambda r: (
            r.exchange,
            r.date,
        )
    )
