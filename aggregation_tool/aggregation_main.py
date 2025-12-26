from aggregation_tool.aggregator import AggregatorFactory
from common.config import Config
from common.data_exporter import DataExporter
from common.data_importer import DataImporter


class AggregationTool:
    def __init__(self):
        self.config = Config("./aggregation_tool/data/config.json")
        self.importer = DataImporter(self.config)
        self.aggregator = AggregatorFactory.get_aggregator(
            self.config.get_data_format()
        )
        self.exporter = DataExporter()

    def run(self):
        records = self.importer.load_data()
        aggregated_records = self.aggregator.aggregate_lines(records)
        path = self.config.get_export_file()
        self.exporter.save_raw_data(path, aggregated_records)


if __name__ == "__main__":
    tool = AggregationTool()
    tool.run()
