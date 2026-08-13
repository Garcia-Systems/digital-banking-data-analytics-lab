# Chapter 14 — API Analytics

Part III showed weaker mobile completion near identity verification. The application-layer question is: **what was Harbor's API doing during those sessions?** Harbor exposes synthetic `POST /api/applications`, `POST /api/applications/{id}/verify`, submit/status, transfer, and account endpoints; this fixture focuses on verification so its tail is visible.

Request telemetry records request, session, application, and correlation identifiers plus endpoint, method, status, outcome, channel/device, and duration—metadata needed for analysis, not bodies, tokens, names, credentials, or account numbers. Purpose-limited metadata reduces exposure while retaining joins. Real systems often have correlation gaps; absence of a match is not proof that no call happened.

Core measures are volume, success/error counts and rates, average, median, and p95 latency. `percentile` uses **nearest rank**: sort `n` values and select rank `ceil(p/100 × n)` (minimum rank one). This is deliberately visible Python, not NumPy. An average can remain modest while p95 exposes a slow minority. Segment by endpoint with `requests_by_endpoint`, `error_rate_by_endpoint`, `latency_by_endpoint`, and `status_codes_by_endpoint`. SQLite examples stay readable; Python computes p95 because portable SQLite percentile SQL is awkward.

```text
experience event → session_id/application_id → API request → correlation_id
```

Run `python3 scripts/chapter_14_api_analytics.py`. An endpoint difference supports a next investigation, not a causal verdict.
