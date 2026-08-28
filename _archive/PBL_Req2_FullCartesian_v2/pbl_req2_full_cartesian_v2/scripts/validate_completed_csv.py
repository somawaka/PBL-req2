#!/usr/bin/env python3
"""Validate that a completed Req2 CSV preserves the 570-cell grid."""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path


REQUIRED = {
    "candidate_id",
    "stakeholder_id",
    "situation_id",
    "context_id",
    "interpretation",
    "technical_bridge",
    "behavior_change",
    "assumption",
    "evidence_status",
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    args = parser.parse_args()

    with args.input.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        fields = set(reader.fieldnames or [])

    missing_columns = REQUIRED - fields
    if missing_columns:
        raise SystemExit(f"Missing columns: {sorted(missing_columns)}")
    if len(rows) != 570:
        raise SystemExit(f"Expected 570 rows, got {len(rows)}")

    ids = [row["candidate_id"] for row in rows]
    if len(set(ids)) != 570:
        raise SystemExit("Candidate IDs are not unique")

    expected = {(s, st, c) for s in list("ABCDEFGHIJKLMNOPQRS") for st in [f"S{i}" for i in range(1, 6)] for c in [f"C{i}" for i in range(1, 7)]}
    actual = {(row["situation_id"], row["stakeholder_id"], row["context_id"]) for row in rows}
    if actual != expected:
        raise SystemExit(f"Cartesian coverage mismatch: missing={len(expected-actual)}, extra={len(actual-expected)}")

    blank_counts = Counter(
        field for field in REQUIRED for row in rows if not row.get(field, "").strip()
    )
    if blank_counts:
        raise SystemExit(f"Required values are blank: {dict(blank_counts)}")
    print("valid: 570 unique rows, full 5 x 19 x 6 coverage, required values present")


if __name__ == "__main__":
    main()
