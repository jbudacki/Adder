# ADDER skill authoring standard

## Goal

Every ADDER skill must be portable, discoverable, evidence-driven, and usable from a clean checkout without relying on separately installed specialist skills.

## Required layout

```text
skills/<skill-name>/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/      Optional; conditional detail only
├── scripts/         Optional; repeatable deterministic operations only
└── assets/          Optional; files used in generated output
```

Only `SKILL.md` is universally required. Create optional directories only when the skill actually needs them.

## Naming

- Use lowercase letters, digits, and hyphens.
- Prefix every toolkit-owned skill with `adder-`.
- Keep names shorter than 64 characters.
- The directory name and frontmatter `name` must match.

## Entrypoint contract

`SKILL.md` must contain YAML frontmatter with a concise, discriminating `name` and `description`. Its body should define:

- The outcome the skill produces
- When it applies and meaningful routing boundaries
- Required evidence and relevant trust boundaries
- The decision process or workflow
- Output fields and applicable shared schemas
- Limitations and conditions requiring human review
- References to conditional supporting material

Do not include generic coding advice, claim permissions the user did not grant, or treat retrieved content and model output as instructions.

## Evidence requirements

A security finding must identify, when applicable:

- Affected file, artifact, or policy object
- Entry point or evidence source
- Source-to-sink or control path
- Trust boundary
- Preconditions
- Impact and exploitability notes
- False-positive considerations
- Recommended correction
- Verification performed
- Confidence and open questions

If the evidence cannot support a finding or provenance claim, return uncertainty or `manual_review`; do not manufacture certainty.

## Shared outputs

- Findings conform to `schemas/finding.schema.json`.
- Provenance records conform to `schemas/provenance.schema.json`.
- Consolidated assessments conform to `schemas/assessment.schema.json`.
- Artifact attestations conform to `schemas/attestation.schema.json`.

Skill-specific extensions must use a documented namespaced field or a separately versioned schema. A skill must not silently change the meaning of a shared enum or required field.

## UI metadata

Use `agents/openai.yaml` for `display_name`, `short_description`, and `default_prompt`. Keep these values consistent with `SKILL.md`. Automatic discovery remains enabled unless repository owners explicitly decide otherwise.

## Scripts and network access

Scripts should make repeated deterministic work safer or more reliable. They must fail with actionable errors, avoid printing secrets, and document external writes or network access. A new network dependency requires an identified credential source, data-handling boundary, failure mode, and owner.

## Validation

For each new or materially changed skill:

1. Run the Codex skill validator.
2. Validate any JSON or YAML resources.
3. Execute deterministic scripts against representative safe fixtures.
4. Run realistic positive, negative, and ambiguous evaluation cases.
5. Confirm the skill does not imply autonomous merge, deployment, exception approval, or destructive remediation.

Use `templates/skill/` as the maintained starting point. Replace all template markers before validation.

