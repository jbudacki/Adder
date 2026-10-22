# ADDER release criteria

ADDER uses four release decisions. A decision applies to the evidence available at the time of review; it is not a permanent certification of the toolkit.

## Decision levels

### Not ready

Use when the toolkit cannot be run safely or repeatably in the intended environment. Required schemas, validation, operating boundaries, or recovery guidance may be missing.

### Pilot only

Use when the toolkit is suitable for controlled evaluation but the evidence is not representative enough for routine use. Pilot-only use must be read-only or advisory, explicitly scoped, and reviewed by a human.

Minimum evidence:

- Required skills, policies, schemas, and deterministic validators are present.
- Findings identify evidence, confidence, limitations, and a recommended disposition.
- Agent permissions and recovery boundaries are documented.
- Pilot participants understand that results are not an enterprise assurance claim.

### Advisory ready

Use when ADDER can produce non-blocking findings for a defined population of repositories.

Minimum evidence:

- A representative pilot cohort covers the approved technology and risk scope.
- Human review has measured true positives, false positives, severity agreement, and material misses.
- Runtime, reliability, and operating-cost measurements are acceptable.
- Repository, policy, exception, support, and release owners are named.
- Compatibility limits and unsupported environments are published.
- Package provenance, license, versioning, and distribution controls are approved.
- Recovery and remediation paths have been exercised.

### Mandatory ready

Use only when a named authority approves ADDER to block a merge, deployment, or release within a precisely defined scope.

In addition to all advisory-ready evidence:

- Each blocking control has positive, negative, ambiguous, and rollback test cases.
- Blocking thresholds and exception paths are approved by AppSec and Delivery Enablement.
- The false-positive rate and time-to-resolution are acceptable to affected engineering owners.
- Bypass, outage, and degraded-mode procedures have been tested.
- Control ownership, review cadence, and retirement criteria are recorded.
- The exact release is signed or otherwise protected by approved integrity controls.

## Decision rules

- No model, agent, scanner, or skill may approve its own promotion.
- Evidence from one repository cannot justify general enforcement. It may support a narrowly scoped control candidate.
- Unknown evidence is not treated as passing evidence.
- An unresolved owner blocks advisory and mandatory release.
- A material false positive pauses promotion until a negative fixture and tuning decision exist.
- A material missed finding pauses promotion until the root cause and regression evidence exist.
- Mandatory controls must fail predictably and have a tested rollback path.

The machine-readable current decision is maintained in `release/readiness.json` and checked by `scripts/validate_phase6.py`.
