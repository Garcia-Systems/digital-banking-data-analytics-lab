# Chapter 7 — Data Quality and Analytical Trust

**A precise calculation from bad data is still a bad answer.** Duplicate or missing events, malformed timestamps, missing dimensions, inconsistent categories, impossible durations, ordering violations, instrumentation changes, bot/test traffic, partial outages, and schema drift all threaten interpretation.

Run `python3 scripts/generate_dirty_fixture.py` and `python3 scripts/chapter_07_data_quality.py`. The separate deterministic dirty fixture includes a duplicate completion, removed start, `Mobile`, negative duration, completion before start, blank channel, and malformed timestamp. Checks detect rather than repair. The responsible sequence is detect → understand → decide treatment → document; silent cleaning can erase evidence or introduce undocumented choices.

## Part II investigation
Ask: “Harbor's account-opening completion rate appears to have declined. What can we responsibly say?” Use SQL → time → segmentation → quality checks → evidence-bounded conclusion. The canonical observations support a period decline concentrated in mobile phones and overlapping identity-success degradation. They do not prove vendor causation. Only use the canonical conclusion after its defined checks pass.

This Part asks what is happening and where to investigate. Measurable Outcomes asks whether a change produced an intended improvement. Machine Learning asks whether history predicts or classifies unknown cases. Journey funnels and abandonment begin in Part III, not here.

## Chapter contract

- **Read:** the quality rules and `src/harbor_analytics/quality.py`.
- **Run:** `python3 scripts/generate_dirty_fixture.py && python3 scripts/chapter_07_data_quality.py` from the repository root.
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

[← Chapter 6](06-segmentation.md) · [Contents](../CONTENTS.md) · [Chapter 8 →](08-modeling-the-member-journey.md)
