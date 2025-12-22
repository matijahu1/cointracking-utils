class MockConfig:
    def __init__(
        self,
        coin: str = "",
        decimal_separator: str = ".",
        date_format: str = "%Y-%m-%d %H:%M:%S",
        ct_exchanges: list[str] = [],
    ):
        self._coin = coin
        self._decimal_separator = decimal_separator
        self._date_format = date_format
        self._ct_exchanges = ct_exchanges

    def get_coin(self) -> str:
        return self._coin

    def get_decimal_separator(self) -> str:
        return self._decimal_separator

    def get_date_format(self) -> str:
        return self._date_format

    def get_ct_exchanges(self) -> list[str]:
        return self._ct_exchanges
