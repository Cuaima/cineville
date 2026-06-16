from src.models import Member, Visit
from src.reporter import count_walk_ins, top_n_members


def test_count_walk_ins_counts_empty_reservation_id() -> None:
    visits = [
        Visit(visit_id="v1", barcode="ABC123", reservation_id=""),
        Visit(visit_id="v2", barcode="DEF456", reservation_id="RES-1"),
    ]

    assert count_walk_ins(visits) == 1


def test_count_walk_ins_counts_none_reservation_id() -> None:
    visits = [
        Visit(visit_id="v1", barcode="ABC123", reservation_id=None),
        Visit(visit_id="v2", barcode="DEF456", reservation_id="RES-1"),
    ]

    assert count_walk_ins(visits) == 1


def test_top_n_members_returns_member_objects() -> None:
    members = {
        "ABC123": Member(member_id="1", barcode="ABC123"),
        "DEF456": Member(member_id="2", barcode="DEF456"),
    }
    visits = [
        Visit(visit_id="v1", barcode="ABC123", reservation_id=None),
        Visit(visit_id="v2", barcode="DEF456", reservation_id="RES-1"),
        Visit(visit_id="v3", barcode="ABC123", reservation_id=None),
    ]

    top = top_n_members(visits, members, n=2)

    assert top[0][0].member_id == "1"
    assert top[0][1] == 2
    assert top[1][0].member_id == "2"
    assert top[1][1] == 1
