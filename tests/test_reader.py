from pathlib import Path
import pytest
from src.reader import load_members, load_visits


def write_csv(path: Path, header: list[str], rows: list[list[str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as csv_file:
        csv_file.write(",".join(header) + "\n")
        for row in rows:
            csv_file.write(",".join(row) + "\n")


def test_load_members_reads_member_records(tmp_path: Path) -> None:
    path = tmp_path / "members.csv"
    write_csv(path, ["member_id", "barcode"], [["1", "ABC123"], ["2", "DEF456"]])

    members, members_by_barcode = load_members(path)

    assert len(members) == 2
    assert members_by_barcode["ABC123"].member_id == "1"
    assert members_by_barcode["DEF456"].member_id == "2"


def test_load_members_raises_for_missing_columns(tmp_path: Path) -> None:
    path = tmp_path / "members.csv"
    write_csv(path, ["member_id"], [["1"], ["2"]])

    with pytest.raises(ValueError):
        load_members(path)


def test_load_visits_parses_missing_reservation_id(tmp_path: Path) -> None:
    path = tmp_path / "visits.csv"
    write_csv(
        path,
        ["visit_id", "barcode", "reservation_id"],
        [["v1", "ABC123", ""], ["v2", "DEF456", "RES-1"]],
    )

    visits = load_visits(path)

    assert visits[0].reservation_id == ""
    assert visits[1].reservation_id == "RES-1"
