from __future__ import annotations

import argparse
import logging
from pathlib import Path

from .reader import load_members, load_visits
from .validator import filter_valid_visits
from .processor import group_visits_by_member
from .reporter import count_walk_ins, top_n_members
from .writer import write_member_visit_groups


def configure_logging() -> None:
    log_path = Path("logs/app.log")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    handlers = [
        logging.StreamHandler(),
        logging.FileHandler(log_path, encoding="utf-8"),
    ]
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=handlers,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Process membership visits and emit grouped output with summary stats."
    )
    parser.add_argument(
        "--members", default="data/members.csv", help="Path to members CSV"
    )
    parser.add_argument(
        "--visits", default="data/visits.csv", help="Path to visits CSV"
    )
    parser.add_argument(
        "--output", default="output/result.csv", help="Path to output CSV"
    )
    return parser.parse_args()


def main() -> int:
    configure_logging()
    args = parse_args()

    members, members_by_barcode = load_members(Path(args.members))
    visits = load_visits(Path(args.visits))
    valid_visits = filter_valid_visits(visits, members_by_barcode)

    groups = group_visits_by_member(members, valid_visits)
    write_member_visit_groups(Path(args.output), groups)

    walk_in_count = count_walk_ins(valid_visits)
    top_members = top_n_members(valid_visits, members_by_barcode)

    print("Top 5 members by visit count:")
    if top_members:
        for member, count in top_members:
            print(f"{member.member_id}, {count}")
    else:
        print("- none")

    print(f"Total walk-ins: {walk_in_count}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
