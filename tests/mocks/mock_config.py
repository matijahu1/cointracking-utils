from common.config import Config  # oder Protocol, falls du es benutzt

class MockConfig:
    def get_coin(self) -> str:
        return "ADA"

    def get_decimal_separator(self) -> str:
        return "."

    def get_date_format(self) -> str:
        return "%Y-%m-%d %H:%M:%S"
