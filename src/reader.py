from __future__ import annotations

import csv
import logging
from pathlib import Path

from .models import Member, Visit

logger = logging.getLogger(__name__)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        return [row for row in reader]


def load_members(path: Path) -> tuple[list[Member], dict[str, Member]]:
    rows = read_csv_rows(path)
    missing = [
        row for row in rows if not row.get("barcode") or not row.get("member_id")
    ]
    if missing:
        raise ValueError("members.csv must include member_id and barcode on every row")

    members: list[Member] = []
    barcode_index: dict[str, Member] = {}
    for row in rows:
        barcode = row["barcode"].strip()
        member = Member(member_id=row["member_id"].strip(), barcode=barcode)
        if barcode in barcode_index:
            logger.warning(
                "Skipping duplicate member barcode %s in members.csv", barcode
            )
            continue
        members.append(member)
        barcode_index[barcode] = member

    return members, barcode_index


def load_visits(path: Path) -> list[Visit]:
    rows = read_csv_rows(path)
    visits: list[Visit] = []
    for row in rows:
        visit_id = row.get("visit_id", "").strip()
        barcode = row.get("barcode", "").strip()
        reservation_id = row.get("reservation_id")
        reservation_id = reservation_id.strip() if reservation_id is not None else None
        visits.append(
            Visit(visit_id=visit_id, barcode=barcode, reservation_id=reservation_id)
        )

    return visits
