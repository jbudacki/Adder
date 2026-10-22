# Core decision policy

**Version:** 0.1.0  
**Mode:** Advisory pilot  
**Owner:** Not yet assigned

This policy supports ADDER evaluation and pilot reporting. It does not configure GitLab enforcement or authorize an automated merge, deployment, exception, or external action.

## Block-recommended conditions

Recommend a block when evidence validates one or more of these conditions:

- Exposed credential or private key
- Critical or high-severity vulnerability that meets documented exploitability or blocking criteria
- Known malicious, prohibited, unresolvable, or policy-unverifiable dependency
- Required lockfile update missing
- Required security test failed
- Required Tier 3 human approval missing
- Required artifact integrity or attestation check failed
- Coding-agent activity outside approved permissions

The assessment must identify the evidence, policy condition, corrective action, and owner. A candidate signal or severity label alone is insufficient.

## Manual-review conditions

Require manual review when required evidence or checks are unavailable, material provenance is unverifiable or inconsistent, findings conflict, a candidate finding needs validation, or a novel condition requires AppSec judgment.

If a validated blocking condition and a manual-review condition both exist, `block_recommended` controls the disposition and the uncertainty remains documented.

## Warning conditions

Use a warning for a supported non-blocking issue with a named follow-up, including lower-severity findings outside blocking criteria or provenance gaps not required by the applicable tier.

## Pass conditions

Pass only when all checks and evidence required for the tier are complete, required approvals are present, and no unresolved warning, manual-review, or block condition remains.

## Exceptions

An exception affects the decision only when it has an identifier, authorized approver, exact subject and condition, rationale, compensating controls when required, and an unexpired date. Exceptions do not erase findings. Because the exception owner is not yet assigned, Phase 2 evaluations must not manufacture or self-approve exceptions.

## Degraded operation

An unavailable required skill, evidence source, or authorized execution path results in `manual_review` unless another validated condition already requires `block_recommended`. Enterprise fail-open or fail-closed behavior remains undecided and must not be inferred from this pilot policy.
