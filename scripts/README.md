# ADDER scripts

This directory contains repeatable deterministic validation and packaging helpers.

- `validate_core_fixtures.py` checks Phase 2 fixture structure, tier and outcome coverage, and basic decision invariants. It uses only the Python standard library.
- `validate_skills.py` checks ADDER frontmatter, naming, references, and required UI metadata without third-party dependencies.
- `validate_specialist_fixtures.py` checks Phase 3 embedded-specialist fixture coverage and evidence requirements.
- `validate_specialist_scanners.py` smoke-tests secret redaction, cryptographic discovery, and LLM source-line redaction with synthetic temporary inputs.
- `validate_phase3_completion.py` checks package-trust and security-test-evidence decision invariants and outcome coverage.
- `validate_agent_recovery_fixtures.py` checks Phase 4 boundary-status coverage and recovery completion invariants.
- `prepare_advisory_assessment.py` validates a contextual assessment or emits a conservative Tier 3 `manual_review` fallback.
- `render_gitlab_report.py` renders an assessment as a Markdown artifact and GitLab Code Quality JSON without exposing raw evidence.
- `aggregate_pilot_metrics.py` calculates pilot coverage, detection, false-positive, disposition, time, recovery, and control metrics.
- `validate_phase5.py` checks representative fixtures, reporting, degraded behavior, GitLab configuration, and exact pilot metrics.
- `validate_phase6.py` checks intelligence-loop lifecycle cases, pilot-derived control candidates, operational cohort state, and release-readiness blockers.
- `validate_distribution.py` checks portable and Codex-compatible manifests, release-version consistency, all 18 skills, local skill links, and clean-package hygiene.
