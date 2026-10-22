#!/usr/bin/env python3
"""Aggregate synthetic or measured ADDER pilot observations."""

from __future__ import annotations

import argparse
import json
import statistics
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any


REPOSITORY_TYPES = {"enterprise_application", "infrastructure", "ai_agent"}
NULLABLE_INTEGER_FIELDS = {
    "seeded_or_validated_scenarios",
    "confirmed_scenarios_detected",
    "findings_reviewed",
    "false_positives",
    "risky_changes",
    "risky_changes_block_recommended",
    "reusable_controls_created",
}
NULLABLE_REQUIRED_NUMBER_FIELDS = {"review_minutes", "human_review_minutes"}
OPTIONAL_NUMBER_FIELDS = {"remediation_minutes", "recovery_minutes"}
OPTIONAL_FIELDS = OPTIONAL_NUMBER_FIELDS | {"repository_reference", "notes"}
REQUIRED_FIELDS = {
    "schema_version",
    "observation_id",
    "repository_type",
    "assessment_id",
    "provenance_verifiable",
    "observed_at",
} | NULLABLE_INTEGER_FIELDS | NULLABLE_REQUIRED_NUMBER_FIELDS
ALLOWED_FIELDS = REQUIRED_FIELDS | OPTIONAL_FIELDS


def rate(numerator: float | None, denominator: float | None) -> float | None:
    return round(numerator / denominator, 4) if numerator is not None and denominator else None


def average(values: list[float]) -> float | None:
    return round(statistics.fmean(values), 2) if values else None


def sum_available(observations: list[dict[str, Any]], field: str) -> int | float | None:
    values = [item[field] for item in observations if item[field] is not None]
    return sum(values) if values else None


def load_observations(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list) or not data:
        raise ValueError("pilot observations must be a non-empty JSON array")
    identifiers: set[str] = set()
    for observation in data:
        if not isinstance(observation, dict):
            raise ValueError("each pilot observation must be an object")
        missing = sorted(REQUIRED_FIELDS - set(observation))
        unknown = sorted(set(observation) - ALLOWED_FIELDS)
        if missing:
            raise ValueError(f"pilot observation is missing required fields: {', '.join(missing)}")
        if unknown:
            raise ValueError(f"pilot observation contains unknown fields: {', '.join(unknown)}")
        identifier = observation.get("observation_id")
        if not isinstance(identifier, str) or not identifier or identifier in identifiers:
            raise ValueError(f"invalid or duplicate observation_id: {identifier!r}")
        identifiers.add(identifier)
        if observation.get("schema_version") != "1.0.0":
            raise ValueError(f"{identifier}: unsupported schema_version")
        if observation.get("repository_type") not in REPOSITORY_TYPES:
            raise ValueError(f"{identifier}: invalid repository_type")
        if not isinstance(observation.get("assessment_id"), str) or not observation["assessment_id"]:
            raise ValueError(f"{identifier}: assessment_id must be a non-empty string")
        if not isinstance(observation.get("provenance_verifiable"), bool):
            raise ValueError(f"{identifier}: provenance_verifiable must be boolean")
        for field in NULLABLE_INTEGER_FIELDS:
            value = observation.get(field)
            if value is not None and (not isinstance(value, int) or isinstance(value, bool) or value < 0):
                raise ValueError(f"{identifier}: {field} must be null or a non-negative integer")
        for field in NULLABLE_REQUIRED_NUMBER_FIELDS:
            value = observation.get(field)
            if value is not None and (not isinstance(value, (int, float)) or isinstance(value, bool) or value < 0):
                raise ValueError(f"{identifier}: {field} must be null or a non-negative number")
        for field in OPTIONAL_NUMBER_FIELDS:
            value = observation.get(field)
            if value is not None and (not isinstance(value, (int, float)) or isinstance(value, bool) or value < 0):
                raise ValueError(f"{identifier}: {field} must be null or a non-negative number")
        notes = observation.get("notes")
        if notes is not None and (not isinstance(notes, list) or not all(isinstance(item, str) for item in notes)):
            raise ValueError(f"{identifier}: notes must be an array of strings")
        observed_at = observation.get("observed_at")
        if not isinstance(observed_at, str):
            raise ValueError(f"{identifier}: observed_at must be an ISO 8601 date-time")
        try:
            parsed_time = datetime.fromisoformat(observed_at.replace("Z", "+00:00"))
        except ValueError as error:
            raise ValueError(f"{identifier}: observed_at must be an ISO 8601 date-time") from error
        if parsed_time.tzinfo is None:
            raise ValueError(f"{identifier}: observed_at must include a timezone")
        if (
            observation["confirmed_scenarios_detected"] is not None
            and observation["seeded_or_validated_scenarios"] is not None
            and observation["confirmed_scenarios_detected"] > observation["seeded_or_validated_scenarios"]
        ):
            raise ValueError(f"{identifier}: detected scenarios exceed known scenarios")
        if (
            observation["false_positives"] is not None
            and observation["findings_reviewed"] is not None
            and observation["false_positives"] > observation["findings_reviewed"]
        ):
            raise ValueError(f"{identifier}: false positives exceed reviewed findings")
        if (
            observation["risky_changes_block_recommended"] is not None
            and observation["risky_changes"] is not None
            and observation["risky_changes_block_recommended"] > observation["risky_changes"]
        ):
            raise ValueError(f"{identifier}: block recommendations exceed risky changes")
    return data


def aggregate(observations: list[dict[str, Any]]) -> dict[str, Any]:
    total_scenarios = sum_available(observations, "seeded_or_validated_scenarios")
    detected = sum_available(observations, "confirmed_scenarios_detected")
    findings_reviewed = sum_available(observations, "findings_reviewed")
    false_positives = sum_available(observations, "false_positives")
    risky_changes = sum_available(observations, "risky_changes")
    risky_blocked = sum_available(observations, "risky_changes_block_recommended")
    remediation = [float(item["remediation_minutes"]) for item in observations if item.get("remediation_minutes") is not None]
    recovery = [float(item["recovery_minutes"]) for item in observations if item.get("recovery_minutes") is not None]
    repo_counts = Counter(item["repository_type"] for item in observations)
    return {
        "schema_version": "1.0.0",
        "observation_count": len(observations),
        "repository_type_counts": {key: repo_counts.get(key, 0) for key in sorted(REPOSITORY_TYPES)},
        "provenance_coverage": rate(sum(item["provenance_verifiable"] for item in observations), len(observations)),
        "scenario_detection_rate": rate(detected, total_scenarios),
        "false_positive_rate": rate(false_positives, findings_reviewed),
        "risky_change_block_recommendation_rate": rate(risky_blocked, risky_changes),
        "average_review_minutes": average([
            float(item["review_minutes"]) for item in observations if item["review_minutes"] is not None
        ]),
        "average_human_review_minutes": average([
            float(item["human_review_minutes"])
            for item in observations
            if item["human_review_minutes"] is not None
        ]),
        "average_remediation_minutes": average(remediation),
        "average_recovery_minutes": average(recovery),
        "reusable_controls_created": sum(item["reusable_controls_created"] for item in observations),
        "totals": {
            "seeded_or_validated_scenarios": total_scenarios,
            "confirmed_scenarios_detected": detected,
            "findings_reviewed": findings_reviewed,
            "false_positives": false_positives,
            "risky_changes": risky_changes,
            "risky_changes_block_recommended": risky_blocked,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Aggregate ADDER pilot observations")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    observations = load_observations(Path(args.input))
    summary = aggregate(observations)
    Path(args.output).write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(f"Aggregated {len(observations)} pilot observations.")


if __name__ == "__main__":
    main()
