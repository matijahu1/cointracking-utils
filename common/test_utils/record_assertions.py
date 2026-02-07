# common/test_utils/assertions.py
from dataclasses import fields, is_dataclass
from decimal import Decimal
from enum import Enum


def assert_records_equal(actual, expected, index: int) -> None:
    """
    Detailed comparison with Enum handling and numeric tolerance.
    """
    if not is_dataclass(actual):
        assert actual == expected, f"Record {index} mismatch: {actual} != {expected}"
        return

    for field in fields(actual):
        field_name = field.name
        val_actual = getattr(actual, field_name)
        val_expected = getattr(expected, field_name)

        # 1. Enum-Handling
        cmp_actual = val_actual.name if isinstance(val_actual, Enum) else val_actual
        cmp_expected = (
            val_expected.name if isinstance(val_expected, Enum) else val_expected
        )

        # 2. Numerisches Handling (Toleranz für Rundungsdifferenzen)
        if isinstance(cmp_actual, (Decimal, float)) and isinstance(
            cmp_expected, (Decimal, float)
        ):
            # Wir prüfen, ob die Differenz kleiner als eine winzige Schwelle ist
            tolerance = Decimal("0.0000000001")
            is_equal = (
                abs(Decimal(str(cmp_actual)) - Decimal(str(cmp_expected))) < tolerance
            )
        else:
            is_equal = cmp_actual == cmp_expected

        assert is_equal, (
            f"Record {index} mismatch in field '{field_name}':\n"
            f"   Actual:   {val_actual}\n"
            f"   Expected: {val_expected}"
        )
