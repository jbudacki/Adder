# ADDER delivery roadmap

## Phase 1 — Foundation

Status: **complete in the initial repository scaffold**

- Establish repository governance and contribution boundaries.
- Define the control model, risk tiers, outcomes, and trust boundaries.
- Define shared schemas and skill packaging conventions.
- Add the GitLab README and placeholder branding.
- Record licensing, ownership, and branding decisions still required.

Exit criteria:

- Shared contracts parse successfully.
- The skill template follows Codex naming and frontmatter conventions.
- README clearly distinguishes planned capabilities from implemented ones.
- No external skill is represented as a hidden runtime requirement.

## Phase 2 — Core assurance

Status: **complete in the current repository**

- Created `adder-code-assurance`, `adder-provenance-review`, `adder-change-risk`, and `adder-pr-decision`.
- Added repository-owned routing, provenance, classification, and decision rules.
- Added a risk-classification schema.
- Added fixtures covering all risk tiers and outcomes.

Exit criteria:

- Every Phase 2 skill passes the standalone repository validator and the Codex skill validator in a development environment with its YAML dependency available.
- Shared and Phase 2 JSON schemas parse successfully.
- Core fixtures pass their deterministic validation.
- Required but unavailable Phase 3 reviews cause `manual_review`, not an unsupported pass.

## Phase 3 — Embedded specialist capabilities

Status: **complete in the current repository**

Completed:

- Created ADDER-owned skills for security routing, secure code review, secrets, AWS IAM, network exposure, cryptography, LLM security, dependency hygiene, and threat modeling.
- Embedded local secrets, cryptography, and LLM reconnaissance scanners.
- Folded STRIDE and MAESTRO guidance into `adder-threat-model` without external generator dependencies.
- Added upstream-source attribution and specialist fixtures.
- Preserved candidate-versus-finding gates and explicit authorization boundaries.
- Created `adder-package-trust` for attributable registry, publisher, integrity, malware, reputation, maintenance, and vulnerability evidence.
- Created `adder-test-evidence` for behavior-to-test mapping, assertion strength, negative coverage, regression discrimination, and independence.
- Added skill-specific schemas, positive, blocking, insufficient, and ambiguous evaluations, and router integration.

Exit criteria:

- Package existence is not represented as package safety.
- Name similarity and reputation signals alone cannot produce a blocking recommendation.
- Unavailable or stale required package evidence produces `manual_review`, not a clean result.
- A passing test suite is not sufficient without behavior-level assertions and applicable negative coverage.
- Test evidence that cannot be safely inspected or executed produces `manual_review`.

## Phase 4 — Agent boundaries and recovery

Status: **complete in the current repository**

- Created `adder-agent-boundary` with explicit identity, repository, worktree, filesystem, shell, network, registry, secret, Git, CI/CD, deployment, logging, and attribution controls.
- Created `adder-code-recovery` with containment, minimal correction, rebuild, independent verification, residual-risk, and human-approval gates.
- Added machine-readable agent-boundary and recovery schemas.
- Connected agent-boundary review to the core and LLM-security routers.
- Added fixtures for all boundary statuses and recovery completion invariants.

Exit criteria:

- Demonstrated out-of-bound activity signals `block_recommended`.
- Missing or contradictory boundary evidence signals `manual_review`.
- Recovery cannot be marked `verified` with failed or unperformed required checks.
- Verified Tier 3 recovery requires independent evidence and recorded human approval.
- Recovery planning does not implicitly authorize repository, credential, production, deployment, or external actions.

## Phase 5 — Evaluation and GitLab integration

Status: **complete in the current repository**

- Added representative enterprise-application, infrastructure, and AI-agent repositories with expected routing and outcomes.
- Added an advisory GitLab CI component and merge-request assurance template.
- Added deterministic preparation and rendering of Markdown and GitLab Code Quality reports.
- Added conservative degraded behavior: a missing or invalid assessment produces `manual_review` at Tier 3.
- Added a pilot plan, observation schema, synthetic observations, and deterministic metric aggregation.
- Kept the GitLab job non-blocking and avoided API-driven comments or other externally visible side effects.

Exit criteria:

- Representative scenarios cover application, infrastructure, and agent-specific risk.
- GitLab artifacts are generated without network access or third-party Python packages.
- Missing assessment context cannot produce `pass`.
- Pilot metrics preserve unavailable denominators as `null` rather than representing them as zero.
- Enterprise blocking remains disabled pending separate governance approval and real pilot evidence.

## Phase 6 — Intelligence and release readiness

Status: **complete in the current repository**

- Created `adder-intelligence-loop` with a governed candidate, evaluation, promotion, and retirement lifecycle.
- Added machine-readable intelligence and release-readiness contracts.
- Added lifecycle fixtures and pilot-derived control candidates that cannot self-promote.
- Published release criteria, compatibility limits, operational ownership requirements, pilot evidence, and a build/integrate/buy recommendation.
- Added a deterministic Phase 6 validator and CI integration.
- Recorded the current release decision as `pilot_only`.

Exit criteria:

- Lessons can be represented as attributable, testable control candidates.
- No agent, model, scanner, or skill can approve its own promotion.
- Missing human validation, ownership, representative evidence, or rollback testing prevents mandatory status.
- Compatibility and pilot limitations are explicit rather than inferred as support.
- The release decision distinguishes implementation completion from production or enforcement approval.

Decision: **do not advance ADDER controls to mandatory enforcement.** Continue controlled advisory pilots until the blockers in `docs/release-readiness.md` and `release/readiness.json` are resolved.

## Open foundation decisions

- Final repository owner and GitLab group path
- Approved license and distribution model
- Named AppSec, pipeline, exception, and brand owners
- Final isolated logo and avatar assets
- Versioning and release-signing model
- Supported Codex and host-platform versions
- Approved external registries, intelligence sources, and model providers
