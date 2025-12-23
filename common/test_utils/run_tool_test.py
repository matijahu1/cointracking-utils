from typing import Callable, Optional, TypeVar

from common.test_utils.record_assertions import assert_records_equal

TInput = TypeVar("TInput")
TOutput = TypeVar("TOutput")


def run_csv_based_tool_test(
    input_file: str,
    expected_file: str,
    run_tool: Callable[[list[TInput]], list[TOutput]],
    load_input: Callable[[str], list[TInput]],
    load_expected: Callable[[str], list[TOutput]],
    sort_result: Optional[Callable[[list[TOutput]], None]] = None,
) -> None:
    # ... (Loading and Running as before) ...
    input_records = load_input(input_file)
    expected_records = load_expected(expected_file)
    result_records = run_tool(input_records)

    if sort_result:
        sort_result(result_records)
        sort_result(expected_records)

    # 1. Compare length
    assert len(result_records) == len(expected_records), (
        f"Number of records mismatch: {len(result_records)} != {len(expected_records)}"
    )

    # 2. Compare records using your detailed helper
    for i, (res, exp) in enumerate(zip(result_records, expected_records)):
        # Instead of generic 'assert res == exp', we use your helper:
        assert_records_equal(res, exp, i)
