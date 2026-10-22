#!/usr/bin/env python3
"""Validate Phase 4 agent-boundary and recovery fixture invariants."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "evaluations" / "agent-recovery" / "cases.json"
BOUNDARY_STATUSES = {"within_boundary", "gap", "violation", "unverifiable"}
RECOVERY_STATUSES = {
    "planned",
    "containment_pending",
    "remediation_in_progress",
    "verification_pending",
    "ready_for_human_approval",
    "verified",
    "failed",
}


def main() -> None:
    data = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError("cases must be a non-empty list")

    ids: set[str] = set()
    boundary_coverage: set[str] = set()
    skill_coverage: set[str] = set()

    for case in cases:
        case_id = case.get("id")
        skill = case.get("skill")
        expected = case.get("expected", {})
        if not isinstance(case_id, str) or not case_id or case_id in ids:
            raise ValueError(f"invalid or duplicate case id: {case_id!r}")
        if skill not in {"adder-agent-boundary", "adder-code-recovery"}:
            raise ValueError(f"{case_id}: unexpected skill {skill!r}")
        if not isinstance(case.get("input_summary"), str) or not case["input_summary"]:
            raise ValueError(f"{case_id}: input_summary is required")

        ids.add(case_id)
        skill_coverage.add(skill)

        if skill == "adder-agent-boundary":
            status = expected.get("overall_status")
            evidence = expected.get("evidence_requirements")
            if status not in BOUNDARY_STATUSES:
                raise ValueError(f"{case_id}: invalid boundary status")
            if not isinstance(evidence, list) or len(evidence) < 3:
                raise ValueError(f"{case_id}: boundary evidence requirements are incomplete")
            if status == "violation" and expected.get("decision_signal") != "block_recommended":
                raise ValueError(f"{case_id}: a demonstrated violation must signal block_recommended")
            if status == "unverifiable" and expected.get("decision_signal") != "manual_review":
                raise ValueError(f"{case_id}: unverifiable evidence must signal manual_review")
            boundary_coverage.add(status)
            continue

        status = expected.get("status")
        checks = expected.get("required_checks")
        required_approvals = expected.get("required_approvals")
        verification = expected.get("verification_evidence")
        approvals = expected.get("approval_evidence")
        if status not in RECOVERY_STATUSES:
            raise ValueError(f"{case_id}: invalid recovery status")
        if not isinstance(checks, list) or not checks:
            raise ValueError(f"{case_id}: required checks are missing")
        if not isinstance(required_approvals, list):
            raise ValueError(f"{case_id}: required_approvals must be a list")
        if not isinstance(verification, list) or not isinstance(approvals, list):
            raise ValueError(f"{case_id}: evidence fields must be lists")
        check_statuses = {item.get("status") for item in checks}
        if status == "verified":
            if check_statuses != {"passed"} or not verification:
                raise ValueError(f"{case_id}: verified recovery lacks passed checks or evidence")
            if required_approvals and not approvals:
                raise ValueError(f"{case_id}: verified recovery lacks required approval evidence")
        if status == "failed" and "failed" not in check_statuses:
            raise ValueError(f"{case_id}: failed recovery requires a failed check")
        if status == "verification_pending" and check_statuses <= {"passed"}:
            raise ValueError(f"{case_id}: pending recovery must identify an incomplete check")

    if boundary_coverage != BOUNDARY_STATUSES:
        raise ValueError(f"boundary status coverage mismatch: {sorted(BOUNDARY_STATUSES - boundary_coverage)}")
    if skill_coverage != {"adder-agent-boundary", "adder-code-recovery"}:
        raise ValueError("both Phase 4 skills require fixture coverage")

    print(f"Validated {len(cases)} agent-boundary and recovery fixtures.")


if __name__ == "__main__":
    main()
