# Security test-evidence policy

**Version:** 0.1.0  
**Mode:** Advisory pilot  
**Owner:** Not yet assigned

This policy defines the initial ADDER test-evidence requirements for security-sensitive changes. It does not authorize execution of untrusted repository commands or make test results a merge gate.

## Required evidence

Tier 3 changes must map each material security claim to the actors, protected outcome, allowed and denied states, enforcement layer, applicable tests, and assertions. Evidence must include:

- Positive behavior where applicable
- Negative authorization, isolation, validation, or rejection behavior
- Boundary and malformed input behavior where applicable
- Failure, rollback, cleanup, state-transition, or concurrency behavior where applicable
- Assertions against the protected outcome or durable side effect
- Execution result and environment, or an explicit record that tests were not run
- Independent regression evidence appropriate to the risk for vulnerability corrections

Tier 2 changes require behavior-level tests proportionate to their security effect. Tier 1 test-only changes use normal repository requirements unless they remove, weaken, or replace security evidence.

## Advisory decisions

Test evidence is `sufficient` only when the material claims are covered, assertions prove the relevant outcomes, applicable negative paths are tested, and no unresolved independence issue remains.

Evidence is `insufficient` when a required behavior is demonstrably untested, assertions do not establish the outcome, mocks bypass the control, a security test was removed or weakened without an approved behavior change, or expected values merely reproduce the implementation error.

Require `manual_review` when the behavior, tests, helpers, environment, execution result, or required provenance cannot be established. A passing suite or high line-coverage value is not sufficient by itself.

A failed required security test can support `block_recommended` under `core-decision-policy.md` after determining that the failure is attributable to the assessed product behavior rather than an unrelated environment or fixture failure.

## Execution boundary

Inspect test commands and their scripts before execution. Do not run tests that may access production, use credentials, perform destructive setup, or execute untrusted code outside the user’s authorization. Never weaken a test to obtain a passing result.

Exceptions must satisfy `core-decision-policy.md`; they do not change the underlying test-evidence assessment.
