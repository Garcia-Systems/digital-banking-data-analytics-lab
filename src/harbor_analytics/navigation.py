"""Small, session-aware navigation and privacy-conscious search summaries."""
from collections import Counter
from collections.abc import Iterable
from .analysis import Event, rate

def entry_pages(events: Iterable[Event]) -> dict[str, int]:
    first = {}
    for event in sorted(events, key=lambda e: e["timestamp"]):
        if event["event_name"] == "page_view": first.setdefault(event["session_id"], event["page_or_feature"])
    return dict(Counter(first.values()).most_common())

def navigation_transitions(events: Iterable[Event]) -> dict[tuple[str, str], int]:
    return dict(Counter((e["navigation_from"], e["navigation_to"]) for e in events
                        if e["event_name"] == "navigation_click"))

def searches_by_category(events: Iterable[Event]) -> dict[str, int]:
    return dict(Counter(e["search_category"] for e in events if e["event_name"] == "search_started"))

def search_summary(events: Iterable[Event]) -> dict[str, float | int]:
    materialized = list(events)
    starts = [e for e in materialized if e["event_name"] == "search_started"]
    sessions = {e["session_id"] for e in starts}
    no_results = sum(e["event_name"] == "search_no_results" for e in materialized)
    selected = sum(e["event_name"] == "search_result_selected" for e in materialized)
    repeated = sum(count > 1 for count in Counter(e["session_id"] for e in starts).values())
    return {"searches": len(starts), "search_sessions": len(sessions), "no_results": no_results,
            "no_result_rate": rate(no_results, len(starts)), "selected_results": selected,
            "selection_rate": rate(selected, len(starts)), "repeated_search_sessions": repeated}
