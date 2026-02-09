from decimal import Decimal
from typing import Dict, List, Tuple

from common.models.records import PnLResult, RawRecord

from .pnl_models import AssetLot, OpenLot, PositionSide


class PnLEngine:
    def __init__(self, config):
        self.config = config
        self.method = config.get_accounting_method()  # "LIFO" or "FIFO"
        self.coin = config.get_coin()
        self.curr = config.get_currency()
        # Stores lists of AssetLot objects per coin: { "HYPE": [Lot1, Lot2] }
        self.open_lots: Dict[str, List[AssetLot]] = {}
        self.pnl_results: List[PnLResult] = []

    def calculate(self, records: list) -> Tuple[List[PnLResult], List[OpenLot]]:
        """
        Processes all records chronologically.
        Includes guard clauses for robustness and handles fees.
        """
        # Ensure chronological order for correct lot building
        records.sort(key=lambda x: x.datetime)

        for record in records:
            # Guard Clause: Skip irrelevant records (Safety for Unit Tests)
            if self.coin not in (record.buy_currency, record.sell_currency):
                continue

            if self.curr not in (record.buy_currency, record.sell_currency):
                continue

            # Process only Trade type for now
            if record.type != "Trade":
                continue

            new_pnl_events = self._match_trade_against_lots(record)
            self.pnl_results.extend(new_pnl_events)

        return self.pnl_results, self._get_all_open_lots()

    def _match_trade_against_lots(self, record) -> list[PnLResult]:
        """
        Matches a trade record against current open lots to determine PnL.

        This method implements the core matching logic:
        1. It identifies if the trade closes existing positions (Short vs. Long).
        2. It updates 'self.open_lots' by consuming matched lots or adding new ones.
        3. It calculates PnL for every closed lot (or partial lot).

        Args:
            record: The trade record to be processed.

        Returns:
            A list of PnLResult objects for each lot that was closed during
            this trade. Returns an empty list if no lots were closed (e.g.,
            when only opening a new position).
        """

        is_buy = record.buy_currency == self.coin
        incoming_amount = record.buy_amount if is_buy else record.sell_amount
        price = self._calculate_current_price(record, is_buy)

        # Referenz auf die OpenLots des Coins holen
        if self.coin not in self.open_lots:
            self.open_lots[self.coin] = []
        active_lots = self.open_lots[self.coin]

        # Bestehende Lots schließen (Matching)
        pnl_results, remaining_amount = self._close_opposing_lots(
            record, incoming_amount, price, is_buy, active_lots
        )

        # Restbetrag als neues Lot eröffnen (Opening)
        if remaining_amount > 0:
            self._open_new_lot(record, remaining_amount, price, is_buy, active_lots)

        return pnl_results

    def _calculate_pnl(
        self, side: PositionSide, amount: Decimal, open_p: Decimal, close_p: Decimal
    ) -> Decimal:
        """
        Profit calculation:
        Long:  (Close - Open) * Amount
        Short: (Open - Close) * Amount
        """
        if side == PositionSide.LONG:
            return (close_p - open_p) * amount
        else:
            return (open_p - close_p) * amount

    def _get_all_open_lots(self) -> List[OpenLot]:
        """Collects remaining lots for the secondary CSV report."""
        reports = []
        for coin, lots in self.open_lots.items():
            for lot in lots:
                reports.append(
                    OpenLot(
                        coin=coin,
                        side=lot.side.name,
                        open_datetime=lot.open_datetime,
                        remaining_amount=lot.remaining_amount,
                        open_price=lot.open_price,
                        currency=lot.currency,
                        total_value_at_open=lot.remaining_amount * lot.open_price,
                    )
                )
        return reports

    def _calculate_current_price(self, record, is_buy: bool):
        return (
            record.sell_amount / record.buy_amount
            if is_buy
            else record.buy_amount / record.sell_amount
        )

    def _close_opposing_lots(
        self,
        record: RawRecord,
        amount: Decimal,
        price: Decimal,
        is_buy: bool,
        active_lots: List[AssetLot],
    ) -> Tuple[List[PnLResult], Decimal]:
        """Sucht Gegenseiten und berechnet PnL."""
        results = []
        needed_side = PositionSide.SHORT if is_buy else PositionSide.LONG
        amount_to_process = amount

        while amount_to_process > 0 and active_lots:
            idx = -1 if self.method == "LIFO" else 0
            if active_lots[idx].side != needed_side:
                break

            current_lot = active_lots[idx]
            match_amount = min(amount_to_process, current_lot.remaining_amount)

            # PnL erzeugen
            results.append(
                self._create_pnl_result(record, current_lot, match_amount, price)
            )

            # Beträge reduzieren
            current_lot.remaining_amount -= match_amount
            amount_to_process -= match_amount

            if current_lot.remaining_amount <= 0:
                active_lots.pop(idx)

        return results, amount_to_process

    def _open_new_lot(
        self,
        record: RawRecord,
        amount: Decimal,
        price: Decimal,
        is_buy: bool,
        active_lots: List[AssetLot],
    ) -> None:
        """Erstellt ein neues AssetLot und fügt es der Liste hinzu."""
        new_side = PositionSide.LONG if is_buy else PositionSide.SHORT
        new_lot = AssetLot(
            coin=self.coin,
            side=new_side,
            open_datetime=record.datetime,
            amount=amount,
            remaining_amount=amount,
            open_price=price,
            currency=record.sell_currency if is_buy else record.buy_currency,
        )
        active_lots.append(new_lot)

    def _create_pnl_result(
        self, record: RawRecord, lot: AssetLot, amount: Decimal, close_price: Decimal
    ) -> PnLResult:
        """Hilfsmethode zur Kapselung der PnLResult-Erstellung."""
        return PnLResult(
            coin=self.coin,
            side=lot.side,  # Wir speichern das Enum-Objekt
            open_datetime=lot.open_datetime,
            close_datetime=record.datetime,
            amount=amount,
            open_price=lot.open_price,
            close_price=close_price,
            currency=record.sell_currency
            if record.buy_currency == self.coin
            else record.buy_currency,
            pnl=self._calculate_pnl(lot.side, amount, lot.open_price, close_price),
            method=self.method,
        )
