from pathlib import Path

from aggregation_tool.aggregator import AggregatorFactory
from aggregation_tool.transfer_pairs import remove_matching_transfer_pairs
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
        if self.config.get_remove_matching_transfer_pairs():
            audit_path = self.config.get_removed_transfer_pairs_file()
            if audit_path.resolve() == Path(self.config.get_import_file()).resolve():
                raise ValueError("The transfer pair audit file must not overwrite the input file")
            records, removed = remove_matching_transfer_pairs(records)
            self.exporter.save_raw_data(audit_path, removed)
            print(f"Removed {len(removed) // 2} transfer pairs ({len(removed)} records). Audit: {audit_path}")
        aggregated_records = self.aggregator.aggregate_lines(records)
        path = self.config.get_export_file()
        self.exporter.save_raw_data(path, aggregated_records)


if __name__ == "__main__":
    tool = AggregationTool()
    tool.run()
