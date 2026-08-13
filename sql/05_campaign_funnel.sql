-- Chapter 13: observed applications after a tagged arrival, not causal attribution.
SELECT campaign_id,
 COUNT(DISTINCT session_id) AS sessions,
 COUNT(DISTINCT CASE WHEN event_name='application_started' THEN application_id END) AS starts,
 COUNT(DISTINCT CASE WHEN event_name='identity_verification_completed' THEN application_id END) AS verified,
 COUNT(DISTINCT CASE WHEN event_name='application_submitted' THEN application_id END) AS submitted,
 COUNT(DISTINCT CASE WHEN event_name='application_completed' THEN application_id END) AS completed,
 100.0 * COUNT(DISTINCT CASE WHEN event_name='application_completed' THEN application_id END) /
 NULLIF(COUNT(DISTINCT CASE WHEN event_name='application_started' THEN application_id END),0) AS observed_completion_rate
FROM events WHERE campaign_id <> '' GROUP BY campaign_id ORDER BY campaign_id;
