# Chapter 5 — Time-Based Analysis

A total without time can conceal trends and spikes. Harbor timestamps are ISO-8601 UTC instants. We derive dates and hours; daily groups are demonstrated, while weekly groups, rolling windows, seasonality, and forecasting require choices about calendars and sufficient history.

Run `python3 scripts/chapter_05_time_analysis.py`. The 21-day fixture contains normal variation, rising mobile mix, and a short identity-verification degradation. A baseline and comparison are descriptive windows, not automatically an experiment. `events_between` uses a half-open interval; `group_by_day`, `daily_event_counts`, and `daily_rate` keep logic visible.

For 70% → 63%, the absolute/percentage-point difference is -7 points, while relative change is `(63-70)/70 = -10%`. “Completion was lower Tuesday” can be observed. “The identity provider caused it” requires evidence beyond temporal overlap. Forecasting is deferred.
