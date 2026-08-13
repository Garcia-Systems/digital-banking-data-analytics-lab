# Chapter 15 — Vendor and Fintech Integration Analytics

A Harbor API result can depend on another system: **Harbor API failure does not necessarily mean Harbor application failure, and a provider call failure does not necessarily mean the member journey failed.**

```text
Member → Mobile/Web → Harbor API → integration adapter → Beacon Identity Labs
```

Beacon Identity Labs is entirely fictional. Its separate fixture records provider, operation, status, duration, attempt, retryability, outcome, and correlation ID. Analyze call volume, success/timeout rates, categories, average/p95, retry rate, recovery, and unrecovered operations. A `timeout → success` retry lowers call-level reliability but preserves operation-level reliability and potentially completion. Therefore raw failures can exaggerate member-visible impact.

Run `python3 scripts/chapter_15_vendor_analytics.py` and `python3 scripts/trace_application.py app-0111`. The latter traverses actual fixture rows: `application_id → API → correlation_id → integration attempts`. Evidence justifies investigating the provider; it cannot establish that the provider caused an entire conversion change.

## Chapter contract

- **Read:** the operation/call distinction and `src/harbor_analytics/engineering.py`.
- **Run:** `python3 scripts/chapter_15_vendor_analytics.py && python3 scripts/trace_application.py app-0111` from the repository root.
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

[← Chapter 14](14-api-analytics.md) · [Contents](../CONTENTS.md) · [Chapter 16 →](16-database-analytics.md)
