from common.config import Config
from common.data_exporter import DataExporter
from common.data_importer import DataImporter
from pnl_tool.pnl_engine import PnLEngine


class PnLTool:
    def __init__(self):
        self.config = Config("./pnl_tool/data/config.json")
        self.importer = DataImporter(self.config, coin_filtering_enabled=True)
        self.engine = PnLEngine(self.config)
        self.exporter = DataExporter()

    def run(self):
        # 1. Load and filter records (only for the specific coin and exchange)
        records = self.importer.load_data()

        # 2. Calculate PnL Matches and Open Lots
        # The engine will return two sets of data
        pnl_results, open_lots = self.engine.calculate(records)

        # 3. Export PnL Report
        pnl_path = self.config.get_pnl_export_file()
        self.exporter.save_pnl_results(pnl_path, pnl_results)

        # 4. Export Open Lots Report
        open_lots_path = self.config.get_open_lots_export_file()
        self.exporter.save_open_lots(open_lots_path, open_lots)


if __name__ == "__main__":
    tool = PnLTool()
    tool.run()
