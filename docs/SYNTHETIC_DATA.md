# Synthetic-data generation

Everything describes fictional Harbor Federal Credit Union. Run both generators:

```bash
python3 scripts/generate_synthetic_data.py
python3 scripts/generate_engineering_telemetry.py
```

The generators use fixed rules and timestamps, no randomness or current date. The event source
and four application telemetry sources intentionally remain separate. Regeneration tests compare
bytes. Identifiers are synthetic join keys—not member facts—and telemetry contains metadata rather
than request bodies, tokens, credentials, account numbers, raw parameters, or sensitive traces.
Beacon Identity Labs and every observed incident are fictional.
