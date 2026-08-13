# Chapter 18 — Baselines, Targets, and Before/After Analysis

Part IV made Harbor's fictional identity-verification integration a leading hypothesis. Engineers now deploy the synthetic `harbor-experience-next` change and ask: **Did observed behavior improve after the change?**

## Three different ideas
A **baseline** is what was observed before a change: mobile verification completion was 74% in the declared baseline window. A **target** is a declared objective—not an observation: Harbor would consider at least 80% desirable. A **comparison** is what was observed in the later, declared window: 81%. The absolute difference is `comparison - baseline`; for rates that is also 7 **percentage points**. Relative change divides that difference by 74%, about 9.5%. State which one you mean.

Declare the analysis before inspecting results:

```text
Question → Metric → Population → Baseline window → Comparison window → Target / decision rule → THEN examine result
```

Moving a target after seeing results rewards motivated reasoning. A target being met does not identify why.

## Comparable windows and bounded claims
Traffic volume, channel and campaign mix, weekdays, instrumentation, experience versions, and fictional vendor behavior can differ. Compare like with like and disclose remaining differences. A release boundary provides ordering, not causation: another concurrent change may explain the pattern. `release_version` is useful as a dimension, but version membership is not random assignment.

Run:

```bash
python3 scripts/chapter_18_before_after.py
```

The lab reports application, mobile, and verification completion plus API errors, p95 latency, and vendor timeouts. Rates include denominators conceptually; latency is milliseconds. The declared target precedes status evaluation. This chapter teaches analysis for a decision; a separate measurable-outcomes discipline asks how far the observation supports technical, member, or business impact claims.
