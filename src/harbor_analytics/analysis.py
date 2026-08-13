"""Small, explicit analytics operations used in Chapter 0."""

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


def load_events(path: str | Path) -> list[Event]:
    """Load events from CSV, converting duration to an integer."""
    with Path(path).open(newline="", encoding="utf-8") as source:
        rows = csv.DictReader(source)
        events: list[Event] = []
        for row in rows:
            row["duration_ms"] = int(row["duration_ms"])
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


def count_events(events: Iterable[Event], event_name: str) -> int:
    """Count rows whose event name exactly matches ``event_name``."""
    return sum(event["event_name"] == event_name for event in events)


def completion_rate(starts: int, completions: int) -> float:
    """Return completions per start as a percentage; zero starts is safe."""
    return (completions / starts * 100) if starts else 0.0


def group_by_channel(events: Iterable[Event], event_name: str) -> dict[str, int]:
    """Count a named event by channel."""
    counts: dict[str, int] = {}
    for event in events:
        if event["event_name"] == event_name:
            channel = event["channel"]
            counts[channel] = counts.get(channel, 0) + 1
    return counts
