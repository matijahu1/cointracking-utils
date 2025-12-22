from aggregation_tool.aggregator import CoinTrackingAggregator
from common.data_importer import DataImporter
from common.models import RawRecord
from common.utils.helper import sort_raw_records


def run_aggregator_test(input_file: str, expected_file: str, config) -> None:
    """
    Runs the CoinTrackingAggregator on input CSV and compares the result
    against the expected CSV.

    Args:
        input_file: path to CSV with input data
        expected_file: path to CSV with expected results
        config: config object or mock
    """
    # Load CSVs
    input_records = DataImporter.parse_csv_file(input_file)
    expected_records = DataImporter.parse_csv_file(expected_file)

    # Run aggregation
    aggregator = CoinTrackingAggregator()
    result_records = aggregator.aggregate_lines(input_records)
    sort_raw_records(result_records)

    # Compare results
    assert len(result_records) == len(expected_records), (
        f"Number of records mismatch: {len(result_records)} != {len(expected_records)}"
    )

    # Compare field by field
    for i, (res, exp) in enumerate(zip(result_records, expected_records)):
        for field in RawRecord.__dataclass_fields__:
            val_res = getattr(res, field)
            val_exp = getattr(exp, field)
            assert val_res == val_exp, (
                f"Record {i} field '{field}' mismatch: {val_res} != {val_exp}"
            )
