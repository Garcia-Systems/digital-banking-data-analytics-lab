-- COUNT(*) counts events, not sessions; DISTINCT answers a session question.
SELECT COUNT(*), COUNT(DISTINCT session_id) FROM events;
-- Use HAVING after aggregation, not WHERE COUNT(*) > 1.
SELECT session_id, COUNT(*) FROM events GROUP BY session_id HAVING COUNT(*) > 1;
-- 100.0 prevents integer division; NULLIF makes a missing denominator NULL, not failure.
-- A LEFT JOIN to non-unique event rows can multiply records: aggregate each side first.
-- `outcome = NULL` is never true; use `outcome IS NULL`.
SELECT outcome, COUNT(*) FROM events GROUP BY outcome;
-- Absence of application_completed means only "not observed," not necessarily "failed."
