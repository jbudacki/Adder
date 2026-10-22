#!/usr/bin/env python3
"""Validate Phase 6 intelligence-loop and release-readiness invariants."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PATHS = [
    "skills/adder-intelligence-loop/SKILL.md",
    "skills/adder-intelligence-loop/references/control-lifecycle.md",
    "skills/adder-intelligence-loop/agents/openai.yaml",
    "schemas/intelligence-record.schema.json",
    "schemas/release-readiness.schema.json",
    "policies/control-promotion-policy.md",
    "docs/release-criteria.md",
    "docs/release-readiness.md",
    "docs/compatibility.md",
    "docs/operational-ownership.md",
    "docs/pilot-evidence.md",
    "docs/build-buy-recommendation.md",
    "evaluations/intelligence-loop/cases.json",
    "evaluations/intelligence-loop/control-candidates.json",
    "release/readiness.json",
]


def load_json(relative_path: str):
    with (ROOT / relative_path).open(encoding="utf-8") as handle:
        return json.load(handle)


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def main() -> int:
    errors: list[str] = []

    for relative_path in REQUIRED_PATHS:
        if not (ROOT / relative_path).is_file():
            fail(errors, f"missing required Phase 6 file: {relative_path}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    for schema_path in (
        "schemas/intelligence-record.schema.json",
        "schemas/release-readiness.schema.json",
    ):
        schema = load_json(schema_path)
        if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            fail(errors, f"{schema_path}: expected JSON Schema draft 2020-12")

    cases = load_json("evaluations/intelligence-loop/cases.json").get("cases", [])
    required_case_ids = {
        "repeated-human-validated-auth-finding",
        "single-agent-validated-operational-finding",
        "material-false-positive",
        "incomplete-pilot-requests-mandatory",
        "verified-remediation-and-recovery",
        "contradictory-or-stale-evidence",
    }
    case_ids = {case.get("id") for case in cases}
    missing_cases = required_case_ids - case_ids
    if missing_cases:
        fail(errors, f"missing intelligence-loop cases: {sorted(missing_cases)}")

    for case in cases:
        expected = case.get("expected_state")
        prerequisites = case.get("prerequisites", {})
        if expected == "mandatory":
            mandatory_requirements = (
                case.get("validation_status") in {"human_validated", "independently_verified"},
                case.get("evidence_scope") == "multiple_repositories",
                prerequisites.get("owner") is True,
                prerequisites.get("positive_fixture") is True,
                prerequisites.get("negative_fixture") is True,
                prerequisites.get("ambiguous_fixture") is True,
                prerequisites.get("rollback_fixture") is True,
                prerequisites.get("representative_cohort") is True,
                prerequisites.get("enforcement_approval") is True,
                case.get("material_false_positive") is not True,
            )
            if not all(mandatory_requirements):
                fail(errors, f"{case.get('id')}: invalid mandatory expectation")
        if case.get("material_false_positive") and not prerequisites.get("negative_fixture"):
            fail(errors, f"{case.get('id')}: material false positive lacks negative fixture")

    candidates = load_json("evaluations/intelligence-loop/control-candidates.json")
    candidate_ids: set[str] = set()
    for candidate in candidates:
        record_id = candidate.get("record_id")
        if not record_id or record_id in candidate_ids:
            fail(errors, f"duplicate or missing intelligence record id: {record_id}")
        candidate_ids.add(record_id)
        for field in (
            "schema_version",
            "record_id",
            "source_evidence",
            "validation_status",
            "root_cause",
            "proposed_control",
            "applicability",
            "validation_cases",
            "lifecycle_status",
            "owner",
            "promotion_blockers",
            "rollback_trigger",
            "created_at",
            "review_by",
            "limitations",
        ):
            if field not in candidate:
                fail(errors, f"{record_id}: missing {field}")
        fixture_types = {fixture.get("case_type") for fixture in candidate.get("validation_cases", [])}
        if fixture_types != {"positive", "negative", "ambiguous", "rollback"}:
            fail(errors, f"{record_id}: incomplete validation-case types")
        if candidate.get("lifecycle_status") == "mandatory":
            if candidate.get("owner") is None:
                fail(errors, f"{record_id}: mandatory control has no owner")
            if candidate.get("validation_status") not in {"human_validated", "independently_verified"}:
                fail(errors, f"{record_id}: mandatory control lacks human validation")
        if "control_type" not in candidate.get("proposed_control", {}):
            fail(errors, f"{record_id}: proposed control lacks control_type")

    readiness = load_json("release/readiness.json")
    for field in (
        "schema_version",
        "decision_id",
        "toolkit_version",
        "decision",
        "criteria",
        "blocking_conditions",
        "allowed_use",
        "prohibited_use",
        "decision_owner",
        "generated_at",
        "review_by",
    ):
        if field not in readiness:
            fail(errors, f"release/readiness.json: missing {field}")
    if readiness.get("decision") != "pilot_only":
        fail(errors, "current release decision must remain pilot_only for available evidence")
    criteria = readiness.get("criteria", [])
    criterion_ids = [criterion.get("criterion_id") for criterion in criteria]
    if len(criterion_ids) != len(set(criterion_ids)):
        fail(errors, "release criteria contain duplicate ids")
    criterion_status = {criterion.get("criterion_id"): criterion.get("status") for criterion in criteria}
    for criterion in criteria:
        for reference in criterion.get("evidence", []):
            if not (ROOT / reference).exists():
                fail(errors, f"release criterion evidence does not exist: {reference}")
    for blocker_id in (
        "representative-cohort",
        "human-metrics",
        "ownership",
        "license-distribution",
        "release-integrity",
        "enforcement-approval",
    ):
        if criterion_status.get(blocker_id) != "not_met":
            fail(errors, f"release blocker must be not_met: {blocker_id}")
    if readiness.get("decision_owner") is not None:
        fail(errors, "decision_owner must remain null until a human owner accepts the decision")
    prohibited = " ".join(readiness.get("prohibited_use", [])).lower()
    if "mandatory" not in prohibited or "enforcement" not in prohibited:
        fail(errors, "release record must prohibit mandatory enforcement")

    pilot_root = ROOT / "evaluations/pilot/runs"
    operational_runs = [
        path for path in pilot_root.iterdir()
        if path.is_dir() and path.name != "fixtures" and (path / "assessment.json").is_file()
    ]
    if len(operational_runs) >= 3:
        fail(errors, "release/readiness.json is stale: representative cohort may now be complete")
    if criterion_status.get("representative-cohort") != "not_met":
        fail(errors, "incomplete operational cohort must block release")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(
        "Phase 6 validation passed: "
        f"{len(cases)} lifecycle cases, {len(candidates)} control candidates, "
        f"{len(operational_runs)}/3 operational pilot repositories, decision=pilot_only."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
