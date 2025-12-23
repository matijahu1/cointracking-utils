# common/test_utils/assertions.py
from dataclasses import fields, is_dataclass


def assert_records_equal(actual, expected, index: int) -> None:
    """
    Detailed comparison of two dataclass records with field-level error reporting.
    """
    if not is_dataclass(actual):
        assert actual == expected, f"Record {index} mismatch: {actual} != {expected}"
        return

    # Iterate over all fields defined in the dataclass
    for field in fields(actual):
        field_name = field.name
        val_actual = getattr(actual, field_name)
        val_expected = getattr(expected, field_name)

        assert val_actual == val_expected, (
            f"Record {index} mismatch in field '{field_name}':\n"
            f"  Actual:   {val_actual}\n"
            f"  Expected: {val_expected}"
        )
