# GitLab advisory integration

## Scope

Phase 5 provides advisory reporting only. It does not configure branch protection, approval rules, security policies, merge blocking, deployment gates, or GitLab API writes.

The example uses GitLab's directly imported Code Quality JSON format rather than the deprecated CodeClimate template. GitLab requires a JSON array containing `description`, `check_name`, `fingerprint`, `severity`, and a repository-relative path and line. See the official [Code Quality documentation](https://docs.gitlab.com/ci/testing/code_quality/) and [artifact report reference](https://docs.gitlab.com/ci/yaml/artifacts_reports/).

## Prerequisites

- A GitLab runner with Python 3 available
- ADDER vendored or otherwise made available inside the job workspace
- An approved mechanism that produces `adder-input-assessment.json`, when contextual assessment is available
- Repository owners who understand that this integration is advisory

No container image is prescribed by ADDER. Projects should use their approved runner or a version- and digest-controlled image under their dependency policy.

## Install the example

One pilot option is to vendor ADDER at `.adder/` and include the example:

```yaml
include:
  - local: ".adder/examples/gitlab/adder-advisory.gitlab-ci.yml"
```

If ADDER is stored elsewhere, override `ADDER_ROOT`. The included job runs for merge-request pipelines and the default branch. Running on the default branch provides a comparison report for merge requests; GitLab's Code Quality view compares source and target results.

## Artifacts

The job publishes:

- `adder-assessment.json` — normalized input or degraded-mode assessment
- `adder-report.md` — human-readable report exposed from the merge request
- `gl-code-quality-report.json` — findings with valid repository-relative locations

Findings without a valid path and line remain in the Markdown assessment but are omitted from Code Quality JSON because GitLab requires both fields. Reports avoid raw evidence values and do not include credential material.

## Degraded operation

| Condition | Advisory behavior |
| --- | --- |
| Contextual assessment is absent | Generate `manual_review` with conservative Tier 3 classification and name the missing check |
| Assessment JSON is malformed | Generate `manual_review` and record that supplied evidence was invalid |
| Finding lacks a valid location | Keep it in Markdown; omit it from Code Quality annotations |
| Renderer or runner fails | Job may fail but remains `allow_failure: true`; investigate the job rather than treating absence as a pass |
| GitLab cannot display Code Quality | Retain downloadable JSON and Markdown artifacts |

The job must not convert an unavailable service into `pass`. Future mandatory behavior must define risk-tier-specific fail-open, fail-closed, or manual-review handling with Delivery Enablement and DevOps.

## Merge-request comments

Phase 5 does not post comments through the GitLab API. The exposed Markdown artifact and Code Quality report avoid requiring a write token. A future commenting integration would require a dedicated scoped identity, retention and redaction controls, idempotency, and explicit authorization for externally visible writes.

## Promotion criteria

Do not remove `allow_failure: true` until the pilot establishes acceptable accuracy, false-positive rate, latency, reliability, fallback behavior, developer experience, ownership, support, and exception handling. GitLab supports rule-level and job-level `allow_failure`; see the official [CI/CD YAML reference](https://docs.gitlab.com/ci/yaml/).

