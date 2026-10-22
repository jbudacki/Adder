#!/usr/bin/env python3
"""Validate Phase 5 fixtures, GitLab artifacts, fallback behavior, and metrics."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPRESENTATIVE_ROOT = ROOT / "evaluations" / "representative-repositories"
OPERATIONAL_RUNS_ROOT = ROOT / "evaluations" / "pilot" / "runs"


def run(*arguments: str, environment: dict[str, str] | None = None) -> None:
    result = subprocess.run(
        [sys.executable, *arguments],
        cwd=ROOT,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise ValueError(f"command failed: {' '.join(arguments)}\n{result.stderr.strip()}")


def validate_representative_repositories() -> None:
    expected_types = {
        "application": "enterprise_application",
        "infrastructure": "infrastructure",
        "ai-agent": "ai_agent",
    }
    catalog = (ROOT / "skills" / "CATALOG.md").read_text(encoding="utf-8")
    for directory, repository_type in expected_types.items():
        fixture = REPRESENTATIVE_ROOT / directory
        for required in (fixture / "baseline", fixture / "proposed", fixture / "expected.json"):
            if not required.exists():
                raise ValueError(f"missing representative fixture path: {required}")
        expected = json.loads((fixture / "expected.json").read_text(encoding="utf-8"))
        if expected.get("repository_type") != repository_type or expected.get("risk_tier") not in {1, 2, 3}:
            raise ValueError(f"{directory}: invalid repository type or risk tier")
        required_skills = expected.get("required_skills")
        if not isinstance(required_skills, list) or not required_skills:
            raise ValueError(f"{directory}: required_skills are missing")
        for skill in required_skills:
            if f"`{skill}`" not in catalog:
                raise ValueError(f"{directory}: unknown ADDER skill {skill}")
        if len(expected.get("evidence_requirements", [])) < 3:
            raise ValueError(f"{directory}: insufficient evidence requirements")


def validate_gitlab_artifacts(temporary: Path) -> None:
    valid_input = ROOT / "examples" / "gitlab" / "adder-assessment.example.json"
    normalized = temporary / "adder-assessment.json"
    markdown = temporary / "adder-report.md"
    codequality = temporary / "gl-code-quality-report.json"
    run(str(ROOT / "scripts" / "prepare_advisory_assessment.py"), "--input", str(valid_input), "--output", str(normalized))
    run(
        str(ROOT / "scripts" / "render_gitlab_report.py"),
        "--assessment", str(normalized),
        "--markdown", str(markdown),
        "--codequality", str(codequality),
    )
    assessment = json.loads(normalized.read_text(encoding="utf-8"))
    entries = json.loads(codequality.read_text(encoding="utf-8"))
    if assessment.get("outcome") != "block_recommended":
        raise ValueError("valid example assessment outcome changed")
    if len(entries) != 1:
        raise ValueError("expected one GitLab Code Quality entry")
    entry = entries[0]
    required_fields = {"description", "check_name", "fingerprint", "severity", "location"}
    if not required_fields <= set(entry):
        raise ValueError("GitLab Code Quality entry is missing required fields")
    if entry["location"]["path"].startswith("./") or entry["location"]["lines"]["begin"] < 1:
        raise ValueError("GitLab Code Quality location is invalid")
    if "Advisory only" not in markdown.read_text(encoding="utf-8"):
        raise ValueError("Markdown report is missing the advisory boundary")

    degraded = temporary / "degraded-assessment.json"
    environment = dict(os.environ)
    environment.update({"CI_PROJECT_PATH": "synthetic/group/project", "CI_COMMIT_SHA": "f" * 40})
    run(
        str(ROOT / "scripts" / "prepare_advisory_assessment.py"),
        "--input", str(temporary / "missing-assessment.json"),
        "--output", str(degraded),
        environment=environment,
    )
    degraded_data = json.loads(degraded.read_text(encoding="utf-8"))
    if degraded_data.get("outcome") != "manual_review" or degraded_data.get("risk_tier") != 3:
        raise ValueError("degraded mode must produce conservative manual_review")


def validate_metrics(temporary: Path) -> None:
    summary = temporary / "pilot-summary.json"
    run(
        str(ROOT / "scripts" / "aggregate_pilot_metrics.py"),
        "--input", str(ROOT / "evaluations" / "pilot" / "observations.example.json"),
        "--output", str(summary),
    )
    actual = json.loads(summary.read_text(encoding="utf-8"))
    expected = json.loads((ROOT / "evaluations" / "pilot" / "expected-summary.json").read_text(encoding="utf-8"))
    if actual != expected:
        raise ValueError("pilot metric aggregate does not match the expected synthetic summary")

    invalid_observations = json.loads(
        (ROOT / "evaluations" / "pilot" / "observations.example.json").read_text(encoding="utf-8")
    )
    invalid_observations[0]["findings_reviewed"] = 1.5
    invalid_input = temporary / "invalid-observations.json"
    invalid_input.write_text(json.dumps(invalid_observations), encoding="utf-8")
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "aggregate_pilot_metrics.py"),
            "--input",
            str(invalid_input),
            "--output",
            str(temporary / "invalid-summary.json"),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        raise ValueError("pilot metric importer accepted a fractional integer field")


def validate_gitlab_yaml_contract() -> None:
    template = (ROOT / "examples" / "gitlab" / "adder-advisory.gitlab-ci.yml").read_text(encoding="utf-8")
    required_tokens = (
        "allow_failure: true",
        "codequality: gl-code-quality-report.json",
        "expose_as: \"ADDER advisory report\"",
        'CI_PIPELINE_SOURCE == "merge_request_event"',
        "CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH",
    )
    for token in required_tokens:
        if token not in template:
            raise ValueError(f"GitLab advisory template is missing {token!r}")


def validate_operational_runs(temporary: Path) -> None:
    if not OPERATIONAL_RUNS_ROOT.is_dir():
        return
    run_directories = sorted(path for path in OPERATIONAL_RUNS_ROOT.iterdir() if path.is_dir())
    for run_directory in run_directories:
        required_files = (
            "assessment.json",
            "adder-report.md",
            "gl-code-quality-report.json",
            "operational-pilot-report.md",
            "pilot-observations.json",
            "pilot-summary.json",
            "provenance.json",
            "risk-classification.json",
            "test-evidence-assessment.json",
            "threat-model.md",
        )
        for filename in required_files:
            if not (run_directory / filename).is_file():
                raise ValueError(f"{run_directory.name}: missing operational artifact {filename}")

        assessment = json.loads((run_directory / "assessment.json").read_text(encoding="utf-8"))
        if assessment.get("risk_tier") != 3 or assessment.get("outcome") not in {
            "manual_review",
            "block_recommended",
        }:
            raise ValueError(f"{run_directory.name}: operational Tier 3 disposition is invalid")
        findings = assessment.get("findings")
        if not isinstance(findings, list) or not findings:
            raise ValueError(f"{run_directory.name}: operational assessment has no findings")
        for finding in findings:
            if finding.get("status") not in {"candidate", "validated", "false_positive", "accepted", "remediated"}:
                raise ValueError(f"{run_directory.name}: finding has invalid status")
            if not finding.get("evidence"):
                raise ValueError(f"{run_directory.name}: finding is missing evidence")

        observations = json.loads((run_directory / "pilot-observations.json").read_text(encoding="utf-8"))
        if not isinstance(observations, list) or len(observations) != 1:
            raise ValueError(f"{run_directory.name}: expected one operational observation")
        if observations[0].get("assessment_id") != assessment.get("assessment_id"):
            raise ValueError(f"{run_directory.name}: observation and assessment identifiers differ")

        regenerated = temporary / f"{run_directory.name}-summary.json"
        run(
            str(ROOT / "scripts" / "aggregate_pilot_metrics.py"),
            "--input",
            str(run_directory / "pilot-observations.json"),
            "--output",
            str(regenerated),
        )
        actual_summary = json.loads((run_directory / "pilot-summary.json").read_text(encoding="utf-8"))
        regenerated_summary = json.loads(regenerated.read_text(encoding="utf-8"))
        if actual_summary != regenerated_summary:
            raise ValueError(f"{run_directory.name}: saved pilot summary is stale")

        entries = json.loads((run_directory / "gl-code-quality-report.json").read_text(encoding="utf-8"))
        if not isinstance(entries, list) or not entries:
            raise ValueError(f"{run_directory.name}: GitLab Code Quality report is empty")
        report = (run_directory / "operational-pilot-report.md").read_text(encoding="utf-8")
        if "advisory" not in report.lower() or "Cohort status" not in report:
            raise ValueError(f"{run_directory.name}: operational report lacks advisory or cohort boundary")


def main() -> None:
    validate_representative_repositories()
    validate_gitlab_yaml_contract()
    with tempfile.TemporaryDirectory(prefix="adder-phase5-") as temporary:
        temporary_path = Path(temporary)
        validate_gitlab_artifacts(temporary_path)
        validate_metrics(temporary_path)
        validate_operational_runs(temporary_path)
    print("Validated Phase 5 fixtures, GitLab artifacts, degraded mode, and pilot metrics.")


if __name__ == "__main__":
    main()
