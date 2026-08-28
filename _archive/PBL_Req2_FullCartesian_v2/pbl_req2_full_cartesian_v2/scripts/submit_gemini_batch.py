#!/usr/bin/env python3
"""Submit 19 inline requests to Gemini Batch API.

Requires: pip install google-genai pydantic
Authentication: GEMINI_API_KEY environment variable.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Literal

from google import genai
from pydantic import BaseModel


class Candidate(BaseModel):
    candidate_id: str
    stakeholder_id: str
    stakeholder_name: str
    situation_id: str
    situation_name: str
    context_id: str
    context_name: str
    situation_detail: str
    organization_archetype: str
    role: str
    interpretation: str
    technical_bridge: str
    behavior_change: str
    assumption: str
    evidence_status: Literal["FACT", "INFERENCE", "ASSUMPTION"]
    duplicate_note: str


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batches", type=Path, required=True)
    parser.add_argument("--system-instruction", type=Path, required=True)
    parser.add_argument("--model", required=True, help="Current generateContent-compatible Gemini model")
    parser.add_argument("--display-name", default="pbl-req2-full-cartesian")
    args = parser.parse_args()

    system_instruction = args.system_instruction.read_text(encoding="utf-8")
    inline_requests: list[dict] = []
    with args.batches.open("r", encoding="utf-8") as handle:
        for line in handle:
            batch = json.loads(line)
            prompt = json.dumps(batch, ensure_ascii=False, indent=2)
            inline_requests.append(
                {
                    "contents": [
                        {
                            "parts": [
                                {
                                    "text": (
                                        "以下の固定tupleを全件処理してください。"
                                        "expected_countと同数を入力順で返してください。\n\n"
                                        + prompt
                                    )
                                }
                            ],
                            "role": "user",
                        }
                    ],
                    "config": {
                        "system_instruction": {"parts": [{"text": system_instruction}]},
                        "response_mime_type": "application/json",
                        "response_schema": list[Candidate],
                    },
                }
            )

    if len(inline_requests) != 19:
        raise SystemExit("Expected exactly 19 Situation requests")

    client = genai.Client()
    job = client.batches.create(
        model=args.model,
        src=inline_requests,
        config={"display_name": args.display_name},
    )
    print(job.name)


if __name__ == "__main__":
    main()
