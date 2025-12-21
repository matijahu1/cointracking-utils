import os

import pytest

from aggregation_tool.tests.utils.aggregator_helpers import run_aggregator_test
from tests.mocks.mock_config import MockConfig


@pytest.fixture
def mock_config() -> MockConfig:
    return MockConfig()


@pytest.mark.parametrize(
    "input_file, expected_file",
    [
        (
            "./aggregation_tool/data/CT-test-data1.csv",
            "./aggregation_tool/data/CT-test-data1-exp.csv",
        ),
        (
            "./aggregation_tool/data/CT-test-data2.csv",
            "./aggregation_tool/data/CT-test-data2-exp.csv",
        ),
        (
            "./aggregation_tool/data/CT-test-data3.csv",
            "./aggregation_tool/data/CT-test-data3-exp.csv",
        ),
        (
            "./aggregation_tool/data/CT-test-data4.csv",
            "./aggregation_tool/data/CT-test-data4-exp.csv",
        ),
    ],
)
def test_csv_data(input_file, expected_file, mock_config):
    if not os.path.exists(input_file):
        pytest.skip(
            f"\n[INFO] Skipping test: {input_file} not found. Create local data to run this."
        )

    if not os.path.exists(expected_file):
        pytest.skip(
            f"\n[INFO] Skipping test: {expected_file} not found. Create local data to run this."
        )

    run_aggregator_test(input_file, expected_file, mock_config)
