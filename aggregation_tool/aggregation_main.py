import pandas as pd
from common.config import Config
from aggregation_tool.aggregator import *
from common.data_importer import DataImporter
from common.data_exporter import DataExporter

class AggregationTool:
    def __init__(self):
        self.config = Config('./aggregation_tool/data/config.json')
        self.importer = DataImporter(self.config)
        self.aggregator = AggregatorFactory.get_aggregator(self.config.get_data_format())
        self.exporter = DataExporter(self.config)

    def run(self):
        df = self.importer.load_data()        
        aggregated_df = self.aggregator.aggregate_lines(df)
        
        self.exporter.save_data(aggregated_df)

if __name__ == '__main__':
    tool = AggregationTool()
    tool.run()
