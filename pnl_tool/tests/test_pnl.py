import os

import pytest

from common.data_importer import DataImporter
from common.test_utils.mock_config import MockConfig
from common.test_utils.run_tool_test import run_csv_based_tool_test
from pnl_tool.pnl_engine import PnLEngine


@pytest.mark.parametrize(
    "input_file, expected_file, config_params",
    [
        (
            "./pnl_tool/data/FewLines.csv",
            "./pnl_tool/data/PnL_ADA-EUR-LIFO-Few.csv",
            {"coin": "ADA", "currency": "EUR", "accounting_method": "LIFO"},
        ),
    ],
)
def test_pnl_engine_csv(input_file, expected_file, config_params):
    """
    Test the PnL engine using CSV files and automated record comparison.
    """
    # 1. Skip if test data is missing
    if not os.path.exists(input_file) or not os.path.exists(expected_file):
        pytest.skip(f"Test data missing: {input_file} or {expected_file}")

    # 2. Setup mock config
    # Ensure MockConfig can handle 'symbol' and 'accounting_method'
    mock_config = MockConfig(**config_params)

    # 3. Define the tool execution for the generic runner
    def run_pnl_logic(records):
        engine = PnLEngine(mock_config)
        pnl_results, _ = engine.calculate(records)
        return pnl_results

    # 4. Use the generic test runner
    run_csv_based_tool_test(
        input_file=input_file,
        expected_file=expected_file,
        run_tool=run_pnl_logic,
        # Load input as raw records
        load_input=DataImporter.parse_csv_file,
        load_expected=DataImporter.parse_pnl_result_csv_file,
        # Optional: sorting if order in CSV is not guaranteed
        sort_result=lambda x: sorted(
            x, key=lambda r: (r.close_datetime, r.open_datetime)
        ),
    )
