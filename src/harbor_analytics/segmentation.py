"""Session-based application completion segmentation."""
from __future__ import annotations
from collections.abc import Iterable
from .analysis import Event, rate

def completion_by_segment(events: Iterable[Event], dimensions: tuple[str, ...]) -> dict[tuple[str, ...], dict[str, float | int]]:
    rows = list(events)
    starts: dict[tuple[str, ...], set[str]] = {}
    completions: dict[tuple[str, ...], set[str]] = {}
    for event in rows:
        if event["event_name"] not in {"application_started", "application_completed"}: continue
        key = tuple(str(event.get(d) or "<missing>") for d in dimensions)
        target = starts if event["event_name"] == "application_started" else completions
        target.setdefault(key, set()).add(event["session_id"])
    return {key: {"starts": len(sessions), "completions": len(completions.get(key, set())),
                  "rate": rate(len(completions.get(key, set())), len(sessions))}
            for key, sessions in sorted(starts.items())}
