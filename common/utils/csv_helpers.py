import csv
from pathlib import Path


def read_ct_csv(path: str) -> list[list[str]]:
    rows: list[list[str]] = []

    with open(Path(path), newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        next(reader)  # skip header

        for row in reader:
            if row:
                rows.append(row)

    return rows
