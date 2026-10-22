#!/usr/bin/env python3
"""Prepare a supplied ADDER assessment or create an explicit degraded-mode record."""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


OUTCOMES = {"pass", "warning", "manual_review", "block_recommended"}
REQUIRED_KEYS = {
    "schema_version",
    "assessment_id",
    "subject",
    "risk_tier",
    "outcome",
    "findings",
    "required_actions",
    "generated_at",
}


def validate_minimum(assessment: Any) -> dict[str, Any]:
    if not isinstance(assessment, dict):
        raise ValueError("assessment must be a JSON object")
    missing = sorted(REQUIRED_KEYS - set(assessment))
    if missing:
        raise ValueError(f"assessment is missing required fields: {', '.join(missing)}")
    if assessment.get("outcome") not in OUTCOMES:
        raise ValueError("assessment outcome is invalid")
    if assessment.get("risk_tier") not in {1, 2, 3}:
        raise ValueError("assessment risk_tier is invalid")
    if not isinstance(assessment.get("findings"), list):
        raise ValueError("assessment findings must be a list")
    return assessment


def degraded_assessment(reason: str) -> dict[str, Any]:
    repository = os.environ.get("CI_PROJECT_PATH", "unknown-repository")
    commit = os.environ.get("CI_COMMIT_SHA", "unknown-commit")
    merge_request = os.environ.get("CI_MERGE_REQUEST_IID")
    subject: dict[str, str] = {"repository": repository, "commit": commit}
    if merge_request:
        subject["merge_request"] = merge_request
    return {
        "schema_version": "1.0.0",
        "assessment_id": f"degraded-{commit[:12]}",
        "subject": subject,
        "risk_tier": 3,
        "risk_rationale": ["Change scope was not classified; Tier 3 is used conservatively pending review."],
        "outcome": "manual_review",
        "findings": [],
        "checks_performed": ["ADDER degraded-mode assessment preparation"],
        "checks_not_performed": ["Contextual ADDER assessment"],
        "required_actions": ["Complete the required ADDER assessment and obtain applicable human review."],
        "required_approvals": ["Human review appropriate to the confirmed risk tier"],
        "limitations": [reason],
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "toolkit_version": "0.1.0",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare an ADDER advisory assessment for CI reporting")
    parser.add_argument("--input", help="Optional supplied assessment JSON")
    parser.add_argument("--output", required=True, help="Normalized output assessment JSON")
    args = parser.parse_args()

    prepared: dict[str, Any]
    source = Path(args.input) if args.input else None
    if source and source.is_file():
        try:
            prepared = validate_minimum(json.loads(source.read_text(encoding="utf-8")))
        except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
            prepared = degraded_assessment(f"Supplied assessment was invalid: {error}")
    else:
        prepared = degraded_assessment("No contextual assessment artifact was supplied to the advisory job.")

    output = Path(args.output)
    output.write_text(json.dumps(prepared, indent=2) + "\n", encoding="utf-8")
    print(f"Prepared advisory assessment with outcome={prepared['outcome']} at {output}")


if __name__ == "__main__":
    main()

