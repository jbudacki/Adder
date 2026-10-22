#!/usr/bin/env python3
"""Validate ADDER skill packaging without third-party dependencies."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FRONTMATTER_PATTERN = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
REFERENCE_PATTERN = re.compile(r"\[[^\]]+\]\((references/[^)]+)\)")
ALLOWED_FRONTMATTER = {"name", "description", "license", "allowed-tools", "metadata"}


def parse_simple_mapping(text: str, source: Path) -> dict[str, str]:
    """Parse the flat key-value YAML subset used in ADDER frontmatter."""
    result: dict[str, str] = {}
    for number, line in enumerate(text.splitlines(), start=1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith((" ", "\t")) or ":" not in line:
            raise ValueError(f"{source}:{number}: unsupported frontmatter structure")
        key, value = line.split(":", 1)
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
            value = value[1:-1]
        result[key.strip()] = value
    return result


def validate_skill(skill_dir: Path) -> None:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        raise ValueError(f"{skill_dir}: SKILL.md not found")

    content = skill_md.read_text(encoding="utf-8")
    match = FRONTMATTER_PATTERN.match(content)
    if not match:
        raise ValueError(f"{skill_md}: invalid frontmatter delimiters")
    frontmatter = parse_simple_mapping(match.group(1), skill_md)

    unexpected = set(frontmatter) - ALLOWED_FRONTMATTER
    if unexpected:
        raise ValueError(f"{skill_md}: unexpected frontmatter keys: {sorted(unexpected)}")
    name = frontmatter.get("name", "")
    description = frontmatter.get("description", "")
    if not NAME_PATTERN.fullmatch(name) or len(name) > 64:
        raise ValueError(f"{skill_md}: invalid skill name")
    if name != skill_dir.name:
        raise ValueError(f"{skill_md}: skill name does not match directory")
    if not description or len(description) > 1024 or "<" in description or ">" in description:
        raise ValueError(f"{skill_md}: invalid description")
    if "[TODO:" in content:
        raise ValueError(f"{skill_md}: unfinished TODO marker")

    for relative_reference in REFERENCE_PATTERN.findall(content):
        if not (skill_dir / relative_reference).is_file():
            raise ValueError(f"{skill_md}: missing reference {relative_reference}")

    openai_yaml = skill_dir / "agents" / "openai.yaml"
    if not openai_yaml.is_file():
        raise ValueError(f"{skill_dir}: agents/openai.yaml not found")
    interface = openai_yaml.read_text(encoding="utf-8")
    for field in ("display_name", "short_description", "default_prompt"):
        if not re.search(rf"^  {field}:\s+\S", interface, re.MULTILINE):
            raise ValueError(f"{openai_yaml}: missing interface.{field}")
    if f"${name}" not in interface:
        raise ValueError(f"{openai_yaml}: default prompt must mention ${name}")


def main() -> None:
    skill_dirs = sorted(path for path in SKILLS.glob("adder-*") if path.is_dir())
    if not skill_dirs:
        raise ValueError("no ADDER skill directories found")
    for skill_dir in skill_dirs:
        validate_skill(skill_dir)
    print(f"Validated {len(skill_dirs)} ADDER skill packages.")


if __name__ == "__main__":
    main()

