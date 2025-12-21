import os

import pandas as pd
import pytest

from calculation_tool.calculator import Calculator
from common.config import ConfigProtocol
from common.mappers import (
    dataframe_to_raw_records,
    dataframe_to_target_records,
    normalize_ct_columns,
)
from tests.mocks.mock_config import MockConfig


@pytest.fixture
def load_ct_dataframe(request: pytest.FixtureRequest):
    file_path = request.param
    df = pd.read_csv(file_path)
    df = df.sort_values(
        by=["Type", "Cur.", "Cur..1", "Cur..2", "Exchange", "Group", "Comment", "Date"]
    )
    return normalize_ct_columns(df)


@pytest.fixture
def load_expected_data(request: pytest.FixtureRequest, mock_config: MockConfig):
    file_path = request.param
    df = pd.read_csv(file_path)
    return dataframe_to_target_records(df, mock_config)


@pytest.fixture
def mock_config() -> MockConfig:
    return MockConfig()


@pytest.mark.parametrize(
    "load_ct_dataframe, load_expected_data",
    [
        (
            "./calculation_tool/data/test-ADA-1.csv",
            "./calculation_tool/data/test-ADA-1-exp.csv",
        )
    ],
    indirect=["load_ct_dataframe", "load_expected_data"],
)
@pytest.mark.skipif(
    not os.path.exists("./calculation_tool/data/test-ADA-1.csv"),
    reason="Local test data not found. Please place your CSV in /data to run this test.",
)
def test_csv_data1(
    load_ct_dataframe: pd.DataFrame,
    load_expected_data: pd.DataFrame,
    mock_config: ConfigProtocol,
):
    # Load input data and expected data as DataFrames
    input_ct_data = load_ct_dataframe

    expected_records = load_expected_data

    input_records = dataframe_to_raw_records(input_ct_data, mock_config)

    calculator = Calculator(mock_config)
    result_records = calculator.track_balance(input_records)

    assert len(result_records) == len(expected_records)
    assert result_records[0].balance == expected_records[0].balance
