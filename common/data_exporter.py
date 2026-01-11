import csv
from dataclasses import astuple
from decimal import Decimal
from pathlib import Path
from typing import Sequence

from common.models.records import PnLResult, RawRecord, TargetRecord


class DataExporter:
    def _save(self, path: Path, header: list[str], data: Sequence) -> None:
        """Internal helper to handle the actual file I/O."""
        with open(path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            writer.writerow(header)
            for record in data:
                # Konvertiere den Record in ein Tuple und formatiere jedes Element
                row = [self._format_value(v) for v in astuple(record)]
                writer.writerow(row)

    def _format_value(self, value):
        """Helper to decide how to format each field."""
        if isinstance(value, Decimal):
            return self._format_decimal(value)
        if value is None:
            return ""
        # Datetime Objekte oder andere Typen werden standardmäßig zu Strings
        return str(value)

    def save_raw_data(self, path: Path, records: Sequence[RawRecord]) -> None:
        header = [
            "Type",
            "Buy",
            "Cur.",
            "Sell",
            "Cur.",
            "Fee",
            "Cur.",
            "Exchange",
            "Group",
            "Comment",
            "Date",
            "LPN",
            "Tx-ID",
        ]
        self._save(path, header, records)

    def save_target_data(self, path: Path, records: Sequence[TargetRecord]) -> None:
        header = [
            "Type",
            "Buy",
            "Cur.",
            "Sell",
            "Cur.",
            "Fee",
            "Cur.",
            "Exchange",
            "Group",
            "Comment",
            "Date",
            "Balance",
            "BCur",
        ]
        self._save(path, header, records)

    def save_pnl_results(self, path: Path, records: Sequence[PnLResult]) -> None:
        """Saves the PnLResult records to a CSV file matching the dataclass structure."""
        header = [
            "Coin",
            "Side (Long/Short)",
            "Open Date",
            "Close Date",
            "Amount",
            "Open Price",
            "Close Price",
            "Currency",
            "PnL",
            "Method",
        ]
        self._save(path, header, records)

    @staticmethod
    def _format_decimal(value):
        """
        Format Decimal values for CSV output.
        Empty or zero values are written as empty strings.
        """
        if value is None:
            return ""
        return f"{value:.10f}".rstrip("0").rstrip(".")
