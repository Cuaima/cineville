from __future__ import annotations

from collections import Counter, defaultdict
from typing import Iterable
from .models import Member, MemberVisitGroup, Visit


def group_visits_by_member(
    members: Iterable[Member], visits: Iterable[Visit]
) -> list[MemberVisitGroup]:
    grouped: dict[str, list[str]] = defaultdict(list)
    for visit in visits:
        grouped[visit.barcode].append(visit.visit_id)

    result: list[MemberVisitGroup] = []
    for member in members:
        result.append(
            MemberVisitGroup(
                member_id=member.member_id,
                barcode=member.barcode,
                visit_ids=tuple(grouped.get(member.barcode, [])),
            )
        )

    return result
