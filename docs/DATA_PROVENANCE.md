# Synthetic Data Provenance

Every dataset in this repository is fictional, synthetic, deterministic, and created solely for instruction. No row describes a real member, institution, account, vendor, campaign, application, or incident. Generators write stable identifiers and purpose-limited metadata; they exclude names, email addresses, account numbers, SSNs, passwords, tokens, request bodies, and raw search text.

## Dataset inventory

| Dataset | Generator | Determinism | Grain and schema summary | Purpose / condition | Chapters |
| --- | --- | --- | --- | --- | --- |
| `digital_events.csv` | `scripts/generate_synthetic_data.py` → `dataset.generate_events` | Fixed construction; no random seed | One event: IDs, UTC timestamp, channel/device, event/outcome/duration, source, application, normalized campaign/navigation/search metadata | Clean core experience fixture | 0–13 |
| `digital_events_dirty.csv` | `scripts/generate_dirty_fixture.py` → `dirty.generate_dirty_events` | Fixed mutations of the core fixture | Same event schema | Intentionally dirty: duplicate, missing start, category drift, blank value, negative duration, ordering and timestamp defects | 7 |
| `api_requests.csv` | `scripts/generate_engineering_telemetry.py` → `engineering.write_fixtures` | Fixed construction; no random seed | One API request: request/correlation/session/application IDs, endpoint, status, duration, outcome, segment, period | Clean teaching telemetry with designed degradation examples | 14, 17 |
| `integration_calls.csv` | Same engineering generator | Fixed construction | One provider call: logical integration ID, correlation ID, provider/operation, attempt, outcome, duration, retryability, period | Retry/recovery and call-vs-operation grain | 15, 17 |
| `database_queries.csv` | Same engineering generator | Fixed construction | One query observation: correlation ID, stable query/category, duration, row counts, outcome, period | Database latency, scans, repetition, N+1 | 16–17 |
| `error_events.csv` | Same engineering generator | Fixed construction | One structured error: correlation, component/category/severity, endpoint/provider, recoverability, visibility, period | Error-pattern and incident comparison | 17 |
| `verification_guidance_experiment.csv` | `scripts/generate_decision_data.py` → `decisions.generate_experiment` | Python PRNG seed `20250320`; 400 assignments | One assigned application: variant, segment, completion, verification, duration, API/retry/support guardrails | Controlled synthetic experiment | 20–22 |
| `capstone_journey_events.csv` | `scripts/generate_capstone_data.py` → `capstone.write_capstone` | Fixed construction; no random seed | One journey event with session/application/request/correlation/version context | Capstone cross-layer evidence | 23 |
| `capstone_api_requests.csv` | Same capstone generator | Fixed construction | One API request | Capstone baseline/comparison API evidence | 23 |
| `capstone_vendor_calls.csv` | Same capstone generator | Fixed construction | One provider call and attempt | Capstone retry and recovery evidence | 23 |
| `capstone_database_observations.csv` | Same capstone generator | Fixed construction | One categorized query observation | Capstone alternative-explanation check | 23 |
| `capstone_errors.csv` | Same capstone generator | Fixed construction | One structured cross-layer error | Capstone friction/timeline evidence | 23 |
| `capstone_navigation.csv` | Same capstone generator | Fixed construction | One application/session navigation summary | Capstone campaign and search alternative checks | 23 |
| `capstone_releases.csv` | Same capstone generator | Fixed construction | One fictional release record | Capstone timeline and alternative hypothesis | 23 |

`data/generated/harbor_analytics.sqlite` is not an independent source. `scripts/build_analytics_db.py` rebuilds this disposable SQLite projection from the committed CSV fixtures. `dist/dashboard.html` is generated presentation output, not a dataset.

## Reproducibility and safe use

Regenerate core, dirty, engineering, decision, and capstone fixtures before analysis. Tests compare deterministic outputs and important invariants. The synthetic scenario intentionally contains clean, dirty, degraded, experimental, and capstone evidence; those labels describe teaching design, not real operational quality.
