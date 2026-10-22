# Agent-boundary and recovery evaluations

`cases.json` covers all four boundary statuses and recovery states where evidence or approval is incomplete, complete, or failed.

Run:

```bash
python3 scripts/validate_agent_recovery_fixtures.py
```

The validator checks decision invariants, including that a boundary violation produces a block signal and that recovery cannot be `verified` without passed required checks, verification evidence, and approval evidence.

