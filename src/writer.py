"""Write grouped member visits to CSV."""

from __future__ import annotations

import csv
import json
import logging
from pathlib import Path
from .models import MemberVisitGroup


def write_member_visit_groups(path: Path, groups: list[MemberVisitGroup]) -> None:
    """Write grouped member visits to CSV.

    The output CSV has columns: `member_id`, `barcode`, and `visit_ids`.
    `visit_ids` is serialized as a JSON array (e.g. `["v1", "v2"]`) so it
    remains machine-readable when embedded in a single CSV cell and can be
    parsed by downstream tools without ambiguity.
    """

    path.parent.mkdir(parents=True, exist_ok=True)
    try:
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
                        "visit_ids": json.dumps(group.visit_ids, ensure_ascii=False),
                    }
                )
    except OSError as error:
        logging.error("Could not write output file %s: %s", path, error)
        raise
