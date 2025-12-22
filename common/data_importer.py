import csv
from decimal import Decimal
from pathlib import Path
from typing import List

from common.models import RawRecord
from common.utils.date_helper import parse_date


class DataImporter:
    def __init__(self, config, check_coin=False):
        self.file_name = config.get_import_file()
        self.data_format = config.get_data_format()
        self.ct_exchanges = config.get_ct_exchanges()
        self.ct_year = config.get_ct_year()
        self.check_coin = check_coin
        self.coin = config.get_coin()

    # def load_data(self) -> list[RawRecord]:
    #     all_records = self.parse_csv_file(self.file_name)

    #     filtered_records = []
    #     for r in all_records:
    #         if r.exchange == self.ct_exchange and str(r.date.year) == self.ct_year:
    #             if self.check_coin:
    #                 if self.coin in (r.buy_currency, r.sell_currency, r.fee_currency):
    #                     filtered_records.append(r)
    #             else:
    #                 filtered_records.append(r)

    #     return filtered_records
    def load_data(self) -> list[RawRecord]:
        """
        Load and filter RawRecords from CSV input.
        Empty config values ("" or []) disable the corresponding filter.
        """
        all_records = self.parse_csv_file(self.file_name)
        filtered_records: list[RawRecord] = []

        exchanges = self.ct_exchanges  # list[str]

        for r in all_records:
            # Exchange filter
            if exchanges and r.exchange not in exchanges:
                continue

            # Year filter
            if self.ct_year and str(r.date.year) != self.ct_year:
                continue

            # Coin filter
            if self.check_coin:
                if self.coin not in (r.buy_currency, r.sell_currency, r.fee_currency):
                    continue

            filtered_records.append(r)

        return filtered_records

    @staticmethod
    def parse_csv_file(path: str) -> List[RawRecord]:
        """
        Reads CSV and converts data into RawRecord List.
        Sorts the list.
        :param path: Path of CSV file
        """
        records = []
        with open(Path(path), newline="", encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            header = next(reader)  # Header überspringen

            for row in reader:
                if not row:
                    continue

                # Manuelle Zuweisung basierend auf der CoinTracking CSV-Struktur
                record = RawRecord(
                    type=row[0],
                    buy_amount=Decimal(row[1]) if row[1] else Decimal(0),
                    buy_currency=row[2],
                    sell_amount=Decimal(row[3]) if row[3] else Decimal(0),
                    sell_currency=row[4],
                    fee_amount=Decimal(row[5]) if row[5] else Decimal(0),
                    fee_currency=row[6],
                    exchange=row[7],
                    group=row[8],
                    comment=row[9],
                    date=parse_date(row[10]),
                    tx_id=row[11],
                )
                records.append(record)

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
