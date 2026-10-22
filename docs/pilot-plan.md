# ADDER controlled pilot plan

## Objective

Determine whether ADDER produces useful, accurate, repeatable assurance evidence without unacceptable pipeline delay or developer burden. The pilot is advisory and does not change centrally managed enterprise gates.

## Cohort

Use one approved repository or isolated equivalent from each category:

1. Enterprise application
2. Infrastructure as code
3. AI, agent, or Python application

The synthetic fixtures under `evaluations/representative-repositories/` are suitable for dry runs before real repositories are approved.

## Scenario set

Evaluate authorized seeded or historical examples covering credentials, nonexistent or suspicious dependencies, vulnerable dependencies, missing lockfiles, authorization bypass, wildcard IAM, public exposure, cryptographic misuse, CI workflow risk, inadequate security tests, and coding-agent boundary violations.

Do not introduce live credentials, deploy vulnerable infrastructure, or exercise production attack paths. Prefer synthetic fixtures, isolated environments, and safe proof.

## Execution

1. Capture provenance and human ownership.
2. Classify the change risk tier.
3. Run deterministic repository controls.
4. Run applicable ADDER specialists.
5. Validate candidate findings with human review.
6. Record the advisory PR disposition.
7. Perform authorized remediation and recovery verification for selected cases.
8. Record one pilot observation using `schemas/pilot-observation.schema.json`.

## Metrics

- Provenance coverage
- Confirmed scenario detection rate
- False-positive rate after human validation
- Review elapsed time
- Human review effort
- Risky changes receiving a block recommendation
- Remediation and recovery time
- Reusable controls created
- Pipeline reliability and report-generation failures

Do not report a rate or duration when its denominator or measurement is unavailable; record it as `null`, not zero. Separate synthetic dry-run metrics from measured repository results.

## Decision evidence

The pilot report should identify effective controls, noisy controls, unavailable evidence, controls requiring human judgment, pipeline latency, developer impact, operational ownership, expected cost, and recommended build, buy, or hybrid gaps.

Pilot completion does not authorize mandatory enforcement. It creates the evidence package for Delivery Enablement and DevOps review.
