#!/usr/bin/env python3
"""Group the 570-row grid into 19 complete 30-tuple Situation batches."""

from __future__ import annotations

import argparse
import csv
import json
from collections import OrderedDict
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--grid", type=Path, required=True)
    parser.add_argument("--capability-card", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    with args.grid.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    capability_card = args.capability_card.read_text(encoding="utf-8")

    batches: OrderedDict[str, list[dict[str, str]]] = OrderedDict()
    for row in rows:
        batches.setdefault(row["situation_id"], []).append(row)

    if len(rows) != 570 or len(batches) != 19:
        raise SystemExit("Expected 570 rows grouped into 19 Situations")
    if any(len(batch) != 30 for batch in batches.values()):
        raise SystemExit("Every Situation batch must contain 30 tuples")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as handle:
        for situation_id, batch in batches.items():
            payload = {
                "key": f"situation-{situation_id}",
                "capability_card": capability_card,
                "expected_count": 30,
                "tuples": batch,
            }
            handle.write(json.dumps(payload, ensure_ascii=False) + "\n")
    print(f"wrote {len(batches)} batches to {args.output}")


if __name__ == "__main__":
    main()
