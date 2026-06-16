import logging
import pytest

from src.models import Member, Visit
from src.validator import filter_valid_visits


def test_filter_valid_visits_drops_missing_barcode(
    caplog: pytest.LogCaptureFixture,
) -> None:
    caplog.set_level(logging.WARNING)
    visits = [Visit(visit_id="v1", barcode="", reservation_id=None)]
    members = {"ABC123": Member(member_id="1", barcode="ABC123")}

    valid = filter_valid_visits(visits, members)

    assert not valid
    assert "missing barcode" in caplog.text


def test_filter_valid_visits_drops_unknown_barcode(
    caplog: pytest.LogCaptureFixture,
) -> None:
    caplog.set_level(logging.WARNING)
    visits = [Visit(visit_id="v2", barcode="UNKNOWN", reservation_id=None)]
    members = {"ABC123": Member(member_id="1", barcode="ABC123")}

    valid = filter_valid_visits(visits, members)

    assert not valid
    assert "not found in members.csv" in caplog.text
