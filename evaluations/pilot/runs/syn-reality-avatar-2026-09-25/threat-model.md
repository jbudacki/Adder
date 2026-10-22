# Threat model — Syn Reality Avatar snapshot

**Assessment:** `pilot-syn-reality-avatar-20260925`  
**Method:** Split STRIDE and MAESTRO  
**Scope:** Supplied local source snapshot only  
**Environment validation:** Not performed

## System description

The snapshot contains an Express and TypeScript backend, two Next.js applications, PostgreSQL and pgvector storage, session and password-based authentication code, document ingestion, AWS storage and document extraction, embedding and chat-model calls, an external avatar-session provider, WebSocket transcription, Docker packaging, and GitLab deployment jobs.

The most important assets are user identities and sessions, conversation history, model prompts and responses, uploaded corpus documents, embeddings, provider credentials and session tokens, cloud deployment credentials, container artifacts, and operational logs.

## Trust boundaries and flows

1. Browser or API client → Next.js and Express endpoints
2. Uploaded PDF or image context → temporary storage → extraction → embedding → vector store
3. User question and chat history → rephrasing model → vector retrieval → answer model
4. Server-held provider key → external avatar provider → session token → browser
5. Application → PostgreSQL, pgvector, AWS storage, and document extraction
6. GitLab runner → external download and package sources → cloud identities and deployment targets
7. Application and model data → logs and downstream log consumers

## Worst credible scenario

If the backend is reachable without an equivalent upstream authorization control, an unauthenticated caller can upload instruction-bearing content, activate it for an avatar, and cause it to enter retrieval context. The same missing application authorization exposes document-management and reporting operations. In parallel, an unpinned deployment input could execute in a privileged CI job and alter production artifacts. Confidence is high in the source paths and medium in deployed reachability because gateway and runtime configuration were not supplied.

## STRIDE assessment

| Category | Supported threat | Current controls | Gap and treatment |
| --- | --- | --- | --- |
| Spoofing | Callers can supply user identifiers and invoke sensitive routes without a verified application identity. | Password login and session code exist. | Authentication is not enforced on mounted sensitive routes; require identity and operation-level authorization. |
| Tampering | Uploaded content and document-job state can be changed through unauthenticated handlers. | Uploaded documents default inactive. | Activation and job completion are also unauthenticated; separate ingestion, approval, and promotion. |
| Repudiation | `requestedBy` and `reviewedBy` are caller-supplied strings. | HTTP and application logging exist. | Bind audit actors to authenticated identities and make administrative audit events immutable and reviewable. |
| Information disclosure | Reports return conversation content; application logs questions, retrieved documents, sessions, and model answers. | Logger levels and session cookies provide partial structure. | Minimize returned and logged data, authorize report access, and define retention and access controls. |
| Denial of service | Public upload, embedding, model, extraction, and avatar-token paths can consume storage, compute, provider quota, and cost. | Upload size and count limits exist for some paths. | Add authentication, per-identity quotas, rate limits, timeouts, concurrency limits, and cost attribution. |
| Elevation of privilege | Unauthenticated callers can reach administrative document and job operations; deployment scripts execute in privileged jobs. | Production jobs are manual. | Enforce roles at the sink and verify immutable CI inputs and artifacts before credential use. |

## MAESTRO assessment

| Layer | Supported threat | Current controls | Gap and treatment |
| --- | --- | --- | --- |
| Foundation models | User, history, and retrieved context influence model behavior. | System and formatting prompts exist. | Prompt wording is not an isolation boundary; add adversarial evaluation and deterministic mediation. |
| Data operations | Untrusted uploads can become active retrieval records and retrieved content is logged. | Documents default inactive and retrieval filters on contentFor. | Authorize and attest ingestion and activation; sanitize metadata; monitor corpus integrity; avoid logging content. |
| Agent frameworks | No autonomous tool execution was found in the answer flow. | Model output is post-processed for speech. | Keep model output non-authoritative; validate any future tools separately. |
| Deployment infrastructure | External package, script, image, cloud, database, and provider boundaries are material. | Lockfiles include integrity values; production jobs are manual. | Verify approved registries and package intelligence; pin scripts, packages, base images, and promoted image digests. |
| Evaluation and observability | Only superficial stale backend tests were found. | Request and application logs exist. | Add behavior-level security tests and privacy-preserving telemetry; instrument pilot timing and reliability. |
| Security and compliance | Conversation, corpus, and log data may be sensitive. | Cookies are httpOnly and production cookies are marked secure for selected environment names. | Confirm data classification, retention, consent, access, deletion, and incident-response ownership. |
| Agent ecosystem | Model, embedding, avatar, AWS, database, CI, and log providers form a cascading dependency chain. | Environment variables hold service credentials. | Establish least-privilege identities, provider allowlists, failure modes, provenance, and rollback for each boundary. |

## Verification priorities

1. Confirm gateway and network controls, then perform authorized anonymous and role-based API tests.
2. Seed benign instruction-like corpus content in an isolated environment and verify promotion and model behavior controls.
3. Verify provider-token authentication, rate limits, and allowlists without consuming production quota.
4. Rebuild the pipeline with immutable inputs and prove the reviewed image digest is the deployed digest.
5. Exercise redacted logging tests and inspect downstream retention and access.

## Open questions

- Which repository revision and deployment environment does the snapshot represent?
- Are API routes protected by an identity-aware gateway or private network control?
- Who is authorized to ingest, activate, delete, and review corpus content?
- What data classifications apply to conversations, documents, embeddings, and logs?
- Which package registry, malware, vulnerability, and reputation sources are approved?
