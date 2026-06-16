from src.models import Member, Visit
from src.processor import group_visits_by_member


def test_group_visits_includes_members_with_no_visits() -> None:
    members = [
        Member(member_id="1", barcode="ABC123"),
        Member(member_id="2", barcode="DEF456"),
    ]
    visits = [Visit(visit_id="v1", barcode="ABC123", reservation_id="RES-1")]

    groups = group_visits_by_member(members, visits)

    assert isinstance(groups[0].visit_ids, tuple)
    assert isinstance(groups[1].visit_ids, tuple)
    assert groups[0].visit_ids == ("v1",)
    assert groups[1].visit_ids == ()
