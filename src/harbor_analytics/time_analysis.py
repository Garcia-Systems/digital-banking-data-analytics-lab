"""Explicit UTC time grouping and comparison-window helpers."""
from __future__ import annotations
from collections import defaultdict
from collections.abc import Iterable
from datetime import datetime
from .analysis import Event, rate

def parse_timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))

def events_between(events: Iterable[Event], start: datetime, end: datetime) -> list[Event]:
    """Return events in the half-open interval [start, end)."""
    return [event for event in events if start <= parse_timestamp(event["timestamp"]) < end]

def group_by_day(events: Iterable[Event]) -> dict[str, list[Event]]:
    groups: dict[str, list[Event]] = defaultdict(list)
    for event in events:
        groups[parse_timestamp(event["timestamp"]).date().isoformat()].append(event)
    return dict(sorted(groups.items()))

def daily_event_counts(events: Iterable[Event], event_name: str) -> dict[str, int]:
    return {day: sum(e["event_name"] == event_name for e in rows) for day, rows in group_by_day(events).items()}

def daily_rate(events: Iterable[Event], numerator: str, denominator: str) -> dict[str, dict[str, float | int]]:
    result = {}
    for day, rows in group_by_day(events).items():
        top = sum(e["event_name"] == numerator for e in rows)
        bottom = sum(e["event_name"] == denominator for e in rows)
        result[day] = {"numerator": top, "denominator": bottom, "rate": rate(top, bottom)}
    return result

def compare_periods(baseline: float, comparison: float) -> dict[str, float | None]:
    return {"absolute_difference": comparison - baseline,
            "percentage_point_difference": comparison - baseline,
            "relative_percentage_change": ((comparison - baseline) / baseline * 100) if baseline else None}
