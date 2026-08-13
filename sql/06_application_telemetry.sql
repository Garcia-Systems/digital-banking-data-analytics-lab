-- SQLite has no portable percentile aggregate; Chapter 14 uses transparent Python nearest-rank p95.
SELECT endpoint, COUNT(*) AS requests FROM api_requests GROUP BY endpoint;
SELECT endpoint, ROUND(100.0 * SUM(outcome <> 'success') / COUNT(*), 1) AS error_pct FROM api_requests GROUP BY endpoint;
SELECT endpoint, status_code, COUNT(*) FROM api_requests GROUP BY endpoint, status_code;
SELECT endpoint, AVG(CAST(duration_ms AS INTEGER)) AS average_ms FROM api_requests GROUP BY endpoint;
SELECT request_id, correlation_id, duration_ms FROM api_requests WHERE CAST(duration_ms AS INTEGER) >= 1000 ORDER BY CAST(duration_ms AS INTEGER) DESC;
SELECT provider, outcome, COUNT(*) FROM integration_calls GROUP BY provider, outcome;
SELECT query_name, COUNT(*), AVG(CAST(duration_ms AS INTEGER)) FROM database_queries GROUP BY query_name;
SELECT component, error_category, COUNT(*) FROM error_events GROUP BY component, error_category;
