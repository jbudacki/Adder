# ADDER evaluations

Phase 2 core assurance fixtures are under `core-assurance/`. Phase 3 embedded specialist fixtures are under `specialists/`, with package-trust and test-evidence decision cases under `phase3-completion/`. Phase 4 agent-boundary and recovery fixtures are under `agent-recovery/`.

Phase 5 adds:

- `representative-repositories/` — synthetic enterprise-application, infrastructure, and AI-agent changes with expected routing and outcomes.
- `pilot/` — a synthetic observation dataset and expected aggregate summary for validating the pilot measurement pipeline. These files are examples, not real pilot evidence.

Phase 6 adds `intelligence-loop/`, which tests control promotion and retirement gates and records pilot-derived candidates without treating them as approved controls.

Test behavior, routing, evidence gates, redaction, fallback behavior, and invariants rather than exact prose.
