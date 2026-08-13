# Chapter 17 — Error and Incident Analytics

An **error** is one observation; a **recurring pattern** repeats; a **degradation** is worsened service evidence; an **incident** is a bounded event requiring coordinated attention. This analytics chapter asks what records show and where to investigate—not how to run incident response.

Structured errors record component/category/severity, endpoint/provider, correlation, recoverability, and member visibility. They exclude payloads and sensitive stack values. Group over time, component, endpoint, and category; distinguish recovered from member-visible errors and compare a pattern with its historical baseline before calling it new.

The deterministic baseline/incident comparison covers completion context, API error and p95, provider timeout, database latency, and visible errors. A chronological view orders starts, latency, timeouts, retries, completion changes, and abandonment observations. **Sequence establishes order, not cause.** Run `python3 scripts/chapter_17_error_incident_analytics.py` and `python3 scripts/part_04_investigation.py`.

Evidence strengthens without a fake score: `single observation → repeated pattern → cross-segment comparison → correlated application evidence → cross-layer corroboration → controlled experiment`. Corroboration supports an engineering hypothesis; reproduction or a controlled experiment may still be needed.
