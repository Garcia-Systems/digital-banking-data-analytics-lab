# Chapter 16 — Database Analytics

The application developer asks: **could database behavior explain the symptom?** Query observations use stable labels—not raw SQL parameters—and include correlation ID, operation/table category, duration, rows examined/returned, and outcome. Analyze volume, average/p95, slow counts, errors, scan size, and repetition.

N+1 is visible analytically when one request triggers a parent query and many repeated child queries. Each child can look moderate while their combined request cost is material. `repeated_queries` groups `(correlation_id, query_name)` to expose that pattern. The fixture also deliberately includes both a slow API request with a slow correlated lookup and slow requests whose database work is fast. SQL should not become the default explanation.

For an index lesson, use SQLite `EXPLAIN QUERY PLAN` on a teaching table before and after `CREATE INDEX`: expect a scan to become an indexed search (wording can vary by SQLite version). This teaches plan observation only; SQLite on a laptop is not equivalent to Harbor's fictional production banking infrastructure or production MySQL. Run `python3 scripts/chapter_16_database_analytics.py`.
