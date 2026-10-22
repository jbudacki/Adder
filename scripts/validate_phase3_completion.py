#!/usr/bin/env python3
"""Validate package-trust and security-test-evidence evaluation invariants."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "evaluations" / "phase3-completion" / "cases.json"
EXPECTED_STATUSES = {
    "adder-package-trust": {"verified", "manual_review", "block_recommended"},
    "adder-test-evidence": {"sufficient", "insufficient", "manual_review"},
}
REQUIRED_RESOURCES = (
    ROOT / "schemas" / "package-trust-assessment.schema.json",
    ROOT / "schemas" / "test-evidence-assessment.schema.json",
    ROOT / "policies" / "package-trust-policy.md",
    ROOT / "policies" / "security-test-evidence-policy.md",
    ROOT / "skills" / "adder-package-trust" / "references" / "evidence-and-decisions.md",
    ROOT / "skills" / "adder-test-evidence" / "references" / "assessment-method.md",
)


def require_mapping(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    return value


def validate_package_case(case_id: str, evidence: dict[str, Any], status: str) -> None:
    if status == "verified":
        required = {
            "approved_registry": "yes",
            "exact_version": "exists",
            "publisher_status": "verified",
            "integrity_status": "verified",
            "lockfile_consistency": "consistent",
            "vulnerability_status": "no_applicable_signal",
            "malware_status": "no_signal",
            "reputation_status": "acceptable",
            "sources_current": True,
        }
        mismatches = [key for key, value in required.items() if evidence.get(key) != value]
        if mismatches:
            raise ValueError(f"{case_id}: verified package is missing required evidence: {mismatches}")
    if status == "block_recommended" and not (
        evidence.get("integrity_status") == "mismatch"
        or evidence.get("malware_status") == "confirmed"
        or evidence.get("exact_version") == "not_found"
        or evidence.get("approved_registry") == "no"
    ):
        raise ValueError(f"{case_id}: blocking package case lacks an exact blocking condition")
    if evidence.get("reputation_status") == "concern" and all(
        evidence.get(field) in {"unknown", "unavailable", False}
        for field in ("exact_version", "publisher_status", "integrity_status", "sources_current")
    ) and status == "block_recommended":
        raise ValueError(f"{case_id}: reputation concern alone cannot recommend blocking")


def validate_test_case(case_id: str, evidence: dict[str, Any], status: str) -> None:
    coverage = evidence.get("coverage_kinds")
    if not isinstance(coverage, list) or not all(isinstance(item, str) for item in coverage):
        raise ValueError(f"{case_id}: coverage_kinds must be an array of strings")
    if status == "sufficient":
        if "negative" not in coverage or evidence.get("assertion_strength") != "strong":
            raise ValueError(f"{case_id}: sufficient evidence requires negative coverage and strong assertions")
        if evidence.get("execution_status") != "passed":
            raise ValueError(f"{case_id}: sufficient evidence requires passed execution")
        if evidence.get("independence_status") not in {"independent", "mixed"}:
            raise ValueError(f"{case_id}: sufficient evidence requires independent evidence")
    if evidence.get("execution_status") == "unavailable" and status == "sufficient":
        raise ValueError(f"{case_id}: unavailable execution cannot be sufficient")


def main() -> None:
    for resource in REQUIRED_RESOURCES:
        if not resource.is_file() or not resource.read_text(encoding="utf-8").strip():
            raise ValueError(f"missing or empty Phase 3 resource: {resource}")
    for schema in REQUIRED_RESOURCES[:2]:
        document = require_mapping(json.loads(schema.read_text(encoding="utf-8")), str(schema))
        if document.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            raise ValueError(f"{schema}: unexpected JSON Schema draft")

    data = require_mapping(json.loads(CASES_PATH.read_text(encoding="utf-8")), "evaluation document")
    if data.get("schema_version") != "1.0.0":
        raise ValueError("unsupported evaluation schema_version")
    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError("cases must be a non-empty array")

    identifiers: set[str] = set()
    observed: dict[str, set[str]] = {skill: set() for skill in EXPECTED_STATUSES}
    for case in cases:
        case = require_mapping(case, "case")
        case_id = case.get("id")
        skill = case.get("skill")
        if not isinstance(case_id, str) or not case_id or case_id in identifiers:
            raise ValueError(f"invalid or duplicate case id: {case_id!r}")
        if skill not in EXPECTED_STATUSES:
            raise ValueError(f"{case_id}: unexpected skill {skill!r}")
        identifiers.add(case_id)
        evidence = require_mapping(case.get("evidence"), f"{case_id}.evidence")
        expected = require_mapping(case.get("expected"), f"{case_id}.expected")
        status = expected.get("status")
        if status not in EXPECTED_STATUSES[skill]:
            raise ValueError(f"{case_id}: invalid expected status {status!r}")
        if not isinstance(expected.get("reason"), str) or not expected["reason"]:
            raise ValueError(f"{case_id}: expected reason is required")
        if not isinstance(expected.get("required_skills"), list):
            raise ValueError(f"{case_id}: required_skills must be an array")
        observed[skill].add(status)
        if skill == "adder-package-trust":
            validate_package_case(case_id, evidence, status)
        else:
            validate_test_case(case_id, evidence, status)

    for skill, statuses in EXPECTED_STATUSES.items():
        if observed[skill] != statuses:
            raise ValueError(f"{skill}: status coverage mismatch: {sorted(statuses - observed[skill])}")
    print(f"Validated {len(cases)} Phase 3 completion cases across {len(observed)} skills.")


if __name__ == "__main__":
    main()
