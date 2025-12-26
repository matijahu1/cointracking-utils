import csv
from dataclasses import astuple
from pathlib import Path
from typing import Sequence

from common.models.records import RawRecord, TargetRecord


class DataExporter:
    def _save(self, path: Path, header: list[str], data: Sequence) -> None:
        """Internal helper to handle the actual file I/O."""
        with open(path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            writer.writerow(header)
            for record in data:
                writer.writerow(astuple(record))

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

    @staticmethod
    def _fmt_decimal(value):
        """
        Format Decimal values for CSV output.
        Empty or zero values are written as empty strings.
        """
        if value is None:
            return ""
        return f"{value:.10f}".rstrip("0").rstrip(".")
