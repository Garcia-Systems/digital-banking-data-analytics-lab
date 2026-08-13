"""Readable journey, funnel, and friction calculations for Chapters 8–10."""
from __future__ import annotations

from collections import Counter
from collections.abc import Iterable
from datetime import datetime

from .analysis import Event, rate

ACCOUNT_OPENING_STAGES = (
    "application_started",
    "identity_verification_started",
    "identity_verification_completed",
    "application_submitted",
    "application_completed",
)


def events_for_application(events: Iterable[Event], application_id: str) -> list[Event]:
    """Return one application's events in timestamp order."""
    return sorted((e for e in events if e["application_id"] == application_id), key=lambda e: e["timestamp"])


def group_by_application(events: Iterable[Event]) -> dict[str, list[Event]]:
    grouped: dict[str, list[Event]] = {}
    for event in events:
        if event["application_id"]:
            grouped.setdefault(event["application_id"], []).append(event)
    return {key: sorted(value, key=lambda e: e["timestamp"]) for key, value in grouped.items()}


def ordered_journey(events: Iterable[Event]) -> list[str]:
    """Return distinct observed stages in valid forward order.

    Repeats are collapsed. A later stage cannot imply a missing earlier stage, and
    out-of-order stages are ignored rather than rewritten into a plausible journey.
    """
    result: list[str] = []
    expected = 0
    for event in sorted(events, key=lambda e: e["timestamp"]):
        name = event["event_name"]
        if expected < len(ACCOUNT_OPENING_STAGES) and name == ACCOUNT_OPENING_STAGES[expected]:
            result.append(name)
            expected += 1
    return result


def reached_stage(events: Iterable[Event], stage: str) -> bool:
    return stage in ordered_journey(events)


journey_stage_reached = reached_stage


def journey_is_complete(events: Iterable[Event]) -> bool:
    return ordered_journey(events) == list(ACCOUNT_OPENING_STAGES)


def last_reached_stage(events: Iterable[Event]) -> str | None:
    journey = ordered_journey(events)
    return journey[-1] if journey else None


def stage_count(events: Iterable[Event], stage: str) -> int:
    return sum(reached_stage(journey, stage) for journey in group_by_application(events).values())


def build_funnel(events: Iterable[Event]) -> dict[str, int]:
    grouped = group_by_application(events)
    return {stage: sum(reached_stage(value, stage) for value in grouped.values()) for stage in ACCOUNT_OPENING_STAGES}


def stage_conversion_rate(funnel: dict[str, int], stage: str) -> float:
    index = ACCOUNT_OPENING_STAGES.index(stage)
    if index == 0:
        return 100.0 if funnel.get(stage, 0) else 0.0
    return rate(funnel.get(stage, 0), funnel.get(ACCOUNT_OPENING_STAGES[index - 1], 0))


def overall_conversion_rate(funnel: dict[str, int]) -> float:
    return rate(funnel.get(ACCOUNT_OPENING_STAGES[-1], 0), funnel.get(ACCOUNT_OPENING_STAGES[0], 0))


def stage_dropoff_count(funnel: dict[str, int], stage: str) -> int:
    index = ACCOUNT_OPENING_STAGES.index(stage)
    return 0 if index == 0 else funnel.get(ACCOUNT_OPENING_STAGES[index - 1], 0) - funnel.get(stage, 0)


def stage_dropoff_rate(funnel: dict[str, int], stage: str) -> float:
    index = ACCOUNT_OPENING_STAGES.index(stage)
    return 0.0 if index == 0 else rate(stage_dropoff_count(funnel, stage), funnel.get(ACCOUNT_OPENING_STAGES[index - 1], 0))


def incomplete_journeys(events: Iterable[Event]) -> dict[str, list[Event]]:
    return {key: value for key, value in group_by_application(events).items() if not journey_is_complete(value)}


def abandonment_by_stage(events: Iterable[Event]) -> dict[str, int]:
    counts = Counter(last_reached_stage(value) for value in group_by_application(events).values())
    return {stage: counts[stage] for stage in ACCOUNT_OPENING_STAGES}


def incomplete_by_segment(events: Iterable[Event], dimension: str) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for journey in incomplete_journeys(events).values():
        counts[str(journey[0][dimension])] += 1
    return dict(sorted(counts.items()))


def stage_duration(events: Iterable[Event], start_stage: str, end_stage: str) -> float | None:
    """Elapsed seconds between first ordered observations of two stages."""
    ordered = sorted(events, key=lambda e: e["timestamp"])
    start = next((e for e in ordered if e["event_name"] == start_stage), None)
    end = next((e for e in ordered if e["event_name"] == end_stage and (start is None or e["timestamp"] >= start["timestamp"])), None)
    if not start or not end:
        return None
    return (datetime.fromisoformat(end["timestamp"].replace("Z", "+00:00")) - datetime.fromisoformat(start["timestamp"].replace("Z", "+00:00"))).total_seconds()


def journey_duration(events: Iterable[Event]) -> float | None:
    return stage_duration(events, ACCOUNT_OPENING_STAGES[0], ACCOUNT_OPENING_STAGES[-1])
