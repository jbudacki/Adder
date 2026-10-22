# Pilot metric examples

The observations in this directory are synthetic examples used to test metric aggregation. They are not pilot results and must not be represented as measured ADDER performance.

Measured operational runs are stored under `runs/` and must remain separate from these synthetic examples. The current cohort contains one read-only AI/RAG application snapshot assessment; application and infrastructure slots remain open.

Create a real observation only after a human has established the seeded or validated scenarios, reviewed findings, and recorded effort. Missing denominators should remain unavailable rather than being reported as zero performance.

Run:

```bash
python3 scripts/aggregate_pilot_metrics.py \
  --input evaluations/pilot/observations.example.json \
  --output pilot-summary.json
```
