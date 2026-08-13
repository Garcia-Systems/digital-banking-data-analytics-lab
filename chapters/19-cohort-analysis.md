# Chapter 19 — Cohort Analysis

A **cohort** follows or compares groups sharing a defined starting characteristic. Segmentation compares mobile with desktop; cohort analysis compares applications started in Week 1 with those started in Week 2. Other useful software cohorts include first digital-use month, experience version, and campaign-entry period.

The analytical unit here is one application. `assign_start_cohort` assigns its UTC start to a Monday week, while `cohort_counts`, `cohort_completion`, and `cohort_stage_conversion` keep readable arithmetic. These are focused helpers, not an OLAP system.

## Time changes the denominator
An overall rate can rise because older applications finish later, even while the newest start cohort performs worse. Every comparison therefore needs both a start definition and an observation horizon. **Right censoring** means a recent application has not yet had the full chance to produce an outcome. “Not completed yet” is not automatically “abandoned.” Harbor's lab declares seven days of maturity and marks a cohort safe only when every application has received that window.

```bash
python3 scripts/chapter_19_cohorts.py
```

Read size, completion count and rate, verification rate, and maturity together. Compare mature cohorts with equivalent windows; describe an immature cohort rather than ranking it against mature cohorts. This refines Chapter 10's fixed-window abandonment rule rather than replacing it.
