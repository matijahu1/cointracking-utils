from decimal import Decimal
import pandas as pd

from common.models import RawRecord

class DataImporter:
    def __init__(self, config, check_coin=False):
        self.file_name = config.get_import_file()
        self.data_format = config.get_data_format()
        self.ct_exchange = config.get_ct_exchange()
        self.ct_year = config.get_ct_year()
        self.check_coin = check_coin
        self.coin = config.get_coin()

    def load_data(self):                
        df = pd.read_csv(self.file_name)

        # Special filter for CoinTracking data. 
        if self.data_format == 'CoinTracking':
            df = df[(df['Exchange'] == self.ct_exchange) & (df['Date'].str.startswith(self.ct_year))]
            df = df.sort_values(by=["Type", "Cur.", "Cur..1", "Cur..2", "Exchange", "Group", "Comment", "Date"])
        
         # Additional filter if check_coin is True
        if self.check_coin:
            df = df[(df['Cur.'] == self.coin) | (df['Cur..1'] == self.coin) | (df['Cur..2'] == self.coin)]   
            
        df["Comment"] = df["Comment"].fillna("").astype(str)                 
        return df