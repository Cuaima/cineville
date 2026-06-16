from __future__ import annotations

import csv
import json
from pathlib import Path
from .models import MemberVisitGroup


def write_member_visit_groups(path: Path, groups: list[MemberVisitGroup]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(
            csv_file, fieldnames=["member_id", "barcode", "visit_ids"]
        )
        writer.writeheader()
        for group in groups:
            writer.writerow(
                {
                    "member_id": group.member_id,
                    "barcode": group.barcode,
                    # Use JSON array serialization so visit_ids are written as
                    # [visit_id1, visit_id2, ...], matching the assignment format.
                    "visit_ids": json.dumps(group.visit_ids, ensure_ascii=False),
                }
            )
