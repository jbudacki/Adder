# Contributing to ADDER

ADDER is evidence-driven security tooling. Contributions should improve a defined control, reduce ambiguity, or add verified coverage without expanding authority implicitly.

## Before changing the toolkit

1. Identify the control objective or failure mode being addressed.
2. Inspect the shared schemas and the skills that consume the affected output.
3. Make the smallest coherent change.
4. Add or update a realistic evaluation case.
5. Run schema, skill, and fixture validation relevant to the change.
6. Document limitations, unresolved assumptions, and external dependencies.

## Pull requests

A merge request should state:

- The control or behavior changed.
- Why the change is needed.
- Evidence and evaluation cases used.
- Validation performed.
- Compatibility or migration impact.
- New trust boundaries, network calls, data handling, or dependencies.
- Remaining limitations.

Changes to shared schemas, blocking logic, exceptions, or Tier 3 treatment require review by the designated AppSec owner. The placeholder owner in `.gitlab/CODEOWNERS` must be replaced before GitLab approval rules are enabled.

## Skill contributions

Follow [the skill authoring standard](docs/skill-authoring-standard.md). Do not duplicate generic Codex guidance. Preserve evidence requirements, authorization boundaries, and honest uncertainty.

