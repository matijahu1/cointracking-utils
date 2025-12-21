from common.config import Config
from aggregation_tool.aggregator import *
from common.data_importer import DataImporter
from common.data_exporter import DataExporter
from common.mappers import dataframe_to_raw_records, raw_records_to_dataframe

class AggregationTool:
    def __init__(self):
        self.config = Config('./aggregation_tool/data/config.json')
        self.importer = DataImporter(self.config)
        self.aggregator = AggregatorFactory.get_aggregator(self.config.get_data_format())
        self.exporter = DataExporter(self.config)

    def run(self):        
        records = self.importer.load_data()
        aggregated_records = self.aggregator.aggregate_lines(records)
        self.exporter.save_data(aggregated_records)      

if __name__ == '__main__':
    tool = AggregationTool()
    tool.run()
