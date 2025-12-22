import csv
import os
from typing import List

from common.models import RawRecord


class DataExporter:
    def __init__(self, config):
        self.file_name = config.get_export_file()

    def save_data(self, records: List[RawRecord]) -> None:
        """
        Persist RawRecord objects to a CSV file in CoinTracking format.
        Appends to the file if it already exists.
        """

        file_exists = os.path.isfile(self.file_name)

        with open(self.file_name, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)

            # Write header only once
            if not file_exists:
                writer.writerow(
                    [
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
                )

            for r in records:
                writer.writerow(
                    [
                        r.type,
                        self._fmt_decimal(r.buy_amount),
                        r.buy_currency,
                        self._fmt_decimal(r.sell_amount),
                        r.sell_currency,
                        self._fmt_decimal(r.fee_amount),
                        r.fee_currency,
                        r.exchange,
                        r.group,
                        r.comment or "",
                        r.date.strftime("%Y-%m-%d %H:%M:%S"),
                        r.tx_id,
                    ]
                )

    @staticmethod
    def _fmt_decimal(value):
        """
        Format Decimal values for CSV output.
        Empty or zero values are written as empty strings.
        """
        if value is None:
            return ""
        return f"{value:.10f}".rstrip("0").rstrip(".")
