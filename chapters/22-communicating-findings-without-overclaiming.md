# Chapter 22 — Communicating Findings Without Overclaiming

**Say exactly what the evidence supports—and no more.** Use six parts: (1) question, (2) data and window, (3) calculated finding, (4) bounded interpretation, (5) limitation, and (6) next action.

Poor: “The identity vendor caused members to abandon applications.” Better: “During the observed degradation period, mobile completion declined while verification timeouts and latency increased. Timing and correlated request evidence make the integration a leading engineering hypothesis, but this observational analysis does not establish that the vendor caused every incomplete application.”

Use evidence labels consistently: **OBSERVED** for a recorded value; **CALCULATED** for derived arithmetic; **COMPARISON** for a difference; **ASSOCIATION** for co-occurrence; **HYPOTHESIS** for a candidate explanation; **EXPERIMENTAL EVIDENCE** for assigned comparison; and **NOT ESTABLISHED** for a boundary.

An engineer needs endpoint, latency/errors, and correlation evidence. A product manager needs funnel stage, segment, completion difference, and experience implication. An executive needs scope, measured difference, limitations, and next action. Change emphasis, never the facts or certainty.

```bash
python3 scripts/chapter_22_communication.py
python3 scripts/part_05_decision_review.py
```

All three generated reports share one numeric fact object. The integrated review combines baseline, cohort validity, experiment evidence, guardrails, decision options, and a learner-authored recommendation.

## Preparing, not solving, the capstone
The original question returns: **Digital account-opening completion has declined. Find out why.** You now have question framing → SQL → time → segmentation → data quality → journeys → funnels → abandonment → mobile/desktop → navigation/search → campaigns → API → vendor → database → errors/incidents → baselines → cohorts → experiments → dashboards → communication. Chapter 23 will supply evidence and require the learner to investigate; this chapter does not reveal its answer.

## Chapter contract

- **Read:** the evidence labels and `src/harbor_analytics/decisions.py`.
- **Run:** `python3 scripts/chapter_22_communication.py && python3 scripts/part_05_decision_review.py` from the repository root.
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

[← Chapter 21](21-dashboards-for-engineers-product-and-operations.md) · [Contents](../CONTENTS.md) · [Chapter 23 →](23-the-harbor-federal-digital-experience-investigation.md)
