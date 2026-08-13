"""Small, explicit analytics operations used throughout the opening chapters."""

from __future__ import annotations

import csv
from collections.abc import Iterable
from pathlib import Path
from typing import TypedDict


class Event(TypedDict):
    event_id: str
    timestamp: str
    session_id: str
    anonymous_or_synthetic_member_id: str
    channel: str
    device_type: str
    event_name: str
    page_or_feature: str
    outcome: str
    duration_ms: int
    source_system: str
    application_id: str
    attempt_number: int
    error_category: str
    vendor_result: str
    api_duration_ms: int
    traffic_source: str
    campaign_id: str
    landing_page: str
    referral_category: str
    search_category: str
    navigation_from: str
    navigation_to: str


def load_events(path: str | Path) -> list[Event]:
    """Load events from CSV, converting duration to an integer."""
    with Path(path).open(newline="", encoding="utf-8") as source:
        rows = csv.DictReader(source)
        events: list[Event] = []
        for row in rows:
            row["duration_ms"] = int(row["duration_ms"])
            row["attempt_number"] = int(row["attempt_number"])
            row["api_duration_ms"] = int(row["api_duration_ms"])
            events.append(Event(**row))
        return events


def unique_sessions(events: Iterable[Event], channel: str | None = None) -> int:
    """Count distinct sessions, optionally restricted to a channel."""
    return len(
        {
            event["session_id"]
            for event in events
            if channel is None or event["channel"] == channel
        }
    )


def filter_events(
    events: Iterable[Event], event_name: str | None = None, **attributes: object
) -> list[Event]:
    """Return events matching an optional name and exact field values."""
    return [
        event for event in events
        if (event_name is None or event["event_name"] == event_name)
        and all(event.get(key) == value for key, value in attributes.items())
    ]


def count_events(events: Iterable[Event], event_name: str | None = None) -> int:
    """Count all events, or only events with an exact event name."""
    return sum(1 for _ in filter_events(events, event_name))


def group_count(events: Iterable[Event], dimension: str) -> dict[str, int]:
    """Count events by a named field; missing fields appear as ``<missing>``."""
    counts: dict[str, int] = {}
    for event in events:
        value = str(event.get(dimension, "<missing>"))
        counts[value] = counts.get(value, 0) + 1
    return counts


def rate(numerator: int, denominator: int) -> float:
    """Return a percentage, using 0.0 when the denominator is zero."""
    return numerator / denominator * 100 if denominator else 0.0


def average(values: Iterable[int | float]) -> float:
    """Return the arithmetic mean, or 0.0 for empty input."""
    materialized = list(values)
    return sum(materialized) / len(materialized) if materialized else 0.0


def average_duration(events: Iterable[Event]) -> float:
    """Return mean recorded event duration in milliseconds, or 0.0 if empty."""
    return average(event["duration_ms"] for event in events)


def completion_rate(starts: int, completions: int) -> float:
    """Return completions per start as a percentage; zero starts is safe."""
    return rate(completions, starts)


def group_by_channel(events: Iterable[Event], event_name: str) -> dict[str, int]:
    """Count a named event by channel."""
    counts: dict[str, int] = {}
    for event in events:
        if event["event_name"] == event_name:
            channel = event["channel"]
            counts[channel] = counts.get(channel, 0) + 1
    return counts
