# ADDER control promotion policy

**Version:** 0.1.0  
**Mode:** Advisory pilot  
**Owner:** Not yet assigned

This policy governs how findings, false positives, misses, remediation, recovery, and operational feedback become reusable ADDER controls. It does not itself authorize GitLab enforcement or production changes.

## Lifecycle

1. `candidate` — a traceable lesson and proposed control exist.
2. `evaluating` — positive, negative, ambiguous, and rollback cases are being tested.
3. `advisory` — the control has a named scope, owner, version, safe failure mode, fixtures, monitoring plan, and rollback trigger.
4. `mandatory` — representative operational evidence, approved performance thresholds, exception handling, support, and enforcement approval are complete.
5. `rejected` — evidence does not justify the control or expected harm exceeds benefit.
6. `retired` — the control is obsolete, replaced, unsupported, or no longer trustworthy.

Every transition must preserve the previous state, evidence, approver, effective date, and rollback path.

## Candidate requirements

A candidate must cite at least one source assessment or observation, distinguish human and agent validation, identify the generalized root cause, name its applicability and exclusions, and define at least one meaningful validation case. Raw model output or a scanner match without disposition is insufficient.

## Advisory promotion

Promotion to advisory requires:

- Named control owner and support path
- Explicit scope, exclusions, version, and compatibility assumptions
- Positive, negative, and ambiguous fixtures
- Evidence that secret or sensitive data is not exposed by the control
- Deterministic degraded behavior
- Monitoring signal and rollback trigger
- AppSec approval

## Mandatory promotion

Promotion to mandatory additionally requires:

- A complete representative pilot cohort or an explicitly approved narrower scope
- Human-validated detection and false-positive evidence against approved thresholds
- Measured latency, reliability, developer effort, and operational cost
- Tested remediation, rollback, and recovery
- Named pipeline, exception, support, and incident owners
- Approved license, release version, compatibility statement, and signed distribution process
- Delivery Enablement or DevOps approval for the enforcement mechanism
- No unresolved critical governance blocker

An LLM, agent, skill, or scanner cannot self-approve mandatory promotion. Missing evidence remains `unknown` or `not_met`; it is never inferred as satisfied.

## Tuning and retirement

Confirmed false positives require a negative regression case and the narrowest supported rule change. Do not suppress an entire file, repository, or category when an evidence gate can distinguish the condition.

Retirement requires a replacement or risk disposition, owner approval, communication plan, and preservation of historical evidence. Emergency disablement may precede full retirement when the control causes material harm, but must be recorded and reviewed.
