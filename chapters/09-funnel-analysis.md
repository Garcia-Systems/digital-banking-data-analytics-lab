# 9. Funnel Analysis

> A funnel measures how many eligible journeys reach successive stages of a defined process.

`build_funnel` counts distinct applications that progress through the ordered Harbor stages. Stage-to-stage conversion is `reached current / reached previous`; overall completion is `reached final / started`. Those denominator names must accompany “conversion.” Drop-off is the previous count minus the current count, and its rate uses the previous count. Zero denominators return `0.0` in this teaching API.

Run `python3 scripts/chapter_09_funnels.py` for the calculated table, drop-offs, and dependency-free bar display. Rebuild SQLite first to see the Python/SQL agreement check. `sql/03_account_opening_funnel.sql` uses readable `CASE`, conditional aggregation, and `COUNT(DISTINCT application_id)`.

## Mistakes to avoid

Do not count event rows, inflate retries, change denominators, mix periods, or compare differently defined funnels. Missing telemetry is not proven abandonment. The largest drop locates an investigation area; it does not name a root cause. A funnel is descriptive, not causal.

Continue to [Chapter 10](10-finding-abandonment-and-friction.md).
