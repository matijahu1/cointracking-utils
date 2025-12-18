import sys
import pandas as pd
from numpy import nan

class BaseAggregator:
    def aggregate_lines(self, df: pd.DataFrame) -> pd.DataFrame:
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
    def values_equal(val1, val2):
        return val1 == val2 or (pd.isna(val1) and pd.isna(val2))
           
    @staticmethod
    def _is_coin_buy(line: pd.Series) -> bool:
        """
        Is this a coin buy?
        Determines if the transaction is a coin purchase based on the 'Cur.' field.
        
        Args:
            line (pd.Series): The row of data to analyze.
            
        Returns:
            bool: True if the trade indicates the purchase of a coin or stablecoin
        """
        # Check if 'Cur.' is a coin
        currency = line.get("Cur.")
        if currency in ["BTC", "DFI", "ETH", "SOL2", "LUNA2", "LUNA3", "ADA", "KFEE"]:
            return True
        
        # Elif: Check if 'Cur.' is a stablecoin AND 'Cur..1' is Fiat
        elif currency in ["USDC", "USDT", "DFI", "XRP", "BNB", "BUSD", "KFEE"]:
            sell_currency = line.get("Cur..1")
            if sell_currency in ["EUR", "USD"]:
                return True

        # Default: Return False if none of the conditions are met
        return False
    
    @staticmethod
    def _set_time(date_value: str, new_time: str) -> str:
        return date_value[:-8] + new_time
    
class CoinTrackingAggregator(BaseAggregator):

    def _is_aggregation_applicable(self, current_line, next_line):
        # Prüfen, ob Time und Asset identisch sind
        if (
            BaseAggregator.values_equal(current_line["Type"], next_line["Type"]) and 
            BaseAggregator.values_equal(current_line["Cur."], next_line["Cur."]) and 
            BaseAggregator.values_equal(current_line["Cur..1"], next_line["Cur..1"]) and 
            BaseAggregator.values_equal(current_line["Cur..2"], next_line["Cur..2"]) and 
            BaseAggregator.values_equal(current_line["Exchange"], next_line["Exchange"]) and 
            BaseAggregator.values_equal(current_line["Group"], next_line["Group"]) and 
            BaseAggregator.values_equal(current_line["Comment"], next_line["Comment"]) and 
            BaseAggregator.values_equal(current_line["Date"][:10], next_line["Date"][:10])
        ):
            return True
        else:
            return False
    
    def _adjust_timestamp(self, line: pd.Series):
        # Set time for Deposit to 00:00:00
        if line["Type"] == "Deposit":
            line["Date"] = BaseAggregator._set_time(line["Date"], "00:00:00")
            return
        
        # Set time for Coin Buy to 00:01:00
        if line["Type"] == "Trade" and self._is_coin_buy(line):
            line["Date"] = BaseAggregator._set_time(line["Date"], "00:01:00")

    def _sort_result(self, df: pd.DataFrame) -> pd.DataFrame:
        # Sortiere nach Datum und setze Index zurück
        return df.sort_values(by=["Date"]).reset_index(drop=True)

    def aggregate_lines(self, df: pd.DataFrame) -> pd.DataFrame:

        # Temporary mapping of column names
        # columns_mapping = {
        #     "Type": "Type",
        #     "Buy": "Buy",
        #     "Cur.": "Cur.",
        #     "Sell": "Sell",
        #     "Cur..1": "Cur.",
        #     "Fee": "Fee",
        #     "Cur..2": "Cur.",
        #     "Exchange": "Exchange",
        #     "Group": "Group",
        #     "Comment": "Comment",
        #     "Date": "Date",
        #     "Tx-ID": "Tx_ID"
        # }
        
        result_table = pd.DataFrame(columns=df.columns)  
        aggregation_happended = False
        aggr_buy = 0.00
        aggr_sell = 0.00
        aggr_fee  = 0.00

        if len(df) <= 1:
        #    print("Number of input lines <= 1. Nothing to aggregate.") 
        #    sys.exit(1) 
            return df
              
        i = 0
        while i < len(df) - 1:
            current_line = df.iloc[i]
            next_line = df.iloc[i + 1]

            if self._is_aggregation_applicable(current_line, next_line) == True:

                # Aggregate fields buy, sell, fee
                aggr_buy += BaseAggregator.safe_float(current_line["Buy"])              
                aggr_sell += BaseAggregator.safe_float(current_line["Sell"])   
                aggr_fee  += BaseAggregator.safe_float(current_line["Fee"])    

                aggregation_happended = True
            else:
                # Wenn nicht (mehr) aggregiert werden kann, speichere die current_line in die result_table 
                if aggregation_happended == True:
                    current_line["Buy"] = BaseAggregator.sum_round(current_line["Buy"], aggr_buy)
                    current_line["Sell"] = BaseAggregator.sum_round(current_line["Sell"], aggr_sell)
                    current_line["Fee"] = BaseAggregator.sum_round(current_line["Fee"], aggr_fee)
                    aggr_buy = 0.00
                    aggr_sell = 0.00
                    aggr_fee  = 0.00
                    current_line["Tx-ID"] = nan
                    
                # Adjust time if this is a coin purchase
                self._adjust_timestamp(current_line)                

                # Add current_line to result_table
                result_table = pd.concat([result_table, pd.DataFrame([current_line])], ignore_index=True)
                aggregation_happended = False
            
            # Fortsetzen mit der nächsten Zeile
            i += 1
        
        # Add last line
        if i == len(df) - 1:
            if aggregation_happended == True: # Prepare next_line
                next_line["Buy"] =  BaseAggregator.sum_round(next_line["Buy"], aggr_buy)
                next_line["Sell"] = BaseAggregator.sum_round(next_line["Sell"], aggr_sell)
                next_line["Fee"] = BaseAggregator.sum_round(next_line["Fee"], aggr_fee)
                next_line["Tx-ID"] = ""
            
            self._adjust_timestamp(next_line)         
            result_table = pd.concat([result_table, pd.DataFrame([next_line])], ignore_index=True)                

        return self._sort_result(result_table)

class AggregatorFactory:
    @staticmethod
    def get_aggregator(format: str) -> BaseAggregator:
        if format == 'CoinTracking':
            return CoinTrackingAggregator()
        else:
            raise ValueError(f"Unknown format: {format}")
