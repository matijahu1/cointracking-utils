import pandas as pd
from calculation_tool.calculator import Calculator
from common.config import Config
from common.data_importer import DataImporter
from common.data_exporter import DataExporter
from common.mappers import dataframe_to_raw_records, target_records_to_dataframe


class CalculationTool:
    def __init__(self):
        self.config = Config('./calculation_tool/data/config.json')
        self.importer = DataImporter(self.config, check_coin=True)
        self.calculator = Calculator(self.config)
        self.exporter = DataExporter(self.config)

    def run(self):
        df = self.importer.load_data()
        raw_records = dataframe_to_raw_records(df, self.config)
        target_records = self.calculator.track_balance(raw_records)
        result_df = target_records_to_dataframe(target_records)
        self.exporter.save_data(result_df)

if __name__ == '__main__':
    tool = CalculationTool()
    tool.run()
