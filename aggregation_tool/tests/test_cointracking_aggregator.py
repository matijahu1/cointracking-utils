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
    ],
)
def test_csv_data(input_file, expected_file, mock_config):
    run_aggregator_test(input_file, expected_file, mock_config)
