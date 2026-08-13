# SQL examples

Run `python3 scripts/build_analytics_db.py`, then use `sqlite3 data/generated/harbor_analytics.sqlite < sql/01_core_metrics.sql` when the optional SQLite CLI is installed. The Python Chapter 4 lab needs no CLI. `01_core_metrics.sql` contains correct session-aware rates; `02_mistakes.sql` documents executable mistake contrasts. `03_account_opening_funnel.sql` uses readable conditional aggregation, `CASE`, and distinct application attempts. SQLite is generated, disposable, and never authoritative.
