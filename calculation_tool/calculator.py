# import pandas as pd  -> The calculator should not know pandas because this is the domain layer
# Purpose of the Calculator: Business logic (domain layer)

from decimal import Decimal

from common.config import ConfigProtocol
from common.models.records import RawRecord, TargetRecord
from common.utils.helper import sort_records_for_calculation


class Calculator:
    def __init__(self, config: ConfigProtocol):
        self.config = config

    def track_balance(self, records: list[RawRecord]) -> list[TargetRecord]:
        """
        Track the balance of the configured coin over time.
        """

        sort_records_for_calculation(records)

        coin = self.config.get_coin()
        balance = Decimal("0")
        result: list[TargetRecord] = []

        for record in records:
            delta = Decimal("0")

            # Buy side
            if record.buy_currency == coin:
                delta += record.buy_amount

            # Sell side
            if record.sell_currency == coin:
                delta -= record.sell_amount

            # Fee side
            # if record.fee_currency == coin:
            #     delta -= record.fee_amount

            # If the coin is not involved at all, skip this record
            if delta == Decimal("0"):
                continue

            balance += delta

            result.append(
                TargetRecord(
                    type=record.type,
                    buy_amount=record.buy_amount,
                    buy_currency=record.buy_currency,
                    sell_amount=record.sell_amount,
                    sell_currency=record.sell_currency,
                    fee_amount=record.fee_amount,
                    fee_currency=record.fee_currency,
                    exchange=record.exchange,
                    group=record.group,
                    comment=record.comment,
                    date=record.datetime,
                    balance=balance,
                    balance_currency=coin,
                )
            )

        return result
