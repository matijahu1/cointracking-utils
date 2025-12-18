import csv
import os

class DataExporter:
    def __init__(self, config):
        self.file_name = config.get_export_file()
    
    def save_data(self, df):
        df.columns = ["Cur." if col.startswith("Cur.") else col for col in df.columns]  #Rename some columns
        # df = df.sort_values(by=["Date"])  #already sorted 
                
        # Append lines (without header if file exists)
        file_exists = os.path.isfile(self.file_name)
        df.to_csv(self.file_name, mode='a', header=not file_exists, quoting=csv.QUOTE_ALL, index=False, float_format='%.10f'  )
