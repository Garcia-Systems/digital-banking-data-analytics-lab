# SQL examples

Run `python3 scripts/build_analytics_db.py`, then use `sqlite3 data/generated/harbor_analytics.sqlite < sql/01_core_metrics.sql` when the optional SQLite CLI is installed. The Python Chapter 4 lab needs no CLI. `01_core_metrics.sql` contains correct session-aware rates; `02_mistakes.sql` documents executable mistake contrasts. `03_account_opening_funnel.sql` uses readable conditional aggregation, `CASE`, and distinct application attempts. SQLite is generated, disposable, and never authoritative.

`04_navigation_search.sql` demonstrates page/search counts, event-denominated rates, selections, and transitions. `05_campaign_funnel.sql` reports tagged sessions and application-grain observed conversion. Neither implies cause or attribution.

`06_application_telemetry.sql` adds readable API volume, error, status, average/high-latency,
integration, query, and error examples. Percentiles remain in Python because SQLite lacks
a portable built-in percentile aggregate.
