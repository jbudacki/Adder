# Operational ownership

No operational owner has been formally assigned. The roles below define the minimum ownership model required before ADDER advances beyond pilot-only use.

| Role | Accountability | Current owner |
|---|---|---|
| AppSec control owner | Approves assurance controls, severity policy, tuning, and control retirement | Unassigned |
| Delivery Enablement / DevOps owner | Owns CI integration, runner reliability, latency budgets, and fail-open/fail-closed behavior | Unassigned |
| Repository owner | Accepts pilot scope, validates findings, implements remediation, and requests exceptions | Assigned per pilot; no portfolio owner |
| AI / model risk owner | Reviews AI-specific boundaries, prompt-injection risk, provenance claims, and model changes | Unassigned |
| Data owner | Approves repository data handling, retention, and external-provider use | Unassigned |
| Exception authority | Approves time-bounded risk exceptions and compensating controls | Unassigned |
| Release owner | Versions, signs, publishes, and rolls back ADDER releases | Unassigned |
| Support and incident owner | Handles service degradation, incorrect blocking, sensitive-output events, and recovery | Unassigned |
| Legal / licensing owner | Approves bundled skill licenses, branding, notices, and redistribution | Unassigned |

## Required operating records

Before advisory release, owners must approve and maintain:

- Supported repository populations and exclusions.
- Data handling, retention, and log-redaction rules.
- Control thresholds and severity mappings.
- Exception request, approval, expiry, and review procedures.
- Support hours, escalation routes, and incident classification.
- Release, rollback, and compatibility procedures.
- A recurring control-quality review using human-validated evidence.

Unassigned ownership is an explicit release blocker, not a documentation placeholder that can be treated as approval.
