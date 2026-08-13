# 8. Modeling the Member Journey

An event is one observation; a journey is an ordered interpretation of several observations. Harbor's deliberately simple account-opening model is `application_started` → `identity_verification_started` → `identity_verification_completed` → `application_submitted` → `application_completed`. A landing page supplies entry context but is not an eligible funnel stage.

## Choose the grain

A synthetic member, browser/app session, and application attempt are different units. “What percentage of attempts completed?” uses distinct `application_id` values—not members, sessions, or event rows—as its denominator. One member could try twice; one application could cross sessions. In this fixture, `application_id` is a non-identifying synthetic attempt key and happens to stay within one session.

`journeys.py` groups, orders, collapses repeated stages, and requires forward progress. It does not invent a skipped stage. A completion timestamped before a start is probably telemetry/data-quality trouble, not an exotic experience.

Real experiences can pause, return, repeat, legitimately skip steps, cross tabs/devices, or wait for asynchronous work. Instrumentation can be incomplete. This lab intentionally does not solve those cases or build a workflow engine.

## Lab

Run `python3 scripts/chapter_08_journeys.py`. Select several applications; reconstruct sequences; record last stage and complete/incomplete classification; compare web/mobile. Separate **observation** (“no later expected stage was recorded”) from **hypothesis** (“verification may have impeded progress”). The latter needs additional evidence.

## Chapter contract

- **Read:** the journey stages and `src/harbor_analytics/journeys.py`.
- **Run:** `python3 scripts/chapter_08_journeys.py` from the repository root.
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

[← Chapter 7](07-data-quality-and-analytical-trust.md) · [Contents](../CONTENTS.md) · [Chapter 9 →](09-funnel-analysis.md)
