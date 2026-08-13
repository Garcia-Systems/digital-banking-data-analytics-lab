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

The lab reports application, mobile, and verification completion plus API errors, p95 latency, and vendor timeouts. Each row names its 200-observation denominator unit; latency is calculated across the named requests or calls and expressed in milliseconds. The declared target precedes status evaluation. This chapter teaches analysis for a decision; a separate measurable-outcomes discipline asks how far the observation supports technical, member, or business impact claims.

## Chapter contract

- **Read:** the declared windows and `src/harbor_analytics/decisions.py`.
- **Run:** `python3 scripts/chapter_18_before_after.py` from the repository root.
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

[← Chapter 17](17-error-and-incident-analytics.md) · [Contents](../CONTENTS.md) · [Chapter 19 →](19-cohort-analysis.md)
