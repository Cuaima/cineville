from __future__ import annotations

import logging
from typing import Iterable
from .models import Member, Visit

logger = logging.getLogger(__name__)


def filter_valid_visits(
    visits: Iterable[Visit], members_by_barcode: dict[str, Member]
) -> list[Visit]:
    valid_visits: list[Visit] = []
    for visit in visits:
        if not visit.barcode:
            logger.warning(
                "Dropping visit %s: missing barcode", visit.visit_id or "<unknown>"
            )
            continue
        if visit.barcode not in members_by_barcode:
            logger.warning(
                "Dropping visit %s: barcode %s not found in members.csv",
                visit.visit_id or "<unknown>",
                visit.barcode,
            )
            continue
        valid_visits.append(visit)
    return valid_visits
