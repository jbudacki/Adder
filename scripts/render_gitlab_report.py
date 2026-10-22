#!/usr/bin/env python3
"""Render an ADDER assessment as Markdown and GitLab Code Quality JSON."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path, PurePosixPath
from typing import Any


SEVERITY_MAP = {
    "critical": "blocker",
    "high": "critical",
    "medium": "major",
    "low": "minor",
    "informational": "info",
}


def load_assessment(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("findings"), list):
        raise ValueError("assessment must be an object with a findings list")
    return data


def safe_text(value: Any) -> str:
    return str(value if value is not None else "").replace("\n", " ").replace("|", "\\|").strip()


def valid_gitlab_location(location: Any) -> tuple[str, int] | None:
    if not isinstance(location, dict):
        return None
    path = location.get("path")
    line = location.get("line")
    if not isinstance(path, str) or not isinstance(line, int) or line < 1:
        return None
    pure_path = PurePosixPath(path.removeprefix("./"))
    if pure_path.is_absolute() or ".." in pure_path.parts or not pure_path.parts:
        return None
    return str(pure_path), line


def code_quality_entries(assessment: dict[str, Any]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for finding in assessment.get("findings", []):
        if not isinstance(finding, dict):
            continue
        finding_id = safe_text(finding.get("finding_id", "unknown-finding"))
        title = safe_text(finding.get("title", "ADDER finding"))
        category = safe_text(finding.get("category", "adder"))
        severity = SEVERITY_MAP.get(str(finding.get("severity", "informational")), "info")
        recommendation = safe_text(finding.get("recommendation"))
        description = title if not recommendation else f"{title} — {recommendation}"
        for raw_location in finding.get("affected_locations", []):
            location = valid_gitlab_location(raw_location)
            if location is None:
                continue
            path, line = location
            fingerprint_source = f"{finding_id}|{path}|{line}".encode("utf-8")
            entries.append({
                "description": description,
                "check_name": f"ADDER {category}",
                "fingerprint": hashlib.sha256(fingerprint_source).hexdigest(),
                "severity": severity,
                "location": {"path": path, "lines": {"begin": line}},
            })
    return entries


def markdown_report(assessment: dict[str, Any], visible_entries: int) -> str:
    findings = [item for item in assessment.get("findings", []) if isinstance(item, dict)]
    severity_counts = Counter(str(item.get("severity", "informational")) for item in findings)
    lines = [
        "# ADDER advisory assessment",
        "",
        f"- Outcome: `{safe_text(assessment.get('outcome', 'unknown'))}`",
        f"- Risk tier: `{safe_text(assessment.get('risk_tier', 'unknown'))}`",
        f"- Assessment: `{safe_text(assessment.get('assessment_id', 'unknown'))}`",
        f"- Findings: `{len(findings)}`",
        f"- Findings represented in GitLab Code Quality: `{visible_entries}`",
        "",
        "> Advisory only: this report does not merge, block, deploy, approve an exception, or change production state.",
        "",
    ]
    if severity_counts:
        lines.extend(["## Severity summary", ""])
        for severity in ("critical", "high", "medium", "low", "informational"):
            if severity_counts.get(severity):
                lines.append(f"- {severity}: {severity_counts[severity]}")
        lines.append("")

    lines.extend(["## Findings", ""])
    if not findings:
        lines.extend(["No normalized findings were supplied.", ""])
    for finding in findings:
        lines.extend([
            f"### {safe_text(finding.get('title', 'Untitled finding'))}",
            "",
            f"- Severity: `{safe_text(finding.get('severity', 'unknown'))}`",
            f"- Confidence: `{safe_text(finding.get('confidence', 'unknown'))}`",
            f"- Status: `{safe_text(finding.get('status', 'unknown'))}`",
            f"- Impact: {safe_text(finding.get('impact', 'Not provided'))}",
            f"- Recommendation: {safe_text(finding.get('recommendation', 'Not provided'))}",
            "",
        ])

    for heading, key in (
        ("Required actions", "required_actions"),
        ("Required approvals", "required_approvals"),
        ("Checks not performed", "checks_not_performed"),
        ("Limitations", "limitations"),
    ):
        values = assessment.get(key, [])
        if isinstance(values, list) and values:
            lines.extend([f"## {heading}", ""])
            lines.extend(f"- {safe_text(value)}" for value in values)
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Render ADDER GitLab advisory artifacts")
    parser.add_argument("--assessment", required=True)
    parser.add_argument("--markdown", required=True)
    parser.add_argument("--codequality", required=True)
    args = parser.parse_args()

    assessment = load_assessment(Path(args.assessment))
    entries = code_quality_entries(assessment)
    Path(args.codequality).write_text(json.dumps(entries, indent=2) + "\n", encoding="utf-8")
    Path(args.markdown).write_text(markdown_report(assessment, len(entries)), encoding="utf-8")
    print(f"Rendered {len(entries)} GitLab Code Quality entries from {len(assessment.get('findings', []))} findings.")


if __name__ == "__main__":
    main()

