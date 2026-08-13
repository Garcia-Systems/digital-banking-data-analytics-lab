"""Observed, non-causal campaign-arrival metrics."""
from collections import defaultdict
from collections.abc import Iterable
from .analysis import Event, rate
from .experience import funnel_by_dimension

def campaign_metrics(events: Iterable[Event]) -> dict[str, dict[str, float | int]]:
    grouped: dict[str, list[Event]] = defaultdict(list)
    for event in events:
        if event["campaign_id"]: grouped[event["campaign_id"]].append(event)
    funnels = funnel_by_dimension([e for values in grouped.values() for e in values], "campaign_id")
    result = {}
    for campaign, values in sorted(grouped.items()):
        sessions = len({e["session_id"] for e in values})
        starts = funnels[campaign]["application_started"]
        completed = funnels[campaign]["application_completed"]
        arrivals = len({e["session_id"] for e in values if e["event_name"] == "page_view" and e["page_or_feature"] == "account_opening"})
        result[campaign] = {"sessions": sessions, "application_starts": starts,
            "completed_applications": completed, "completion_rate": rate(completed, starts),
            "landing_arrivals": arrivals, "landing_continuation_rate": rate(starts, arrivals)}
    return result

def campaign_funnels(events: Iterable[Event]) -> dict[str, dict[str, int]]:
    return funnel_by_dimension((e for e in events if e["campaign_id"]), "campaign_id")
