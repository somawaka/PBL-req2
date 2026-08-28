#!/usr/bin/env python3
"""Build the deterministic Stakeholder x Situation x Context grid."""

from __future__ import annotations

import argparse
import csv
from itertools import product
from pathlib import Path


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--patent-id", required=True)
    parser.add_argument("--patent-title", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()

    stakeholders = read_csv(args.root / "01_stakeholder_framework.csv")
    situations = read_csv(args.root / "02_situation_framework.csv")
    contexts = read_csv(args.root / "03_context_framework.csv")

    if (len(stakeholders), len(situations), len(contexts)) != (5, 19, 6):
        raise SystemExit(
            "Framework cardinality mismatch: expected Stakeholder=5, Situation=19, Context=6"
        )

    fieldnames = [
        "candidate_id",
        "patent_id",
        "patent_title",
        "stakeholder_id",
        "stakeholder_name",
        "situation_id",
        "situation_name",
        "context_id",
        "context_name",
    ]
    rows: list[dict[str, str]] = []
    for situation, stakeholder, context in product(situations, stakeholders, contexts):
        rows.append(
            {
                "candidate_id": (
                    f"{args.patent_id}-{situation['situation_id']}-"
                    f"{stakeholder['stakeholder_id']}-{context['context_id']}"
                ),
                "patent_id": args.patent_id,
                "patent_title": args.patent_title,
                "stakeholder_id": stakeholder["stakeholder_id"],
                "stakeholder_name": stakeholder["name_ja"],
                "situation_id": situation["situation_id"],
                "situation_name": situation["name_ja"],
                "context_id": context["context_id"],
                "context_name": context["name_ja"],
            }
        )

    if len(rows) != 570 or len({row["candidate_id"] for row in rows}) != 570:
        raise SystemExit("The Cartesian grid must contain 570 unique candidate IDs")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {len(rows)} rows to {args.output}")


if __name__ == "__main__":
    main()
