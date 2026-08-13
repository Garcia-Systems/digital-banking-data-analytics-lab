# Chapter 7 — Data Quality and Analytical Trust

**A precise calculation from bad data is still a bad answer.** Duplicate or missing events, malformed timestamps, missing dimensions, inconsistent categories, impossible durations, ordering violations, instrumentation changes, bot/test traffic, partial outages, and schema drift all threaten interpretation.

Run `python3 scripts/generate_dirty_fixture.py` and `python3 scripts/chapter_07_data_quality.py`. The separate deterministic dirty fixture includes a duplicate completion, removed start, `Mobile`, negative duration, completion before start, blank channel, and malformed timestamp. Checks detect rather than repair. The responsible sequence is detect → understand → decide treatment → document; silent cleaning can erase evidence or introduce undocumented choices.

## Part II investigation
Ask: “Harbor's account-opening completion rate appears to have declined. What can we responsibly say?” Use SQL → time → segmentation → quality checks → evidence-bounded conclusion. The canonical observations support a period decline concentrated in mobile phones and overlapping identity-success degradation. They do not prove vendor causation. Only use the canonical conclusion after its defined checks pass.

This Part asks what is happening and where to investigate. Measurable Outcomes asks whether a change produced an intended improvement. Machine Learning asks whether history predicts or classifies unknown cases. Journey funnels and abandonment begin in Part III, not here.
