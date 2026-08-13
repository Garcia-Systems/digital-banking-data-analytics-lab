-- Chapter 12: event-grain counts; each denominator is stated explicitly.
SELECT page_or_feature, COUNT(*) AS page_views FROM events
WHERE event_name = 'page_view' GROUP BY page_or_feature ORDER BY page_views DESC;

SELECT search_category, COUNT(*) AS searches FROM events
WHERE event_name = 'search_started' GROUP BY search_category ORDER BY searches DESC;

SELECT 100.0 * SUM(event_name = 'search_no_results') /
       NULLIF(SUM(event_name = 'search_started'), 0) AS no_result_rate
FROM events;

SELECT search_category, COUNT(*) AS selected_results FROM events
WHERE event_name = 'search_result_selected' GROUP BY search_category;

SELECT navigation_from, navigation_to, COUNT(*) AS transitions FROM events
WHERE event_name = 'navigation_click'
GROUP BY navigation_from, navigation_to ORDER BY transitions DESC;
