# Pilot evidence summary

## Evidence completed

- Deterministic synthetic evaluation cases exercise foundation contracts, core assurance routing, specialist capability packaging, agent boundaries, recovery behavior, and GitLab advisory output.
- One operational read-only pilot assessed an AI/RAG JavaScript and TypeScript repository snapshot.
- The operational pilot produced seven advisory findings: four high and three medium severity.
- The pilot recommendation was `block_recommended`; this is advisory evidence, not an enforced gate.
- Source repositories were not changed by the pilot.

## Evidence still required

- Two additional operational repositories to complete the planned three-repository cohort.
- Human adjudication of every operational finding.
- Precision, material-miss, severity-agreement, remediation acceptance, latency, and operator-effort measurements.
- A real remediation and recovery exercise.
- Provenance and package-trust checks against approved authoritative sources.
- A live GitLab pipeline execution in the target runner environment.

## Interpretation limit

One operational repository is enough to reveal useful control candidates and workflow gaps. It is not enough to estimate portfolio-wide accuracy, compare vendors, approve blocking thresholds, or claim broad technology compatibility.

Detailed operational evidence is under `evaluations/pilot/runs/syn-reality-avatar-2026-09-25/`. The current release decision intentionally treats absent human metrics as unknown rather than zero.
