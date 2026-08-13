# Chapter 15 — Vendor and Fintech Integration Analytics

A Harbor API result can depend on another system: **Harbor API failure does not necessarily mean Harbor application failure, and a provider call failure does not necessarily mean the member journey failed.**

```text
Member → Mobile/Web → Harbor API → integration adapter → Beacon Identity Labs
```

Beacon Identity Labs is entirely fictional. Its separate fixture records provider, operation, status, duration, attempt, retryability, outcome, and correlation ID. Analyze call volume, success/timeout rates, categories, average/p95, retry rate, recovery, and unrecovered operations. A `timeout → success` retry lowers call-level reliability but preserves operation-level reliability and potentially completion. Therefore raw failures can exaggerate member-visible impact.

Run `python3 scripts/chapter_15_vendor_analytics.py` and `python3 scripts/trace_application.py app-0111`. The latter traverses actual fixture rows: `application_id → API → correlation_id → integration attempts`. Evidence justifies investigating the provider; it cannot establish that the provider caused an entire conversion change.
