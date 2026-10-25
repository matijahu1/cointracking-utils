import json
from dataclasses import replace
from datetime import datetime, timedelta
from decimal import Decimal

import pytest

from aggregation_tool.aggregation_main import AggregationTool
from aggregation_tool.transfer_pairs import remove_matching_transfer_pairs
from common.config import Config
from common.data_exporter import DataExporter
from common.data_importer import DataImporter
from common.models.records import RawRecord


def deposit():
    return RawRecord(
        type="Deposit", buy_amount=Decimal("1.25"), buy_currency="BTC",
        sell_amount=Decimal("0"), sell_currency="", fee_amount=Decimal("0"),
        fee_currency="", exchange="Bybit", group="", comment="original",
        datetime=datetime(2025, 1, 1, 12), lpn="1", tx_id="deposit-id",
    )


def withdrawal():
    return replace(
        deposit(), type="Withdrawal", buy_amount=Decimal("0"), buy_currency="",
        sell_amount=Decimal("1.250"), sell_currency="BTC", tx_id="withdrawal-id",
    )


@pytest.mark.parametrize("reverse", [False, True])
def test_pairs_are_removed_once_and_original_records_preserved(reverse):
    first, second = deposit(), withdrawal()
    records = [first, first, second]
    if reverse:
        records.reverse()
    remaining, removed = remove_matching_transfer_pairs(records)
    assert len(remaining) == 1
    assert remaining[0] is first
    assert len(removed) == 2
    assert any(r is second for r in removed)
    assert len(records) == 3


@pytest.mark.parametrize("changes", [
    {"datetime": deposit().datetime + timedelta(seconds=1)},
    {"exchange": "Kraken"}, {"sell_currency": "ETH"},
    {"sell_amount": Decimal("1.2500000001")},
    {"fee_amount": Decimal("0.01")}, {"buy_amount": Decimal("1")},
    {"type": "Trade"},
])
def test_near_matches_are_retained(changes):
    records = [deposit(), replace(withdrawal(), **changes)]
    remaining, removed = remove_matching_transfer_pairs(records)
    assert len(remaining) == 2
    assert removed == []


@pytest.mark.parametrize("changes", [
    {"fee_amount": Decimal("0.01")}, {"exchange": ""},
    {"buy_amount": Decimal("0")}, {"buy_amount": Decimal("-1.25")},
    {"buy_currency": ""}, {"sell_amount": Decimal("1")},
])
def test_ineligible_deposits_are_retained(changes):
    remaining, removed = remove_matching_transfer_pairs([
        replace(deposit(), **changes), withdrawal(),
    ])
    assert len(remaining) == 2
    assert removed == []


@pytest.mark.parametrize("enabled", [True, False, None])
def test_tool_export_and_optional_audit(tmp_path, monkeypatch, enabled):
    monkeypatch.chdir(tmp_path)
    data = tmp_path / "aggregation_tool" / "data"
    data.mkdir(parents=True)
    source, output = data / "input.csv", data / "output.csv"
    extra = replace(deposit(), buy_amount=Decimal("2"), tx_id="unmatched")
    DataExporter().save_raw_data(source, [deposit(), withdrawal(), extra])
    settings = {
        "import_file": str(source), "export_file": str(output),
        "data_format": "CoinTracking", "coin": "",
    }
    if enabled is not None:
        settings["remove_matching_transfer_pairs"] = enabled
    (data / "config.json").write_text(json.dumps(settings), encoding="utf-8")
    AggregationTool().run()
    result = DataImporter.parse_csv_file(str(output))
    audit = data / "output-removed-transfer-pairs.csv"
    if enabled:
        assert len(result) == 1
        assert result[0].tx_id == "unmatched"
        removed = DataImporter.parse_csv_file(str(audit))
        assert [r.tx_id for r in removed] == ["deposit-id", "withdrawal-id"]
    else:
        assert len(result) == 2
        assert not audit.exists()


def test_invalid_option_is_rejected(tmp_path):
    path = tmp_path / "config.json"
    path.write_text('{"remove_matching_transfer_pairs": "false"}')
    with pytest.raises(ValueError, match="must be a boolean"):
        Config(str(path)).get_remove_matching_transfer_pairs()


def test_empty_input():
    assert remove_matching_transfer_pairs([]) == ([], [])
