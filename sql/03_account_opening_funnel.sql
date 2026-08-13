-- One row per defined stage. Distinct application_id prevents retry/event inflation.
WITH application_stages AS (
  SELECT application_id,
    MAX(CASE WHEN event_name = 'application_started' THEN 1 ELSE 0 END) AS started,
    MAX(CASE WHEN event_name = 'identity_verification_started' THEN 1 ELSE 0 END) AS verify_started,
    MAX(CASE WHEN event_name = 'identity_verification_completed' THEN 1 ELSE 0 END) AS verify_completed,
    MAX(CASE WHEN event_name = 'application_submitted' THEN 1 ELSE 0 END) AS submitted,
    MAX(CASE WHEN event_name = 'application_completed' THEN 1 ELSE 0 END) AS completed
  FROM events WHERE application_id <> '' GROUP BY application_id
)
SELECT 'application_started', COUNT(DISTINCT CASE WHEN started=1 THEN application_id END) FROM application_stages
UNION ALL SELECT 'identity_verification_started', COUNT(DISTINCT CASE WHEN started=1 AND verify_started=1 THEN application_id END) FROM application_stages
UNION ALL SELECT 'identity_verification_completed', COUNT(DISTINCT CASE WHEN started=1 AND verify_started=1 AND verify_completed=1 THEN application_id END) FROM application_stages
UNION ALL SELECT 'application_submitted', COUNT(DISTINCT CASE WHEN started=1 AND verify_started=1 AND verify_completed=1 AND submitted=1 THEN application_id END) FROM application_stages
UNION ALL SELECT 'application_completed', COUNT(DISTINCT CASE WHEN started=1 AND verify_started=1 AND verify_completed=1 AND submitted=1 AND completed=1 THEN application_id END) FROM application_stages;
