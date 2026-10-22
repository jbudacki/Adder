# ADDER advisory assessment

- Outcome: `block_recommended`
- Risk tier: `3`
- Assessment: `pilot-syn-reality-avatar-20260925`
- Findings: `7`
- Findings represented in GitLab Code Quality: `22`

> Advisory only: this report does not merge, block, deploy, approve an exception, or change production state.

## Severity summary

- high: 4
- medium: 3

## Findings

### Administrative and sensitive API operations lack application authorization

- Severity: `high`
- Confidence: `high`
- Status: `validated`
- Impact: An unauthenticated caller can potentially read conversation records and manipulate uploaded knowledge, document state, or administrative jobs.
- Recommendation: Require authenticated identities and server-side role or ownership checks at each sensitive operation; deny by default and independently test unauthorized roles.

### Unauthenticated callers can place and activate content used as LLM retrieval context

- Severity: `high`
- Confidence: `high`
- Status: `validated`
- Impact: A caller can poison the active knowledge base and influence model responses shown to users, undermining content integrity and potentially exposing retrieved information through crafted instructions.
- Recommendation: Restrict ingestion and activation to approved roles, separate upload from reviewed promotion, validate corpus provenance and integrity, and treat retrieved text strictly as data with injection-focused evaluations.

### Provider session tokens can be minted without an application authorization check

- Severity: `high`
- Confidence: `high`
- Status: `validated`
- Impact: Unauthorized users can consume provider sessions, incur cost, exhaust quota, or use unapproved avatar and voice combinations.
- Recommendation: Authenticate the caller, enforce server-side avatar and voice allowlists, apply per-user authorization and rate limits, and avoid returning provider error bodies verbatim.

### Deployment jobs execute unpinned remote code and promote mutable artifacts

- Severity: `high`
- Confidence: `high`
- Status: `validated`
- Impact: Compromised upstream content can execute in the deployment job, access CI material, alter downloaded credential files or artifacts, and affect production deployment.
- Recommendation: Pin and verify the installer and Python packages, use approved immutable CI images, promote image digests rather than latest tags, and isolate credential acquisition after artifact verification.

### Session and JWT signing configuration accepts static fallback secrets

- Severity: `medium`
- Confidence: `high`
- Status: `validated`
- Impact: A configuration mistake can make signing material predictable and weaken session or token integrity.
- Recommendation: Remove fallback literals, require high-entropy managed secrets at startup, fail fast when absent, and rotate any environment that used the fallback.

### Retrieved documents and conversational content are written to application logs

- Severity: `medium`
- Confidence: `high`
- Status: `validated`
- Impact: Potentially confidential corpus content, user questions, session context, and model responses can be exposed to log readers and retained beyond application data policy.
- Recommendation: Log identifiers, counts, timing, and redacted metadata instead of content; define classification-aware retention and access controls.

### Tier 3 security behaviors have no executable behavior-level test evidence

- Severity: `medium`
- Confidence: `high`
- Status: `validated`
- Impact: Security regressions in access control, corpus integrity, external token issuance, and sensitive-data handling can reach review without independent executable evidence.
- Recommendation: Add a deterministic test command and behavior-level negative, role, corpus-promotion, provider-token, logging, and regression tests with durable outcome assertions.

## Required actions

- Add application-layer authentication and operation-specific authorization before reports, document management, ingestion, generation, and administrative job actions.
- Separate RAG ingestion from reviewed activation and add provenance, integrity, and prompt-injection controls.
- Protect provider-token issuance with identity, allowlists, rate limits, and quota controls.
- Replace unpinned CI downloads and mutable image promotion with verified immutable artifacts.
- Remove fallback signing secrets and minimize content logging.
- Add executable behavior-level security tests and rerun ADDER against a Git-backed change with approved package intelligence.

## Required approvals

- Application owner
- AppSec Tier 3 reviewer
- AI or model-risk owner
- Delivery Enablement or CI/CD owner
- Data owner for corpus, conversations, and logs

## Checks not performed

- Live endpoint validation or exploit testing
- Test execution or build: no test command is defined, the discovered backend tests reference an absent import target, dependencies were not installed, and the target remained read-only
- Authoritative package existence, publisher, vulnerability, malware, maintenance, and reputation checks: no approved registry or intelligence access was supplied
- Git diff and history review: the supplied snapshot contains no .git directory
- Deployment, gateway, runtime, log-platform, cloud-IAM, and production configuration validation

## Limitations

- Static read-only review of a non-Git source snapshot; no network calls, package installation, credential validation, service startup, or production interaction occurred.
- Reachability and severity assume no equivalent upstream identity or network control; deployment evidence is required to resolve that assumption.
- The two database-string scanner candidates were environment-composed values rather than embedded credentials; raw values and secret material were not persisted in pilot artifacts.
