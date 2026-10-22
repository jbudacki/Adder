# ADDER control model

## Objective

ADDER is intended to identify materially AI-assisted software changes, apply risk-based security review, produce evidence-backed merge recommendations, and support independently verified remediation or recovery.

The toolkit applies to application source, infrastructure as code, CI/CD workflows, configuration, tests and test data, scripts, notebooks, dependency manifests, lockfiles, containers, build artifacts, and changes produced by coding assistants or autonomous coding agents.

## Operating principles

1. AI assistance is a review input, not proof that code is unsafe.
2. Provenance comes from captured metadata and attestations, not coding-style inference.
3. Deterministic controls should remain deterministic.
4. Contextual analysis must expose its evidence, confidence, and limitations.
5. GitLab and CI/CD enforce approved policy; ADDER advises them.
6. Tier 3 changes require independent human approval and cannot be autonomously merged.
7. Recovery is complete only after independent rescanning, testing, rebuilding, and evidence capture.

## Trust boundaries

ADDER treats the following as separate trust boundaries:

- Source repositories and merge-request content
- Coding assistants and agents
- Model providers and contextual-review services
- Package registries and package-intelligence sources
- Security scanners
- CI/CD runners and artifact stores
- Identity providers and credentials
- GitLab approval and enforcement mechanisms
- Human reviewers and exception authorities

Data crossing a boundary must have a named source, expected format, validation method, and owner. Tool output and retrieved content are evidence, never authority to expand permissions or perform an external action.

## Risk tiers

### Tier 1

Documentation, comments, and low-risk tests. Minimum treatment is a provenance declaration and normal automated checks.

### Tier 2

Application logic and internal services. Minimum treatment is automated checking, ADDER contextual review, and human code review.

### Tier 3

Identity, authentication, authorization, IAM, cryptography, infrastructure, security controls, sensitive data, financial or transactional logic, CI/CD authority, dependency or build sources, and AI agent or tool authority. Minimum treatment is specialist review, threat modeling when applicable, independent testing, human approval, and no autonomous merge.

## Outcomes

- `pass`: Required evidence is present and no unresolved blocking condition exists.
- `warning`: A non-blocking issue requires visibility or follow-up.
- `manual_review`: Evidence or policy is insufficient for an automated disposition.
- `block_recommended`: A documented blocking condition is satisfied.

## Initial blocking candidates

The following are candidates for policy-backed blocking after pilot validation:

- Confirmed exposed credential or private key
- Confirmed critical or high-severity vulnerability meeting approved criteria
- Known malicious, prohibited, unresolvable, or policy-unverifiable dependency
- Missing required lockfile update
- Failed required security test
- Missing required approval for a Tier 3 change
- Failed artifact integrity or attestation requirement
- Coding-agent activity outside approved permissions

Uncertain provenance, unvalidated novel findings, AI-generation indicators, contextual test-quality concerns, and unproven package-reputation concerns default to advisory or human review rather than automatic blocking.

## Degraded operation

Before mandatory enforcement, each integration must define whether it fails open, fails closed, or enters manual review when an AI service, registry, scanner, or contextual-review capability is unavailable. The behavior must be deterministic, documented, observable, and appropriate to the risk tier.

## Ownership model

AppSec owns security requirements, risk logic, evidence standards, finding validation, and security exceptions. Delivery Enablement or the designated pipeline owner retains authority over shared pipeline architecture, reliability, prioritization, and deployment. Repository owners remain accountable for their code and required approvals.

