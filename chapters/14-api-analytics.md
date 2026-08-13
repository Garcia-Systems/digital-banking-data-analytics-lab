# Chapter 14 — API Analytics

Part III showed weaker mobile completion near identity verification. The application-layer question is: **what was Harbor's API doing during those sessions?** Harbor exposes synthetic `POST /api/applications`, `POST /api/applications/{id}/verify`, submit/status, transfer, and account endpoints; this fixture focuses on verification so its tail is visible.

Request telemetry records request, session, application, and correlation identifiers plus endpoint, method, status, outcome, channel/device, and duration—metadata needed for analysis, not bodies, tokens, names, credentials, or account numbers. Purpose-limited metadata reduces exposure while retaining joins. Real systems often have correlation gaps; absence of a match is not proof that no call happened.

Core measures are volume, success/error counts and rates, average, median, and p95 latency. `percentile` uses **nearest rank**: sort `n` values and select rank `ceil(p/100 × n)` (minimum rank one). This is deliberately visible Python, not NumPy. An average can remain modest while p95 exposes a slow minority. Segment by endpoint with `requests_by_endpoint`, `error_rate_by_endpoint`, `latency_by_endpoint`, and `status_codes_by_endpoint`. SQLite examples stay readable; Python computes p95 because portable SQLite percentile SQL is awkward.

```text
experience event → session_id/application_id → API request → correlation_id
```

Run `python3 scripts/chapter_14_api_analytics.py`. An endpoint difference supports a next investigation, not a causal verdict.

## Chapter contract

- **Read:** the request-grain definitions and `src/harbor_analytics/engineering.py`.
- **Run:** `python3 scripts/chapter_14_api_analytics.py` from the repository root.
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

[← Chapter 13](13-marketing-and-campaign-analytics.md) · [Contents](../CONTENTS.md) · [Chapter 15 →](15-vendor-and-fintech-integration-analytics.md)
