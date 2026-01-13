from typing import Any, Dict

from common.models.records import PnLResult, RawRecord, TargetRecord
from common.utils.csv_helpers import read_ct_csv
from common.utils.helper import (
    parse_date,
    sort_target_records,
    to_decimal,
)
from pnl_tool.pnl_models import PositionSide


class DataImporter:
    def __init__(self, config: Dict[str, Any], coin_filtering_enabled=False):
        self.file_name = config.get_import_file()
        self.data_format = config.get_data_format()
        self.ct_exchanges = config.get_ct_exchanges()
        self.ct_year = config.get_ct_year()
        self.coin_filtering_enabled = coin_filtering_enabled
        self.coin = config.get_coin()

    def load_data(self) -> list[RawRecord]:
        """
        Load and filter RawRecords from CSV input.<br>
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
            if self.coin_filtering_enabled:
                if self.coin not in (r.buy_currency, r.sell_currency, r.fee_currency):
                    continue

            filtered_records.append(r)

        return filtered_records

    @staticmethod
    def parse_csv_file(path: str) -> list[RawRecord]:
        """
        Reads a CoinTracking CSV file and converts it into a list of RawRecord objects.
        """
        rows = read_ct_csv(path)

        records = [
            RawRecord(
                type=row[0],
                buy_amount=to_decimal(row[1]),
                buy_currency=row[2],
                sell_amount=to_decimal(row[3]),
                sell_currency=row[4],
                fee_amount=to_decimal(row[5]),
                fee_currency=row[6],
                exchange=row[7],
                group=row[8],
                comment=row[9],
                date=parse_date(row[10]),
                lpn=row[11],
                tx_id=row[12],
            )
            for row in rows
        ]
        return records

    @staticmethod
    def parse_target_csv_file(path: str) -> list[TargetRecord]:
        rows = read_ct_csv(path)

        records = []
        for row in rows:
            if not row:
                continue

            record = TargetRecord(
                type=row[0],
                buy_amount=to_decimal(row[1]),
                buy_currency=row[2],
                sell_amount=to_decimal(row[3]),
                sell_currency=row[4],
                fee_amount=to_decimal(row[5]),
                fee_currency=row[6],
                exchange=row[7],
                group=row[8],
                comment=row[9],
                date=parse_date(row[10]),
                balance=to_decimal(row[11]),  # Neu im Target
                balance_currency=row[12],  # Neu im Target
            )
            records.append(record)

        # Sortierung wie gewünscht
        sort_target_records(records)
        return records

    @staticmethod
    def parse_pnl_result_csv_file(path: str) -> list[PnLResult]:
        """
        Parses a PnL result CSV file back into a list of PnLResult objects.
        Used primarily for automated testing.
        """
        rows = read_ct_csv(path)  # Reusing your existing CSV reader

        results = []
        for row in rows:
            if not row:
                continue

            # Mapping the CSV columns back to the dataclass fields
            result = PnLResult(
                coin=row[0],
                # Convert the string back to the Enum
                side=PositionSide[row[1]],
                open_date=parse_date(row[2]),
                close_date=parse_date(row[3]),
                amount=to_decimal(row[4]),
                open_price=to_decimal(row[5]),
                close_price=to_decimal(row[6]),
                currency=row[7],
                pnl=to_decimal(row[8]),
                method=row[9],
            )
            results.append(result)

        # Sorting for consistent comparison in tests
        # Primary by close date, secondary by open date
        results.sort(key=lambda x: (x.close_date, x.open_date))
        return results
