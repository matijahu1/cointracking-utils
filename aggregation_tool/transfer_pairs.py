from collections import defaultdict, deque

from common.models.records import RawRecord


def remove_matching_transfer_pairs(
    records: list[RawRecord],
) -> tuple[list[RawRecord], list[RawRecord]]:
    """Remove one-to-one Deposit/Withdrawal pairs before daily aggregation.

    Match timestamps within the same calendar minute, with exact exchanges,
    currencies and Decimal amounts.
    Only positive, fee-free, single-sided transfers with a known exchange and
    currency qualify. Group, comment and transaction IDs need not match.
    Both returned lists retain input order and the original records.
    """
    pending = defaultdict(deque)
    removed_indices: set[int] = set()
    for index, record in enumerate(records):
        if record.fee_amount != 0 or not record.exchange:
            continue
        if record.type == "Deposit" and record.sell_amount == 0:
            amount, currency = record.buy_amount, record.buy_currency
            opposite = "Withdrawal"
        elif record.type == "Withdrawal" and record.buy_amount == 0:
            amount, currency = record.sell_amount, record.sell_currency
            opposite = "Deposit"
        else:
            continue
        if amount <= 0 or not currency:
            continue

        minute = record.datetime.replace(second=0, microsecond=0)
        key = (minute, record.exchange, currency, amount)
        matches = pending[(opposite, key)]
        if matches:
            removed_indices.update((matches.popleft(), index))
        else:
            pending[(record.type, key)].append(index)

    remaining = [r for i, r in enumerate(records) if i not in removed_indices]
    removed = [r for i, r in enumerate(records) if i in removed_indices]
    return remaining, removed
