from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Member:
    member_id: str
    barcode: str


@dataclass(frozen=True)
class Visit:
    visit_id: str
    barcode: str
    reservation_id: Optional[str]


@dataclass(frozen=True)
class MemberVisitGroup:
    member_id: str
    barcode: str
    visit_ids: tuple[str, ...]
