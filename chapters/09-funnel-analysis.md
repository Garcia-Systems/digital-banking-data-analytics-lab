# 9. Funnel Analysis

> A funnel measures how many eligible journeys reach successive stages of a defined process.

`build_funnel` counts distinct applications that progress through the ordered Harbor stages. Stage-to-stage conversion is `reached current / reached previous`; overall completion is `reached final / started`. Those denominator names must accompany “conversion.” Drop-off is the previous count minus the current count, and its rate uses the previous count. Zero denominators return `0.0` in this teaching API.

Run `python3 scripts/chapter_09_funnels.py` for the calculated table, drop-offs, and dependency-free bar display. Rebuild SQLite first to see the Python/SQL agreement check. `sql/03_account_opening_funnel.sql` uses readable `CASE`, conditional aggregation, and `COUNT(DISTINCT application_id)`.

## Mistakes to avoid

Do not count event rows, inflate retries, change denominators, mix periods, or compare differently defined funnels. Missing telemetry is not proven abandonment. The largest drop locates an investigation area; it does not name a root cause. A funnel is descriptive, not causal.

## Chapter contract

- **Read:** the funnel definitions, `src/harbor_analytics/journeys.py`, and `sql/03_account_opening_funnel.sql`.
- **Run:** `python3 scripts/build_analytics_db.py && python3 scripts/chapter_09_funnels.py` from the repository root.
- **Observe:** Verify the printed analytical unit, counts, window, and evidence boundary rather than reading a percentage alone.
- **Change or investigate:** Complete the exercise below on a filter or copy; committed fixtures remain deterministic.
- **Understand afterward:** Explain what this chapter's evidence establishes, what it only suggests, and which earlier definition it depends on.

## Exercise

1. **Predict:** Before running the lab, write one expected count, segment, pattern, or evidence limitation.
2. **Run:** Execute the contract command and identify the analytical unit behind each reported rate.
3. **Inspect and calculate:** Reproduce one result from its numerator and denominator (or verify one non-rate result from the underlying rows).
4. **Compare and explain:** State one evidence-bounded observation and one interpretation or hypothesis that needs more evidence.
5. **Investigate:** Change a filter, segment, window, fixture copy, or trace target; explain why the result changed.

## Navigation

[← Chapter 8](08-modeling-the-member-journey.md) · [Contents](../CONTENTS.md) · [Chapter 10 →](10-finding-abandonment-and-friction.md)
