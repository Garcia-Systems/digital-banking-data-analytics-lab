# Chapter 23 — The Harbor Federal Digital Experience Investigation

[← Chapter 22](22-communicating-findings-without-overclaiming.md) · [Contents](../CONTENTS.md) · [Review only after investigating](../docs/CAPSTONE_REVIEW.md)

> **Harbor Digital Banking request:** “We've noticed that fewer digital account-opening applications seem to be reaching completion. Please investigate whether completion actually declined, where the change is concentrated, what technical evidence may explain it, what engineering should investigate or change, and how we would verify improvement.”

That is all the diagnosis you receive. Harbor Federal Credit Union, Northstar Identity, every identifier, and every observation in this lab are fictional and synthetic.

## Start the investigation

```bash
python3 scripts/generate_capstone_data.py
python3 scripts/run_capstone.py
python3 scripts/run_capstone.py --analysis overview
```

The seven deliberately separate sources are journey events, API requests, vendor attempts, database observations, structured errors, navigation/campaign observations, and releases. Their grains differ. Join only on synthetic `application_id`, `request_id`, or `correlation_id`; never multiply application counts by blindly joining one-to-many tables. The generated CSVs are inspectable in `data/synthetic/`, the reusable calculations are in `src/harbor_analytics/capstone.py`, and SQL starters are in `sql/07_capstone_investigation.sql`.

Record decisions and queries as you go. **Do not read the review yet.**

## Phase 1 — Establish the problem

**Question:** Did completion actually decline?

Use an application—not an event, session, API request, or provider attempt—as the analytical unit. Declare May 1–14 as baseline and May 15–28 as comparison only after confirming the fixture coverage. Report starts, completions, rates, and the comparison-minus-baseline percentage-point difference. Explain why a percentage-point difference is not a relative-percent difference.

## Phase 2 — Find when it changed

```bash
python3 scripts/run_capstone.py --analysis time
```

Plot or inspect daily starts, completions, and rates. When does a sustained pattern begin? Preserve counts: twenty starts and fourteen completions conveys more than “70%.” A daily wobble is not automatically an incident.

## Phase 3 — Segment before explaining

```bash
python3 scripts/run_capstone.py --analysis segment
```

Compare `channel`, `device_type`, and `campaign_source`, always with denominators. Is the decline broad or concentrated? Did traffic mix change? Separate a within-segment rate change from the aggregate effect of a larger segment. Campaign mix can be explanatory without explaining all of the difference.

## Phase 4 — Reconstruct the journey

```bash
python3 scripts/run_capstone.py --analysis funnel
```

Calculate counts, stage-to-stage conversion, overall conversion, and drop-off for:

```text
Application Started → Identity Verification Started → Identity Verification Completed
→ Application Submitted → Application Completed
```

Which transition changes most? Do not label a missing later event a vendor failure until dependency evidence supports that interpretation.

## Phase 5 — Investigate friction

```bash
python3 scripts/run_capstone.py --analysis abandonment
```

For affected journeys, compare last observed stage, start-to-last-stage duration, retry counts, structured errors, and verification outcomes. Write two separate sentences: one describing **observed friction**, and one describing the causal claim the data **cannot prove**.

## Move through the stack

Run each investigation without assuming every anomaly is relevant:

```bash
python3 scripts/run_capstone.py --analysis api
python3 scripts/run_capstone.py --analysis vendor
python3 scripts/run_capstone.py --analysis database
python3 scripts/run_capstone.py --analysis timeline
```

For APIs, compare volume, status/error rate, average, median, and p95 by endpoint and period. Which endpoint aligns with the journey stage? Why can a stable median coexist with a materially worse tail?

For Northstar Identity (a fictional provider), distinguish calls from logical operations. Calculate timeouts, retries, recovered retries, and operations whose final attempt is unsuccessful. A failed attempt is not necessarily member-visible failure.

For the database, compare volume, average/p95 duration, slow counts, and rows examined by query category. One query category may be interesting. Is it relevant to identity verification, and does the relevant `application_state` path degrade?

