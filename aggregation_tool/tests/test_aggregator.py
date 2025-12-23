import os

import pytest

from aggregation_tool.aggregator import CoinTrackingAggregator
from common.data_importer import DataImporter
from common.test_utils.run_tool_test import run_csv_based_tool_test
from common.utils.helper import sort_raw_records
from tests.mocks.mock_config import MockConfig


@pytest.mark.parametrize(
    "input_file, expected_file, config_params",
    [
        (
            "./aggregation_tool/data/CT-test-data1.csv",
            "./aggregation_tool/data/CT-test-data1-exp.csv",
            {},
        ),
        (
            "./aggregation_tool/data/CT-test-data2.csv",
            "./aggregation_tool/data/CT-test-data2-exp.csv",
            {},
        ),
        (
            "./aggregation_tool/data/CT-test-data3.csv",
            "./aggregation_tool/data/CT-test-data3-exp.csv",
            {},
        ),
        (
            "./aggregation_tool/data/CT-test-data4.csv",
            "./aggregation_tool/data/CT-test-data4-exp.csv",
            {"ct_exchanges": ["Bake", "Bake Staked"]},
        ),
    ],
)
def test_aggregator_csv(input_file, expected_file, config_params):
    # 1. Skip if files are missing (Clean Code: keeps test output tidy)
    if not os.path.exists(input_file) or not os.path.exists(expected_file):
        pytest.skip(f"Test data missing: {input_file} or {expected_file}")

    # 2. Create the mock config from params
    mock_config = MockConfig(**config_params)

    # 3. Run the tool test
    run_csv_based_tool_test(
        input_file,
        expected_file,
        # We pass the mock_config to the Aggregator here
        run_tool=lambda records: CoinTrackingAggregator(mock_config).aggregate_lines(
            records
        ),
        load_input=DataImporter.parse_csv_file,
        load_expected=DataImporter.parse_csv_file,
        sort_result=sort_raw_records,
    )
