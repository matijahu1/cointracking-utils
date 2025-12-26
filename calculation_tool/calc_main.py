from calculation_tool.calculator import Calculator
from common.config import Config
from common.data_exporter import DataExporter
from common.data_importer import DataImporter


class CalculationTool:
    def __init__(self):
        self.config = Config("./calculation_tool/data/config.json")
        self.importer = DataImporter(self.config, check_coin=True)
        self.calculator = Calculator(self.config)
        self.exporter = DataExporter()

    def run(self):
        records = self.importer.load_data()
        target_records = self.calculator.track_balance(records)
        path = self.config.get_export_file()
        self.exporter.save_target_data(path, target_records)


if __name__ == "__main__":
    tool = CalculationTool()
    tool.run()
