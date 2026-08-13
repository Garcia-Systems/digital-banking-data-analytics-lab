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

## Part V generation

`python3 scripts/generate_decision_data.py` writes `verification_guidance_experiment.csv` with seed `20250320`. Assignment draws occur before outcome draws; only the documented fictional B probabilities encode a synthetic treatment effect. Running twice is byte-identical. Every entity and observation is invented, contains no banking facts or direct identifiers, and is suitable only for education.
