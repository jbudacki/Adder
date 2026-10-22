# Phase 6 release-readiness decision

## Decision

**Pilot only** as of 2026-09-25.

The six planned implementation phases are complete. ADDER is suitable for continued controlled, advisory evaluation. It is not approved for mandatory merge or deployment enforcement, enterprise-wide assurance claims, or external redistribution.

## Evidence supporting pilot use

- The standalone skill portfolio and embedded specialist capabilities are present in the repository.
- Deterministic validators check skill packaging, phase contracts, pilot records, and Phase 6 governance artifacts.
- GitLab advisory artifact generation has been exercised locally.
- Agent boundaries, recovery modes, and human decision points are documented.
- Synthetic evaluation cases and one operational read-only pilot are recorded.
- The intelligence loop records control candidates without allowing autonomous promotion.

## Blocking evidence

- Only one of the three planned operational pilot repositories has been assessed.
- Pilot findings have not received recorded human validation, so precision, recall, severity agreement, and false-positive measurements remain unavailable.
- Provenance detection and package-trust integrations have not been demonstrated against approved authoritative sources.
- A remediation and recovery cycle has not been exercised on a real repository.
- Operational, policy, exception, support, and release owners are not assigned.
- License, distribution, version-signing, and release-integrity decisions are unresolved.
- Compatibility has been tested only on the local macOS/Python environment; a live GitLab pipeline and Linux runner remain unverified.
- Delivery Enablement and AppSec have not approved blocking thresholds or a fail-open/fail-closed policy.

## Allowed use

- Local synthetic evaluation.
- Explicitly approved, read-only repository pilots.
- Advisory findings with human review before action.
- Development and validation of candidate controls.

## Prohibited use

- Mandatory merge, build, deployment, or release blocking.
- Automatic code changes, merges, deployments, or exception approvals.
- Claims that ADDER provides complete provenance or vulnerability coverage.
- External redistribution until licensing and release controls are approved.

The decision must be revisited after the blockers are resolved. The authoritative machine-readable record is `release/readiness.json`.
