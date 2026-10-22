#!/usr/bin/env python3
"""Validate ADDER's portable and Codex-compatible distribution layout."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


EXPECTED_NAME = "adder-ai-code-assurance"
EXPECTED_VERSION = "0.1.0-pre-pilot.1"
SEMVER = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)
LOCAL_LINK = re.compile(r"\[[^]]*\]\(([^)]+)\)")


def load_object(path: Path, errors: list[str]) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        errors.append(f"{path}: invalid or unreadable JSON: {error}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"{path}: expected a JSON object")
        return {}
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("package_root", nargs="?", default=str(Path(__file__).resolve().parents[1]))
    args = parser.parse_args()
    root = Path(args.package_root).resolve()
    errors: list[str] = []

    portable_path = root / "plugin.json"
    compatibility_path = root / ".codex-plugin" / "plugin.json"
    portable = load_object(portable_path, errors)
    compatibility = load_object(compatibility_path, errors)

    for label, manifest in (("portable", portable), ("compatibility", compatibility)):
        if manifest.get("name") != EXPECTED_NAME:
            errors.append(f"{label} manifest name must be {EXPECTED_NAME}")
        version = manifest.get("version")
        if version != EXPECTED_VERSION or not isinstance(version, str) or not SEMVER.fullmatch(version):
            errors.append(f"{label} manifest version must be strict semver {EXPECTED_VERSION}")
        if not isinstance(manifest.get("description"), str) or not manifest.get("description", "").strip():
            errors.append(f"{label} manifest requires a description")
        author = manifest.get("author")
        if not isinstance(author, dict) or not isinstance(author.get("name"), str) or not author["name"].strip():
            errors.append(f"{label} manifest requires author.name")

    if portable.get("$schema") != "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json":
        errors.append("portable manifest must declare the Agent Plugins 1.0.0 schema")
    if compatibility.get("skills") != "./skills/":
        errors.append("compatibility manifest must declare skills as ./skills/")
    for prohibited in ("apps", "mcpServers", "hooks"):
        if prohibited in compatibility:
            errors.append(f"compatibility manifest must not declare absent component: {prohibited}")

    interface = compatibility.get("interface")
    if not isinstance(interface, dict):
        errors.append("compatibility manifest requires interface metadata")
    else:
        for field in (
            "displayName",
            "shortDescription",
            "longDescription",
            "developerName",
            "category",
            "capabilities",
            "defaultPrompt",
        ):
            if not interface.get(field):
                errors.append(f"compatibility interface requires {field}")

    readiness = load_object(root / "release" / "readiness.json", errors)
    if readiness.get("toolkit_version") != EXPECTED_VERSION:
        errors.append("release readiness version does not match plugin manifests")
    if readiness.get("decision") != "pilot_only":
        errors.append("pre-pilot distribution must retain the pilot_only decision")

    skills_root = root / "skills"
    skill_roots = sorted(path for path in skills_root.glob("adder-*") if path.is_dir())
    if len(skill_roots) != 18:
        errors.append(f"expected 18 ADDER skills, found {len(skill_roots)}")
    for skill_root in skill_roots:
        skill_md = skill_root / "SKILL.md"
        if not skill_md.is_file():
            errors.append(f"{skill_root.name}: missing SKILL.md")
            continue
        contents = skill_md.read_text(encoding="utf-8")
        for target in LOCAL_LINK.findall(contents):
            if "://" in target or target.startswith("#"):
                continue
            resolved = (skill_root / target.split("#", 1)[0]).resolve()
            try:
                resolved.relative_to(root)
            except ValueError:
                errors.append(f"{skill_root.name}: link escapes plugin root: {target}")
                continue
            if not resolved.exists():
                errors.append(f"{skill_root.name}: missing linked resource: {target}")

    required = (
        "README.md",
        "INSTALL.md",
        "LICENSE.md",
        "release/PRE-PILOT-NOTES.md",
        "schemas/assessment.schema.json",
        "policies/core-decision-policy.md",
    )
    for relative in required:
        if not (root / relative).is_file():
            errors.append(f"missing distribution file: {relative}")

    forbidden_names = {".DS_Store", "__pycache__"}
    for path in root.rglob("*"):
        if path.name in forbidden_names or path.suffix == ".pyc":
            errors.append(f"forbidden package artifact: {path.relative_to(root)}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Distribution validation passed: {EXPECTED_NAME} {EXPECTED_VERSION}, 18 skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
