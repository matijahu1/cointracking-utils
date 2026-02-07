import os

import pytest

from calculation_tool.calculator import Calculator
from common.data_importer import DataImporter
from common.test_utils.mock_config import MockConfig
from common.test_utils.run_tool_test import run_csv_based_tool_test
from common.utils.helper import sort_target_records


@pytest.mark.parametrize(
    "input_file, expected_file, config_params",
    [
        (
            "./calculation_tool/data/test-ADA-1.csv",
            "./calculation_tool/data/test-ADA-1-exp.csv",
            {"coin": "ADA"},
        ),
        # Example for another test case with different settings:
        # (
        #     "./calculation_tool/data/test-BTC-1.csv",
        #     "./calculation_tool/data/test-BTC-1-exp.csv",
        #     {"coin": "BTC", "decimal_separator": ","}
        # ),
    ],
)
def test_calculator_csv(input_file, expected_file, config_params):
    """
    Test the calculator using CSV files and automated record comparison.
    """
    # 1. Skip if local test data is missing
    if not os.path.exists(input_file) or not os.path.exists(expected_file):
        pytest.skip(f"Test data missing: {input_file} or {expected_file}")

    # 2. Create the mock config using dictionary unpacking (**)
    # This maps 'coin' from the dict to the 'coin' parameter in __init__
    mock_config = MockConfig(**config_params)

    # 3. Use the generic test runner
    run_csv_based_tool_test(
        input_file=input_file,
        expected_file=expected_file,
        # Inject the config into the Calculator
        run_tool=lambda records: Calculator(mock_config).track_balance(records),
        load_input=DataImporter.parse_csv_file,
        load_expected=DataImporter.parse_target_csv_file,
        sort_result=sort_target_records,
    )