Build a chronological table with time, experience, API, vendor, database, and error observations. Ask what appeared first and what followed. **Temporal order strengthens reasoning; it does not establish causation.**

## Trace real fixture records

These examples are selected only by trace shape; their output is reconstructed from CSVs:

```bash
python3 scripts/capstone_trace.py cap-app-0001   # baseline completed
python3 scripts/capstone_trace.py cap-app-0284   # comparison retry and recovery
python3 scripts/capstone_trace.py cap-app-0283   # comparison unrecovered
```

Confirm journey → API → provider attempt(s) → database → later event (or its absence). Find two more examples yourself. Correlation increases consistency across layers but missing telemetry and shared timing remain limitations.

## Compare hypotheses

```bash
python3 scripts/run_capstone.py --analysis hypothesis
```

| Hypothesis | Supporting evidence | Contradicting evidence | Status |
| --- | --- | --- | --- |
| Mobile UI issue | | | |
| Campaign traffic mix | | | |
| Harbor API regression | | | |
| Identity integration degradation | | | |
| Database slowdown | | | |

Use `SUPPORTED LEAD`, `POSSIBLE`, `WEAKLY SUPPORTED`, `NOT SUPPORTED BY CURRENT EVIDENCE`, or `NOT TESTED`. Do not invent a confidence score.

## Report and act

```bash
python3 scripts/run_capstone.py --analysis report
```

Complete **OBSERVATION, CROSS-LAYER EVIDENCE, LEADING HYPOTHESIS, ALTERNATIVES, LIMITATION, NEXT ACTION**. Recommend a bounded action: reproduce relevant behavior, inspect timeouts/retries and provider responses, improve instrumentation, or run a controlled change—not “replace the vendor.”

Define a primary journey metric, member outcome, technical metrics, guardrails, and comparison method. Explain why a randomized controlled rollout, when safe and feasible, supports a stronger attribution than an uncontrolled before/after comparison.

Communicate the same numerical facts three ways: (1) detailed Engineering evidence, (2) member-journey and operational implications for Digital Product/Operations, and (3) a short Executive scope, issue, leading explanation, limitation, and action. Numbers may not drift between versions.

## Final synthesis

```text
QUESTION → INSTRUMENT → COLLECT → VALIDATE → QUERY → SEGMENT → TRACE → ANALYZE
→ HYPOTHESIZE → INVESTIGATE → DECIDE → CHANGE → MEASURE → COMMUNICATE
```

> Data analytics is not separate from software engineering when the engineer is responsible for understanding how a digital system behaves in the real world.

Analytics does not replace debugging, application/API/database knowledge, testing, product judgment, or communication. It makes each activity more evidence-driven.

[Review the investigation →](../docs/CAPSTONE_REVIEW.md)

## Chapter contract

- **Read:** the investigation phases and `src/harbor_analytics/capstone.py`; keep `docs/CAPSTONE_REVIEW.md` closed until finished.
- **Run:** `python3 scripts/generate_capstone_data.py && python3 scripts/run_capstone.py` from the repository root.
- **Observe:** Verify the printed analytical unit, counts, window, and evidence boundary rather than reading a percentage alone.
- **Change or investigate:** Complete the exercise below on a filter or copy; committed fixtures remain deterministic.
- **Understand afterward:** Explain what this chapter's evidence establishes, what it only suggests, and which earlier definition it depends on.

## Exercise

Complete Phases 1–9 in order without opening the review. For every rate, record numerator, denominator, unit, and window. Maintain a hypothesis table with supporting, contradicting, and missing evidence. Trace at least one recovered and one unrecovered operation, then write a report that labels observations, calculations, associations, the leading hypothesis, alternatives, and what is not established. Only then compare with `docs/CAPSTONE_REVIEW.md`; reasonable evidence-bounded interpretations need not match its wording.

## Navigation

[← Chapter 22](22-communicating-findings-without-overclaiming.md) · [Contents](../CONTENTS.md)
