from dataclasses import replace
from datetime import datetime
from decimal import Decimal
from typing import Any

from common.models.records import RawRecord


class BaseAggregator:
    def __init__(self, config=None):
        """
        Base constructor to store configuration for all aggregators.
        """
        self.config = config

    def aggregate_lines(self, records: list[RawRecord]) -> list[RawRecord]:
        raise NotImplementedError("Implementation missing")

    @staticmethod
    def safe_float(value):
        """Convert to float, return 0.0 if the value is empty or invalid."""
        try:
            return float(value) if value else 0.0
        except ValueError:
            return 0.0

    @staticmethod
    def sum_round(value1, value2, decimals=8):
        """Sum two values and round the result to the specified number of decimals."""

        v1 = BaseAggregator.safe_float(value1)
        v2 = BaseAggregator.safe_float(value2)
        return round(v1 + v2, decimals)

    @staticmethod
    def values_equal(val1: Any, val2: Any) -> bool:
        """
        Compare two values for equality, considering None as equal.

        Works for str, int, float, Decimal, datetime, or None.
        """
        # Both None
        if val1 is None and val2 is None:
            return True

        # One is None, the other not
        if val1 is None or val2 is None:
            return False

        # Otherwise, normal equality
        return val1 == val2

    @staticmethod
    def _is_coin_buy(record: RawRecord) -> bool:
        """
        A coin buy occurs when a crypto asset is bought in exchange for
        fiat currency or another asset.
        """

        crypto_currencies = {
            "BTC",
            "ETH",
            "ADA",
            "SOL2",
            "LUNA2",
            "LUNA3",
            "DFI",
            "BNB",
            "XRP",
            "KFEE",
        }

        stablecoins = {"USDC", "USDT", "BUSD"}
        fiat_currencies = {"EUR", "USD"}

        buy = record.buy_currency
        sell = record.sell_currency

        # Buying crypto with fiat
        if buy in crypto_currencies and sell in fiat_currencies:
            return True

        # Buying crypto with stablecoin
        if buy in crypto_currencies and sell in stablecoins:
            return True

        return False

    @staticmethod
    def _set_time(date_value: datetime, new_time: str) -> datetime:
        """
        Replace the time part of a datetime with a given HH:MM:SS value.
        """
        hours, minutes, seconds = map(int, new_time.split(":"))

        return datetime(
            year=date_value.year,
            month=date_value.month,
            day=date_value.day,
            hour=hours,
            minute=minutes,
            second=seconds,
        )


class CoinTrackingAggregator(BaseAggregator):
    def _is_aggregation_applicable(
        self, current_line: RawRecord, next_line: RawRecord
    ) -> bool:
        if (
            BaseAggregator.values_equal(current_line.type, next_line.type)
            and BaseAggregator.values_equal(
                current_line.buy_currency, next_line.buy_currency
            )
            and BaseAggregator.values_equal(
                current_line.sell_currency, next_line.sell_currency
            )
            and BaseAggregator.values_equal(
                current_line.fee_currency, next_line.fee_currency
            )
            and BaseAggregator.values_equal(current_line.exchange, next_line.exchange)
            and BaseAggregator.values_equal(current_line.group, next_line.group)
            and BaseAggregator.values_equal(current_line.comment, next_line.comment)
            and BaseAggregator.values_equal(
                current_line.date.date(), next_line.date.date()
            )  # nur Datum vergleichen
        ):
            return True
        else:
            return False

    def _adjust_timestamp(self, record: RawRecord) -> RawRecord:
        """
        Adjust the timestamp of a record based on its business meaning.

        Rules:
        - Deposits are normalized to 00:00:00
        - Coin buys are normalized to 00:01:00
        """

        # Rule 1: Deposit → 00:00:00
        if record.type == "Deposit":
            new_date = BaseAggregator._set_time(record.date, "00:00:00")
            return replace(record, date=new_date)

        # Rule 2: Coin buy → 00:01:00
        if record.type == "Trade" and self._is_coin_buy(record):
            new_date = BaseAggregator._set_time(record.date, "00:01:00")
            return replace(record, date=new_date)

        # Default: no change
        return record

    def _sort_result(self, records: list[RawRecord]) -> list[RawRecord]:
        """
        Sort records chronologically by date.
        """
        return sorted(records, key=lambda r: r.date)

    def aggregate_lines(self, records: list[RawRecord]) -> list[RawRecord]:
        """
        The aggregation process consolidates multiple transactions of one day (and further criterias) into a single daily entry.
        The specific logic for the time adjustment is documented in the `_adjust_timestamp` method.
        """
        if len(records) <= 1:
            return records

        result: list[RawRecord] = []

        aggr_buy = Decimal("0")
        aggr_sell = Decimal("0")
        aggr_fee = Decimal("0")
        aggregation_happened = False

        i = 0
        while i < len(records) - 1:
            current = records[i]
            next_rec = records[i + 1]

            if self._is_aggregation_applicable(current, next_rec):
                aggr_buy += current.buy_amount
                aggr_sell += current.sell_amount
                aggr_fee += current.fee_amount
                aggregation_happened = True
            else:
                if aggregation_happened:
                    current = replace(
                        current,
                        buy_amount=current.buy_amount + aggr_buy,
                        sell_amount=current.sell_amount + aggr_sell,
                        fee_amount=current.fee_amount + aggr_fee,
                        tx_id="",
                    )

                    aggr_buy = Decimal("0")
                    aggr_sell = Decimal("0")
                    aggr_fee = Decimal("0")
                    self._adjust_timestamp(current)

                result.append(current)
                aggregation_happened = False

            i += 1

        # letzte Zeile behandeln
        last = records[-1]
        if aggregation_happened:
            last = replace(
                last,
                buy_amount=last.buy_amount + aggr_buy,
                sell_amount=last.sell_amount + aggr_sell,
                fee_amount=last.fee_amount + aggr_fee,
                tx_id="",
            )

        self._adjust_timestamp(last)
        result.append(last)

        return self._sort_result(result)


class AggregatorFactory:
    @staticmethod
    def get_aggregator(format: str) -> BaseAggregator:
        if format == "CoinTracking":
            return CoinTrackingAggregator()
        else:
            raise ValueError(f"Unknown format: {format}")
