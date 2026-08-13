"""Focused channel/device comparisons built on the Chapter 8 journey model."""
from __future__ import annotations
from collections import defaultdict
from collections.abc import Iterable
from .analysis import Event, average, rate
from .journeys import (ACCOUNT_OPENING_STAGES, abandonment_by_stage, build_funnel,
                       group_by_application, journey_duration)

ALLOWED_DIMENSIONS = {"channel", "device_type", "campaign_id", "traffic_source"}

def _journeys_by(events: Iterable[Event], dimension: str) -> dict[str, list[Event]]:
    if dimension not in ALLOWED_DIMENSIONS:
        raise ValueError(f"unsupported experience dimension: {dimension}")
    groups: dict[str, list[Event]] = defaultdict(list)
    for journey in group_by_application(events).values():
        groups[str(journey[0][dimension]) or "unattributed"].extend(journey)
    return dict(groups)

def funnel_by_dimension(events: Iterable[Event], dimension: str) -> dict[str, dict[str, int]]:
    return {key: build_funnel(value) for key, value in sorted(_journeys_by(events, dimension).items())}

def completion_by_dimension(events: Iterable[Event], dimension: str) -> dict[str, dict[str, float | int]]:
    result = {}
    for key, funnel in funnel_by_dimension(events, dimension).items():
        starts, completed = funnel[ACCOUNT_OPENING_STAGES[0]], funnel[ACCOUNT_OPENING_STAGES[-1]]
        result[key] = {"applications": starts, "completed": completed, "completion_rate": rate(completed, starts)}
    return result

def abandonment_by_dimension(events: Iterable[Event], dimension: str) -> dict[str, dict[str, int]]:
    return {key: abandonment_by_stage(value) for key, value in sorted(_journeys_by(events, dimension).items())}

def duration_by_dimension(events: Iterable[Event], dimension: str) -> dict[str, dict[str, float | int]]:
    result = {}
    for key, values in sorted(_journeys_by(events, dimension).items()):
        durations = [duration for journey in group_by_application(values).values()
                     if (duration := journey_duration(journey)) is not None]
        result[key] = {"completed_with_duration": len(durations), "average_seconds": average(durations)}
    return result
