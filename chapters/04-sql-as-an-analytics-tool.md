# Chapter 4 — SQL as an Analytics Tool

Application CRUD asks “what is this application's status?” Analytical SQL asks “how does completion vary by channel?” SQLite lets engineers answer the second question close to familiar application technology. This chapter practices only `SELECT`, `WHERE`, counts, distinct counts, grouping, ordering, `CASE`, aggregates, joins, and calculated rates.

Run `python3 scripts/build_analytics_db.py`, then `python3 scripts/chapter_04_sql.py`. The CSV remains authoritative; SQLite is a disposable projection. Indexes on event name and timestamp illustrate indexes aligned with frequent filters, not indiscriminate indexing. Inspect `sql/01_core_metrics.sql` and `sql/02_mistakes.sql`.

## Analytical traps
A numerator without its denominator is not a rate. Event counts are not session counts. Duplicates inflate counts; non-unique joins multiply rows. Aggregates are filtered with `HAVING`. Use `100.0` for decimal division and `NULLIF` for zero denominators. `NULL` needs `IS NULL`. A missing completion records “not observed,” not necessarily failure. Independent Python and SQL implementations agreeing is useful validation, though shared bad assumptions can still agree.

## Chapter contract

- **Read:** `sql/01_core_metrics.sql`, `sql/02_mistakes.sql`, and `src/harbor_analytics/database.py`.
- **Run:** `python3 scripts/build_analytics_db.py && python3 scripts/chapter_04_sql.py` from the repository root.
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

[← Chapter 3](03-asking-questions-data-can-answer.md) · [Contents](../CONTENTS.md) · [Chapter 5 →](05-time-based-analysis.md)
