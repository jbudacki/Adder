# Phase 3 completion evaluations

`cases.json` contains positive, blocking, and ambiguous package-trust scenarios plus sufficient, insufficient, and unavailable security-test scenarios. The cases use synthetic metadata and do not contact registries, execute packages, or run repository tests.

Run:

```bash
python3 scripts/validate_phase3_completion.py
```

The validator checks decision invariants and routing coverage. It does not establish package safety, vulnerability status, malware status, or real-world test effectiveness.
