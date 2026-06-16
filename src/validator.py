"""Validate visits against known members and data quality rules."""

from __future__ import annotations

import logging
from typing import Iterable
from .models import Member, Visit

logger = logging.getLogger(__name__)


def filter_valid_visits(
    visits: Iterable[Visit], members_by_barcode: dict[str, Member]
) -> list[Visit]:
    """Return visits that are structurally valid and refer to known members.

    This function performs two checks for each visit:
    1. The visit has a non-empty `barcode` value.
    2. The `barcode` exists in the provided `members_by_barcode` mapping.

    Visits failing either check are dropped and a warning is logged. The
    function returns a list of visits that passed both checks.
    """

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
