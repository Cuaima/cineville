import csv
import json
from pathlib import Path

from src.models import MemberVisitGroup
from src.writer import write_member_visit_groups


def test_write_member_visit_groups_serializes_json_list(tmp_path: Path) -> None:
    output_path = tmp_path / "result.csv"
    groups = [MemberVisitGroup(member_id="1", barcode="ABC123", visit_ids=("v1", "v2"))]

    write_member_visit_groups(output_path, groups)

    with output_path.open("r", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        rows = list(reader)

    assert rows[0]["member_id"] == "1"
    assert rows[0]["barcode"] == "ABC123"
    assert json.loads(rows[0]["visit_ids"]) == ["v1", "v2"]
