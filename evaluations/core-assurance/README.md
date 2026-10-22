# Core assurance evaluations

`cases.json` supplies representative Phase 2 routing expectations. It covers every risk tier and every assessment outcome without requiring Phase 3 specialist skills to exist.

The cases test decision invariants rather than exact prose. Run:

```bash
python3 scripts/validate_core_fixtures.py
```

These fixtures validate the expected contract; they do not prove detection accuracy or substitute for independent behavioral evaluation of the skills.

