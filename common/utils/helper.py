from datetime import datetime
from typing import List

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


def sort_raw_records(records: List) -> List:
    """
    Sortiert eine Liste von RawRecord Objekten nach einer definierten
    Hierarchie von Attributen.
    """
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
    return records
