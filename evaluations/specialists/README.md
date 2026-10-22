# Embedded specialist evaluations

`cases.json` provides one routing or evidence-gate case for every Phase 3 embedded specialist. It includes positive and false-positive-sensitive scenarios. Run the structural and scanner checks with:

```bash
python3 scripts/validate_specialist_fixtures.py
python3 scripts/validate_specialist_scanners.py
python3 scripts/validate_phase3_completion.py
```

These checks validate coverage, redaction, and scanner behavior. They do not replace independent review-quality evaluation or establish production detection rates.
