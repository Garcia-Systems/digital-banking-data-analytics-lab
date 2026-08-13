-- Application CRUD asks for one record. Analytics summarizes a population.
SELECT COUNT(*) AS event_count, COUNT(DISTINCT session_id) AS session_count FROM events;
SELECT channel,
 COUNT(DISTINCT CASE WHEN event_name='application_started' THEN session_id END) AS starts,
 COUNT(DISTINCT CASE WHEN event_name='application_completed' THEN session_id END) AS completions,
 100.0 * COUNT(DISTINCT CASE WHEN event_name='application_completed' THEN session_id END)
 / NULLIF(COUNT(DISTINCT CASE WHEN event_name='application_started' THEN session_id END), 0) AS completion_rate
FROM events GROUP BY channel ORDER BY channel;
