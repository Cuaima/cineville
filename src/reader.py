"""Load members and visits from CSV files."""

from __future__ import annotations

import csv
import logging
from pathlib import Path

from .models import Member, Visit

logger = logging.getLogger(__name__)

MEMBER_REQUIRED_FIELDS = ("member_id", "barcode")
VISIT_REQUIRED_FIELDS = ("visit_id", "barcode")


def validate_row(
    row: dict[str, str],
    row_name: str,
    required_fields: tuple[str, ...],
    row_id_field: str | None = None,
 ) -> bool:
    """Check that a CSV row contains the required fields.

    Parameters
    - row: the parsed CSV row as a mapping of column -> value
    - row_name: human friendly name used in log messages (e.g. "visit")
    - required_fields: sequence of field names that must be present and non-empty
    - row_id_field: optional column name whose value should be included in
      log messages when available (for better context)

    Returns
    - True when the row contains all required non-empty fields, False when
      any required field is missing or empty. In the False case a warning is
      logged describing the missing field.
    """
    for field in required_fields:
        if not row.get(field, "").strip():
            row_id = ""
            if row_id_field is not None:
                row_id = row.get(row_id_field, "").strip()
            if row_id and field != row_id_field:
                logger.warning(
                    "Dropping %s %s: missing %s",
                    row_name,
                    row_id,
                    field,
                )
            else:
                logger.warning("Dropping %s row: missing %s", row_name, field)
            return False
    return True


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        logger.error("File not found: %s", path)
        raise FileNotFoundError(f"File not found: {path}")

    try:
        with path.open(newline="", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            return [row for row in reader]
    except OSError as error:
        logger.error("Could not read file %s: %s", path, error)
        raise


def load_members(path: Path) -> tuple[list[Member], dict[str, Member]]:
    rows = read_csv_rows(path)
    if not rows:
        logger.warning("members.csv is empty")
        return [], {}

    members: list[Member] = []
    barcode_index: dict[str, Member] = {}
    for row in rows:
        if not validate_row(row, "member", MEMBER_REQUIRED_FIELDS):
            continue
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
    if not rows:
        logger.warning("visits.csv is empty")
        return []

    visits: list[Visit] = []
    for row in rows:
        if not validate_row(
            row,
            "visit",
            VISIT_REQUIRED_FIELDS,
            row_id_field="visit_id",
        ):
            continue
        visit_id = row["visit_id"].strip()
        barcode = row["barcode"].strip()
        reservation_id = row.get("reservation_id")
        reservation_id = (
            reservation_id.strip() if reservation_id and reservation_id.strip() else None
        )
        visits.append(
            Visit(visit_id=visit_id, barcode=barcode, reservation_id=reservation_id)
        )

    return visits
