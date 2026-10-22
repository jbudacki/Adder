# Representative pilot repositories

These synthetic fixtures model the three repository types required by the ADDER pilot. They contain no credentials, network calls, deployment logic, or live integrations.

Each fixture contains:

- `baseline/` — the known-good comparison state
- `proposed/` — a deliberately risky change for assessment
- `expected.json` — expected tier, routing, and evidence requirements

The fixtures test review behavior; they are not production reference implementations.

