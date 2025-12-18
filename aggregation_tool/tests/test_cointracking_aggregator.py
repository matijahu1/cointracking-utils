import pandas as pd
import pytest
from aggregation_tool.aggregator import CoinTrackingAggregator
from numpy import nan

@pytest.fixture
def load_csv_data(request: pytest.FixtureRequest):
    file_path = request.param
    df = pd.read_csv(file_path)
    df = df.sort_values(by=["Type", "Cur.", "Cur..1", "Cur..2", "Exchange", "Group", "Comment", "Date"])
    return df    

@pytest.fixture
def load_expected_data(request: pytest.FixtureRequest):
    file_path = request.param
    return pd.read_csv(file_path)

@pytest.mark.parametrize("load_csv_data, load_expected_data", [
    ("./aggregation_tool/data/CT-test-data1.csv", "./aggregation_tool/data/CT-test-data1-exp.csv")
    ], indirect=["load_csv_data", "load_expected_data"])
def test_csv_data1(load_csv_data: pd.DataFrame, load_expected_data: pd.DataFrame):
    # Load input data and expected data as DataFrames
    input_data = load_csv_data
    expected_data = load_expected_data
    
    aggregator = CoinTrackingAggregator()    
    result_df = aggregator.aggregate_lines(input_data)
    
    # Leere Felder in beiden DataFrames durch NaN ersetzen
    result_df = result_df.fillna(nan)
    expected_data = expected_data.fillna(nan)    
    pd.testing.assert_frame_equal(result_df, expected_data)

@pytest.mark.parametrize("load_csv_data, load_expected_data", [
    ("./aggregation_tool/data/CT-test-data2.csv", "./aggregation_tool/data/CT-test-data2-exp.csv")
    ], indirect=["load_csv_data", "load_expected_data"])
def test_csv_data2(load_csv_data: pd.DataFrame, load_expected_data: pd.DataFrame):
    # Load input data and expected data as DataFrames
    input_data = load_csv_data
    expected_data = load_expected_data
    
    aggregator = CoinTrackingAggregator()    
    result_df = aggregator.aggregate_lines(input_data)
    
    # Leere Felder in beiden DataFrames durch NaN ersetzen
    result_df = result_df.fillna(nan)
    expected_data = expected_data.fillna(nan)    
    pd.testing.assert_frame_equal(result_df, expected_data)   
    
@pytest.mark.parametrize("load_csv_data, load_expected_data", [
    ("./aggregation_tool/data/CT-test-data3.csv", "./aggregation_tool/data/CT-test-data3-exp.csv")
    ], indirect=["load_csv_data", "load_expected_data"])
def test_csv_data3(load_csv_data: pd.DataFrame, load_expected_data: pd.DataFrame):
    # Load input data and expected data as DataFrames
    input_data = load_csv_data
    expected_data = load_expected_data
    
    aggregator = CoinTrackingAggregator()    
    result_df = aggregator.aggregate_lines(input_data)
    
    # Leere Felder in beiden DataFrames durch NaN ersetzen
    result_df = result_df.fillna(nan)
    expected_data = expected_data.fillna(nan)    
    pd.testing.assert_frame_equal(result_df, expected_data) 


def test_aggregate_7_lines():    

    # CSV (Full Export) Format: "Type","Buy","Cur.","Sell","Cur.","Fee","Cur.","Exchange","Group","Comment","Date","Tx-ID"
    # Input Daten
    data = [
        {"Type": "Trade", "Buy": 0.02600000, "Cur.": "BTC", "Sell": 1000.01000000, "Cur..1": "EUR", "Fee": 1.60000000, "Cur..2": "EUR", 
        "Exchange": "Kraken", "Group": "Kraken Ledger", "Comment": "", "Date": "2021-03-01 07:00:00","Tx-ID": "1"},
        {"Type": "Trade", "Buy": 0.02500000, "Cur.": "BTC", "Sell": 900.01000000, "Cur..1": "EUR", "Fee": 1.50000000, "Cur..2": "EUR", 
        "Exchange": "Kraken", "Group": "Kraken Ledger", "Comment": "", "Date": "2021-03-02 07:00:00","Tx-ID": "2"},
        {"Type": "Trade", "Buy": 0.07500000, "Cur.": "BTC", "Sell": 2900.01000000, "Cur..1": "EUR", "Fee": 3.50000000, "Cur..2": "EUR", 
        "Exchange": "Kraken", "Group": "Kraken Ledger", "Comment": "", "Date": "2021-03-02 08:00:00","Tx-ID": "3"},
        {"Type": "Margin Fee", "Buy": "", "Cur.": "", "Sell": 2.70000000, "Cur..1": "EUR", "Fee": 0.00000000, "Cur..2": "EUR", 
        "Exchange": "Kraken", "Group": "Kraken Margin", "Comment": "", "Date": "2021-03-03 09:00:00","Tx-ID": "4"},
        {"Type": "Margin Fee", "Buy": "", "Cur.": "", "Sell": 0.10000000, "Cur..1": "EUR", "Fee": 0.00000000, "Cur..2": "EUR", 
        "Exchange": "Kraken", "Group": "Kraken Rollover", "Comment": "", "Date": "2021-03-03 13:20:00","Tx-ID": "5"}, 
        {"Type": "Margin Fee", "Buy": "", "Cur.": "", "Sell": 0.10000000, "Cur..1": "EUR", "Fee": 0.00000000, "Cur..2": "EUR", 
        "Exchange": "Kraken", "Group": "Kraken Rollover", "Comment": "", "Date": "2021-03-03 17:20:00","Tx-ID": "6"}, 
        {"Type": "Margin Fee", "Buy": "", "Cur.": "", "Sell": 0.10000000, "Cur..1": "EUR", "Fee": 0.00000000, "Cur..2": "EUR", 
        "Exchange": "Kraken", "Group": "Kraken Rollover", "Comment": "", "Date": "2021-03-03 21:20:00","Tx-ID": "7"}, 
    ]
    
    # DataFrame erstellen
    df = pd.DataFrame(data)
    
    aggregator = CoinTrackingAggregator()    
    result_df = aggregator.aggregate_lines(df)

    # Expected lines: (1), (2,3), (4), (5-7)
    assert len(result_df) == 4 
    assert result_df.iloc[0]["Type"] == "Trade"
    assert result_df.iloc[0]["Date"] == "2021-03-01 00:01:00"
    assert result_df.iloc[0]["Buy"] == round(0.026, 8)

    assert result_df.iloc[1]["Type"] == "Trade"
    assert result_df.iloc[1]["Buy"] == round(0.1, 8)

    assert result_df.iloc[2]["Type"] == "Margin Fee"
    assert result_df.iloc[2]["Group"] == "Kraken Margin"

    assert result_df.iloc[3]["Type"] == "Margin Fee"
    assert result_df.iloc[3]["Buy"] == round(0.0, 8)
    assert result_df.iloc[3]["Sell"] == round(0.3, 8)
    assert result_df.iloc[3]["Group"] == "Kraken Rollover"

