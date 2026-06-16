from __future__ import annotations

from collections import Counter
from typing import Iterable
from .models import Member, Visit


def count_walk_ins(visits: Iterable[Visit]) -> int:
    return sum(1 for visit in visits if not visit.reservation_id)


def top_n_members(
    visits: Iterable[Visit], members_by_barcode: dict[str, Member], n: int = 5
) -> list[tuple[Member, int]]:
    counts = Counter(visit.barcode for visit in visits)
    top: list[tuple[Member, int]] = []
    for barcode, count in counts.most_common(n):
        member = members_by_barcode.get(barcode)
        if member is not None:
            top.append((member, count))
    return top
