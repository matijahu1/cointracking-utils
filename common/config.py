import json
import sys
from pathlib import Path
from typing import Any, Protocol


class ConfigProtocol(Protocol):
    def get_coin(self) -> str: ...
    def get_currency(self) -> str: ...
    def get_decimal_separator(self) -> str: ...
    def get_date_format(self) -> str: ...
    def get_ct_exchanges(self) -> list[str]: ...


class Config:
    def __init__(self, config_file: str):
        self.config_data: dict[str, Any]
        self.config_data = self._load_config(config_file)

    def _load_config(self, config_file):
        try:
            with open(config_file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Error: Config file '{config_file}' not found. Exiting program.")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"Config file '{config_file}' contains invalid JSON.")
            sys.exit(1)

    def get_import_file(self):
        return self.config_data.get("import_file")

    def get_data_format(self) -> str:
        return self.config_data.get("data_format", "")

    def get_ct_exchanges(self) -> list[str]:
        value = self.config_data.get("ct_exchanges")

        if isinstance(value, list):
            return value

        if isinstance(value, str) and value:  # Return string as list
            return [value]

        return []

    def get_ct_year(self):
        return self.config_data.get("ct_year")

    def get_export_file(self) -> Path:
        """
        Returns the export file path as a Path object.
        """
        path_str = self.config_data.get("export_file", "")
        return Path(path_str)

    def get_pnl_export_file(self) -> Path:
        """
        Returns the export file path as a Path object.
        """
        path_str = self.config_data.get("export_pnl_file", "")
        return Path(path_str)

    def get_open_lots_export_file(self) -> Path:
        """
        Returns the export file path as a Path object.
        """
        path_str = self.config_data.get("export_open_lots_file", "")
        return Path(path_str)

    def get_coin(self) -> str:
        coin = self.config_data.get("coin")
        if coin is None:
            raise ValueError("Config value 'coin' is required")
        return coin

    def get_decimal_separator(self):
        return self.config_data.get("decimal_separator", ".")

    def get_date_format(self):
        return self.config_data.get("date_format", "%Y-%m-%d %H:%M:%S")

    def get_accounting_method(self) -> str:
        return self.config_data.get("accounting_method", "")

    def get_currency(self) -> str:
        return self.config_data.get("currency", "")

    # def get_aggregate_trades(self):
    #     return self.config_data.get("aggregate_trades")
