# Adder AI Code Assurance

![Adder Image](Adder.png)

Adder is a portable Codex Agent Toolkit for evaluating AI-assisted software changes before they ship.

It combines:

- Change-risk classification
- AI and agent provenance review
- Evidence-based secure code review
- Specialist reviews for secrets, IAM, network exposure, cryptography, LLMs, dependencies, packages, and tests
- Threat modeling and agent-boundary review
- Pull-request disposition recommendations
- Advisory GitLab reporting

Adder produces evidence and recommendations. It does not merge code, deploy software, approve exceptions, or change GitLab settings.

## Name and terminology

**ADDER** stands for **AI-Assisted Development Detection, Evaluation, and Remediation**.

The project uses the following naming convention:

- **Formal name:** Adder AI Code Assurance Toolkit
- **Short name:** Adder
- **Primary Codex skill:** `adder-code-assurance`
- **Toolkit namespace:** `adder-*`
- **Tagline:** *Identify risk before AI-assisted code ships.*

## Adder skills

Adder is a coordinated collection of 18 Codex skills. The skills produce evidence and recommendations; they do not independently merge code, deploy software, approve exceptions, or enforce GitLab policy.

### Core assessment workflow

| Skill | What it does |
| --- | --- |
| `adder-code-assurance` | Orchestrates an end-to-end assessment, consolidates evidence, and produces one normalized advisory outcome. |
| `adder-provenance-review` | Reviews declared ownership, AI assistance, agent activity, artifacts, and attestations without guessing authorship from code style. |
| `adder-change-risk` | Assigns the highest applicable Tier 1, 2, or 3 classification based on changed behavior, assets, trust boundaries, and impact. |
| `adder-pr-decision` | Converts risk, provenance, findings, checks, approvals, and exceptions into `pass`, `warning`, `manual_review`, or `block_recommended`. |

### Security specialist reviews

| Skill | What it does |
| --- | --- |
| `adder-security-review` | Routes security review requests to the relevant ADDER specialists and applies the evidence gate for confirmed findings. |
| `adder-secure-code-review` | Performs source-to-sink analysis of application and infrastructure code, including validation, authorization, error paths, and security-control regressions. |
| `adder-secrets-analysis` | Detects candidate credentials, tokens, private keys, and sensitive configuration while redacting matched values. |
| `adder-iam-security` | Reviews IAM policies, trust relationships, wildcard permissions, public principals, and privilege-escalation paths. |
| `adder-network-exposure` | Reviews public endpoints, load balancers, databases, security groups, and unintended network exposure. |
| `adder-crypto-analysis` | Reviews algorithms, modes, key sizes, nonces, certificates, signing, randomness, and key-management practices. |
| `adder-llm-security` | Reviews LLM, RAG, agent, and tool integrations for prompt injection, unsafe output handling, excessive agency, and secret exposure. |
| `adder-3pp-dependency-hygiene` | Reviews dependency manifests, lockfiles, registries, build sources, version pinning, and dependency-change hygiene. |
| `adder-package-trust` | Separately evaluates package identity, publisher, artifact integrity, vulnerabilities, malware, maintenance, and reputation evidence. |
| `adder-test-evidence` | Determines whether security tests prove the relevant behavior, including negative cases, assertion strength, execution status, and independence. |
| `adder-threat-model` | Routes formal threat modeling to STRIDE for general systems or MAESTRO for agentic AI, RAG, and tool-using systems. |

### Agent safety and recovery

| Skill | What it does |
| --- | --- |
| `adder-agent-boundary` | Reviews coding-agent permissions, repository and worktree scope, shell and network access, credentials, and merge or deployment authority. |
| `adder-code-recovery` | Plans and, when separately authorized, guides containment, correction, rebuild, independent verification, and release-readiness recovery. |

### Governance and continuous improvement

| Skill | What it does |
| --- | --- |
| `adder-intelligence-loop` | Converts validated findings, false positives, remediation evidence, and pilot observations into traceable candidate controls and release evidence. |

