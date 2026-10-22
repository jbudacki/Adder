#!/usr/bin/env python3
"""Validate Phase 2 evaluation fixture structure and decision invariants."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "evaluations" / "core-assurance" / "cases.json"
VALID_OUTCOMES = {"pass", "warning", "manual_review", "block_recommended"}


def main() -> None:
    data = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError("cases must be a non-empty list")

    seen_ids: set[str] = set()
    seen_tiers: set[int] = set()
    seen_outcomes: set[str] = set()

    for case in cases:
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id:
            raise ValueError("each case requires a non-empty id")
        if case_id in seen_ids:
            raise ValueError(f"duplicate case id: {case_id}")
        seen_ids.add(case_id)

        inputs = case.get("input", {})
        expected = case.get("expected", {})
        tier = expected.get("risk_tier")
        outcome = expected.get("outcome")
        reasons = expected.get("must_include_reasons")

        if tier not in {1, 2, 3}:
            raise ValueError(f"{case_id}: invalid risk tier")
        if outcome not in VALID_OUTCOMES:
            raise ValueError(f"{case_id}: invalid outcome")
        if not isinstance(reasons, list) or not reasons:
            raise ValueError(f"{case_id}: expected reasons must be non-empty")
        if outcome == "pass" and inputs.get("findings"):
            raise ValueError(f"{case_id}: pass fixture cannot contain unresolved findings")
        if outcome == "block_recommended":
            blocking = any(
                finding.get("status") == "validated"
                and finding.get("blocking_policy_match") is True
                for finding in inputs.get("findings", [])
            )
            missing_approval = inputs.get("required_approvals_present") is False
            if not (blocking or missing_approval):
                raise ValueError(f"{case_id}: block requires validated policy evidence")
        if tier == 3 and outcome == "pass":
            if inputs.get("required_approvals_present") is not True:
                raise ValueError(f"{case_id}: Tier 3 pass requires explicit approval")

        seen_tiers.add(tier)
        seen_outcomes.add(outcome)

    if seen_tiers != {1, 2, 3}:
        raise ValueError(f"fixtures must cover all tiers; found {sorted(seen_tiers)}")
    if seen_outcomes != VALID_OUTCOMES:
        raise ValueError(f"fixtures must cover all outcomes; found {sorted(seen_outcomes)}")

    print(f"Validated {len(cases)} core assurance fixtures.")


if __name__ == "__main__":
    main()

