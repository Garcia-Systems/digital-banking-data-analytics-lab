-- Chapter 23 investigation starters. These queries expose evidence, not a conclusion.
-- Application is the unit: count one application_started event per application.
WITH apps AS (
  SELECT application_id, MIN(substr(event_timestamp,1,10)) AS start_date,
         MAX(event_name='application_completed') AS completed
  FROM capstone_journey_events GROUP BY application_id
)
SELECT CASE WHEN start_date <= '2025-05-14' THEN 'baseline' ELSE 'comparison' END period,
       COUNT(*) starts, SUM(completed) completions,
       ROUND(100.0*SUM(completed)/COUNT(*),1) completion_percent
FROM apps GROUP BY period ORDER BY period;

-- Change start: do not smooth away the daily counts.
WITH apps AS (
 SELECT application_id, substr(MIN(event_timestamp),1,10) day,
        MAX(event_name='application_completed') completed
 FROM capstone_journey_events GROUP BY application_id)
SELECT day, COUNT(*) starts, SUM(completed) completions,
       ROUND(100.0*SUM(completed)/COUNT(*),1) completion_percent
FROM apps GROUP BY day ORDER BY day;

-- Endpoint latency/error comparison. NTILE gives an inspectable SQLite p95.
WITH ranked AS (
 SELECT endpoint, CASE WHEN timestamp<'2025-05-15' THEN 'baseline' ELSE 'comparison' END period,
        CAST(duration_ms AS INTEGER) duration_ms, CAST(status_code AS INTEGER) status_code,
        NTILE(20) OVER (PARTITION BY endpoint, CASE WHEN timestamp<'2025-05-15' THEN 'baseline' ELSE 'comparison' END
                        ORDER BY CAST(duration_ms AS INTEGER)) bucket
 FROM capstone_api_requests)
SELECT endpoint, period, COUNT(*) requests,
 ROUND(AVG(duration_ms),1) average_ms,
 MAX(CASE WHEN bucket<=19 THEN duration_ms END) approximate_p95_ms,
 ROUND(100.0*SUM(status_code>=400)/COUNT(*),1) error_percent
FROM ranked GROUP BY endpoint,period ORDER BY endpoint,period;
