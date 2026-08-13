"""Detection-only checks: treatment remains an explicit engineering decision."""
from __future__ import annotations
from collections import Counter, defaultdict
from collections.abc import Iterable, Mapping
from .time_analysis import parse_timestamp

REQUIRED_FIELDS = ("event_id", "timestamp", "session_id", "channel", "device_type", "event_name", "source_system")
VALID_CATEGORIES = {"channel": {"web", "mobile"}, "device_type": {"desktop", "phone"}}

def find_duplicate_event_ids(events: Iterable[Mapping[str, object]]) -> list[str]:
    counts = Counter(str(e.get("event_id", "")) for e in events)
    return sorted(key for key, count in counts.items() if key and count > 1)

def find_missing_required_fields(events: Iterable[Mapping[str, object]]) -> list[tuple[int, str]]:
    return [(index, field) for index, event in enumerate(events) for field in REQUIRED_FIELDS if event.get(field) in (None, "")]

def find_invalid_categories(events: Iterable[Mapping[str, object]]) -> list[tuple[int, str, object]]:
    return [(index, field, event.get(field)) for index, event in enumerate(events)
            for field, valid in VALID_CATEGORIES.items() if event.get(field) not in (None, "") and event.get(field) not in valid]

def find_invalid_durations(events: Iterable[Mapping[str, object]]) -> list[int]:
    return [index for index, event in enumerate(events) if not isinstance(event.get("duration_ms"), int) or int(event["duration_ms"]) < 0]

def find_timestamp_errors(events: Iterable[Mapping[str, object]]) -> list[int]:
    invalid = []
    for index, event in enumerate(events):
        try: parse_timestamp(str(event.get("timestamp", "")))
        except ValueError: invalid.append(index)
    return invalid

def find_journey_order_violations(events: Iterable[Mapping[str, object]]) -> list[str]:
    sessions: dict[str, list[Mapping[str, object]]] = defaultdict(list)
    for event in events:
        try: parse_timestamp(str(event.get("timestamp", "")))
        except ValueError: continue
        sessions[str(event.get("session_id"))].append(event)
    bad = []
    for session, rows in sessions.items():
        starts = [parse_timestamp(str(e["timestamp"])) for e in rows if e.get("event_name") == "application_started"]
        completions = [parse_timestamp(str(e["timestamp"])) for e in rows if e.get("event_name") == "application_completed"]
        if completions and (not starts or min(completions) < min(starts)): bad.append(session)
    return sorted(bad)
