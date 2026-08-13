# Chapter 2 — Metrics, Dimensions, Events, and KPIs

## Why this matters
Precise vocabulary prevents a field, count, and organizational objective from being presented as if they were the same thing.

## Learning objectives
Distinguish events, properties, dimensions, metrics, and KPIs; calculate explicit rates and averages; segment carefully; and handle empty denominators.

## Harbor Federal scenario
Harbor's product team wants to discuss account-opening and identity-verification performance. Engineers first define what was recorded and how each number is calculated before deciding whether a metric belongs on an objective scorecard.

## Conceptual explanation
An **event** is a recorded occurrence, such as `application_started`. A **property** or attribute is attached information, such as `device_type = phone`. A **dimension** is a field used to group or compare observations: channel, device type, source system, page/feature, or outcome. A **metric** is a numeric measurement derived from data: starts, completion rate, mean duration, or error count. A **KPI** is a metric deliberately selected to represent progress toward an important member, product, operational, or business objective.

> Every KPI is a metric, but not every metric is a KPI.

Digital application completion rate, transfer completion rate, and identity-verification success rate may be KPI candidates when owners define objectives, scope, grain, and review cadence. A debug-event count or single handler duration is useful technical evidence but not automatically a KPI.

The reusable functions intentionally remain small: `filter_events`, `count_events`, `group_count`, `rate`, `average`, `average_duration`, and `unique_sessions`. `rate` returns `0.0` for a zero denominator. That makes scripts safe, but reporting should disclose “no eligible observations” rather than imply measured zero performance.

## Data used
Starts and completions are separate lifecycle events. `channel` and `source_system` are dimensions. `duration_ms` is recorded processing duration for an individual event, not end-to-end journey duration.

## Executable walkthrough
Run `python3 scripts/chapter_02_metrics.py`. Outputs explicitly label event counts, dimension breakdowns, metrics, and KPI candidates. Inspect `src/harbor_analytics/analysis.py` to see each calculation.

## Interpretation
The fixture's calculated completion percentages compare observed web and mobile sessions. The association can motivate a hypothesis about friction; it does not establish device, channel, or provider as a cause. The average shown is for recorded completion events and must not be renamed “average journey time.”

```text
DATA → OBSERVATION → INTERPRETATION → HYPOTHESIS → DECISION
```

## Common mistakes
Calling every number a KPI; reversing numerator and denominator; hiding zero denominators; mixing event and session grain; averaging the wrong duration; and interpreting a dimension difference causally.

## Hands-on lab
Calculate transfer starts and completions, group application starts by device, and calculate a rate. Write its numerator, denominator, unit, population, and whether it is merely a metric or a justified KPI candidate.

## Expected observations
There are ten starts and seven completions; web and mobile calculated rates differ; eight of ten verification starts have recorded completions. These are deterministic observations, not general Harbor performance.

## Key takeaways
Define grain and formula; dimensions group; metrics measure; KPI status comes from objectives and governance; empty data needs explicit interpretation.

## Glossary
**Event:** recorded occurrence. **Property:** attached value. **Dimension:** grouping/comparison field. **Metric:** numeric calculation. **KPI:** objective-linked metric. **Grain:** what one row represents.

## Review questions
1. Is `channel` an event or dimension?
2. Why is an error count not automatically a KPI?
3. What does `rate` return for denominator zero?
4. Why can event duration differ from journey duration?
5. What language avoids a causal overclaim after grouping?

## Next chapter
Chapter 3 asks whether these fields and calculations can support the conclusion a question requests.