Specialist scanners intentionally return candidates rather than automatically declaring vulnerabilities. ADDER requires contextual validation before a scanner or model signal becomes a confirmed finding.


## Status

This is the `0.1.0-pre-pilot.1` pre-pilot release. GitLab integration is advisory only and remains `allow_failure: true`.

Use it for approved read-only pilots, local evaluation, and human-reviewed advisory findings. Do not use it for mandatory merge, build, deployment, or release enforcement.

## Repository layout

```text
skills/       ADDER-owned Codex skills
schemas/      Shared JSON Schema contracts
policies/     Decision and control-promotion policies
scripts/      Deterministic validation and report-generation utilities
examples/     GitLab CI and assessment examples
evaluations/  Synthetic and pilot evaluation fixtures
docs/         Operating, integration, and release guidance
```

## Install and validate

Adder requires a Codex client that supports local plugins and Python 3.9 or later for its validation and reporting scripts. It has no bundled service, MCP server, or package-install step.

From the repository root:

```sh
python3 scripts/validate_skills.py
python3 scripts/validate_core_fixtures.py
python3 scripts/validate_specialist_fixtures.py
python3 scripts/validate_specialist_scanners.py
python3 scripts/validate_phase3_completion.py
python3 scripts/validate_agent_recovery_fixtures.py
python3 scripts/validate_phase5.py
python3 scripts/validate_phase6.py
python3 scripts/validate_distribution.py
```

For local Codex installation instructions, see [INSTALL.md](INSTALL.md).

## GitLab advisory job

The example job prepares an assessment and publishes three artifacts:

- `adder-assessment.json` — normalized assessment data
- `adder-report.md` — human-readable advisory report
- `gl-code-quality-report.json` — GitLab Code Quality annotations for findings with valid file locations

Copy or vendor this project into the target repository, for example at `.adder/`, then include the example job:

```yaml
include:
  - local: ".adder/examples/gitlab/adder-advisory.gitlab-ci.yml"
```

The job expects an optional `adder-input-assessment.json` file. It runs with a conservative degraded mode when that assessment is absent or invalid:

- Risk tier: `3`
- Outcome: `manual_review`
- Missing contextual assessment recorded as an unperformed check

This prevents missing assessment evidence from becoming an accidental pass.

The job runs for merge-request pipelines and the default branch. The default-branch run provides a comparison result for GitLab’s Code Quality view.

See the full [GitLab integration guide](docs/gitlab-integration.md).

## Assessment workflow

Adder follows this sequence:

1. Inventory the change and available evidence.
2. Assign the highest applicable risk tier.
3. Review declared provenance without guessing authorship from code style.
4. Route relevant specialist reviews.
5. Keep unvalidated scanner and model signals as candidates.
6. Normalize confirmed findings.
7. Recommend `pass`, `warning`, `manual_review`, or `block_recommended`.

The final result is advisory. GitLab, repository owners, and authorized human reviewers remain responsible for enforcement and consequential actions.

## Risk tiers

| Tier | Typical change | Required treatment |
| --- | --- | --- |
| 1 | Documentation, comments, low-risk tests | Provenance review and normal checks |
| 2 | Application logic and internal services | ADDER review, automated checks, and human code review |
| 3 | Identity, secrets, cryptography, infrastructure, sensitive data, dependencies, agents, or security controls | Specialist review, independent testing, and human approval |

## Important limitations

- Scanner matches are candidates, not confirmed vulnerabilities.
- Missing provenance is reported as unverifiable; authorship is not inferred from source style.
- Findings without valid repository-relative file paths and line numbers are retained in Markdown but omitted from GitLab Code Quality annotations.
- GitLab API comments and branch-protection changes are not performed.
- Enterprise-wide assurance claims and mandatory enforcement are not approved for this release.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md) and the [skill authoring standard](docs/skill-authoring-standard.md) before changing skills, policies, schemas, or evaluation fixtures.

## License and distribution

Licensing and redistribution terms are not yet approved. Do not redistribute this package or treat its placeholder branding as production-approved. See [LICENSE.md](LICENSE.md) and [release readiness](release/readiness.json).
