#import pandas as pd  -> The calculator should not know pandas because this is the domain layer
# Purpose of the Calculator: Business logic (domain layer)

from decimal import Decimal
from common.config import Config, ConfigProtocol
from common.models import RawRecord, TargetRecord

class Calculator:
    def __init__(self, config: ConfigProtocol):
        self.config = config
        
    def track_balance(self, records: list[RawRecord]) -> list[TargetRecord]:
        """
        Track the balance of the configured coin over time.
        """
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
            if record.fee_currency == coin:
                delta -= record.fee_amount

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
                    date=record.date,
                    balance=balance,
                    balance_currency=coin,
                )
            )

        return result
                
# Die Methode brauche ich vermutlich nicht mehr. Das war ein erster Ansatz, der mit DataFrame gearbeitet hat.        
    # def calculate_balance(self, df_in: pd.DataFrame) -> pd.DataFrame:
    #     # Initialize balance and a list to store applicable rows
    #     balance = 0.0
    #     applicable_rows = []

    #     for index, current_line in df_in.iterrows():
    #         # Check if the current line meets the criteria for either buy or sell
    #         balance_changed = False
    #         if self._is_applicable_buy(current_line):
    #             balance += current_line['Buy']
    #             balance_changed = True
    #         elif self._is_applicable_sell(current_line):
    #             balance -= current_line['Sell']
    #             balance_changed = True
            
    #         # Only add to results if the balance was changed (i.e., if it was a buy or sell)
    #         if balance_changed:
    #             # Enter the balance in the new column 'Balance'
    #             current_line['Balance'] = balance
    #             # Append the updated line to the applicable rows list
    #             applicable_rows.append(current_line)

    #     # Create a new DataFrame from the list of applicable rows
    #     df_result = pd.DataFrame(applicable_rows)

    #     return df_result

    # def _is_applicable_buy(self, current_line: pd.Series) -> bool:
    #     result = False
        
    #     # Check if this is a buy transaction 
    #     if current_line['Cur.'] == self.coin:
    #         if current_line['Type'] == "Trade" or "Income (non taxable)" or "Reward / Bonus":
    #             result = True
                
    #     return result

    # def _is_applicable_sell(self, current_line: pd.Series) -> bool:
    #     # Check if this is a sell transaction (ETH in "Cur..1" field)
    #     return current_line['Type'] == "Trade" and current_line['Cur..1'] == self.coin