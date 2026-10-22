# ADDER operational pilot report

## Decision

**Advisory outcome:** `block_recommended`  
**Risk tier:** `3`  
**Provenance:** `unverifiable`  
**Target:** Supplied local Syn Reality Avatar source snapshot  
**Review mode:** Static, read-only, no network or live-system validation

This outcome is controlled by validated high-severity application authorization, RAG corpus-integrity, provider-token, and CI/CD supply-chain conditions. It is advisory and does not configure a GitLab gate or assert that the reviewed snapshot is deployed.

## Scope and method

The pilot exercised repository-owned ADDER routing, provenance, risk classification, secure code review, secrets analysis, LLM security, dependency hygiene, package-trust fallback, test-evidence assessment, split STRIDE/MAESTRO threat modeling, PR decision logic, GitLab report rendering, and pilot metric aggregation.

The target was supplied as a directory without `.git` metadata. Accordingly, this is a whole-snapshot assessment rather than a diff, commit, or merge-request review. The target was not modified. No service was started, no dependency was installed, no credential was validated, and no external API, registry, cloud account, or production environment was contacted.

## Results

| ID | Severity | Result |
| --- | --- | --- |
| `ADDER-AUTH-001` | High | Sensitive reporting, ingestion, document, job, session, and generation routes lack application authentication and operation-level authorization. |
| `ADDER-LLM-001` | High | Unauthenticated upload and activation can place caller-controlled content into model retrieval context. |
| `ADDER-TOKEN-001` | High | A public-facing server route can use a server-held key to mint and return provider session tokens without caller authorization. |
| `ADDER-CICD-001` | High | Deployment jobs execute mutable remote inputs and promote mutable image tags in credentialed deployment workflows. |
| `ADDER-SECRET-001` | Medium | Session and JWT signing controls silently accept fixed fallback secrets when environment configuration is absent. |
| `ADDER-LOG-001` | Medium | Questions, model responses, and retrieved document content can enter operational logs. |
| `ADDER-TEST-001` | Medium | Tier 3 behaviors lack executable behavior-level security tests in the supplied snapshot. |

Two credential-shaped scanner candidates were resolved during agent review as environment-composed database strings rather than embedded credentials. This demonstrates the candidate-to-finding gate, but they are not counted in pilot accuracy metrics until a human reviewer confirms the disposition. Raw candidate values were not retained.

## Dependency and package evidence

All three Node.js applications have lockfile version 3 files. Across the lockfiles, 2,537 resolved entries use the standard npm registry and include integrity values; no Git, file, or alternate resolved sources were identified by the offline check.

This is hygiene evidence, not package trust. Package existence, publisher identity, current vulnerability status, malware status, maintenance, reputation, registry approval, container-image integrity, and provenance were not checked because no approved external access or enterprise intelligence source was supplied. ADDER therefore records package trust as `manual_review`, not verified.

## Test evidence

No package manifest defines a test script. The only two discovered test files cover welcome and not-found responses and import a path absent from the supplied snapshot. Authentication, authorization, RAG corpus integrity, provider-token issuance, logging, and deployment behavior have no demonstrated tests. Tests were not run because dependencies were absent, there was no approved command, and the target remained read-only.

## Pilot measurements

- Provenance coverage: `0%` for this observation
- Scenario detection rate: unavailable pending human validation
- False-positive rate: unavailable pending human validation
- Review duration: unavailable; recorded as `null`
- Human review effort: unavailable; recorded as `null`
- Change-level block rate: unavailable because this was a snapshot, not a change
- Reusable controls created: `1` — pilot metrics now preserve unavailable durations as `null`

These values describe one AI/RAG application snapshot and must not be generalized into toolkit accuracy or enterprise readiness.

## Required next actions

1. Confirm whether an upstream gateway protects every route and obtain the Git-backed repository revision and deployment architecture.
2. Add application authentication and per-operation roles or ownership checks before sensitive data and mutations.
3. Require authorized corpus ingestion, human-reviewed promotion, provenance, integrity, and injection-focused evaluation.
4. Protect provider-token issuance with identity, allowlists, quotas, and rate limits.
5. Replace mutable CI inputs and image tags with verified immutable artifacts.
6. Remove fallback signing secrets and content-bearing logs.
7. Add executable security tests and repeat the assessment on a merge request with approved package intelligence.

## Cohort status

This completes one partial operational-pilot observation in the AI/RAG application category. The enterprise-application and infrastructure cohort slots remain open, and no production-readiness decision should be made from this single observation.
