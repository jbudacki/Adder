#!/usr/bin/env python3
"""Validate embedded specialist fixture coverage and structure."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "evaluations" / "specialists" / "cases.json"
REQUIRED_SKILLS = {
    "adder-security-review",
    "adder-secure-code-review",
    "adder-secrets-analysis",
    "adder-iam-security",
    "adder-network-exposure",
    "adder-crypto-analysis",
    "adder-llm-security",
    "adder-3pp-dependency-hygiene",
    "adder-package-trust",
    "adder-test-evidence",
    "adder-threat-model",
}


def main() -> None:
    data = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError("cases must be a non-empty list")

    ids: set[str] = set()
    covered: set[str] = set()
    for case in cases:
        case_id = case.get("id")
        skill = case.get("skill")
        expected = case.get("expected", {})
        if not isinstance(case_id, str) or not case_id or case_id in ids:
            raise ValueError(f"invalid or duplicate case id: {case_id!r}")
        if skill not in REQUIRED_SKILLS:
            raise ValueError(f"{case_id}: unexpected skill {skill!r}")
        if not isinstance(case.get("input_summary"), str) or not case["input_summary"]:
            raise ValueError(f"{case_id}: input_summary is required")
        if not isinstance(expected.get("action"), str) or not expected["action"]:
            raise ValueError(f"{case_id}: expected action is required")
        if not isinstance(expected.get("required_skills"), list):
            raise ValueError(f"{case_id}: required_skills must be a list")
        evidence = expected.get("evidence_requirements")
        if not isinstance(evidence, list) or len(evidence) < 3:
            raise ValueError(f"{case_id}: at least three evidence requirements are required")
        ids.add(case_id)
        covered.add(skill)

    if covered != REQUIRED_SKILLS:
        raise ValueError(f"specialist coverage mismatch: {sorted(REQUIRED_SKILLS - covered)}")
    print(f"Validated {len(cases)} embedded specialist fixtures across {len(covered)} skills.")


if __name__ == "__main__":
    main()
