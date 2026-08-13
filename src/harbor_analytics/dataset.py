"""Deterministic, fictional event generation for the first lesson."""

from __future__ import annotations

import csv
from datetime import datetime, timedelta, timezone
from pathlib import Path

from .analysis import Event

FIELDNAMES = list(Event.__annotations__)


def generate_events() -> list[Event]:
    """Build a small fixed dataset with no random or current-time inputs."""
    events: list[Event] = []
    base = datetime(2025, 1, 13, 14, 0, tzinfo=timezone.utc)

    def add(session: int, minute: int, channel: str, device: str, name: str,
            feature: str, outcome: str = "success", duration: int = 0) -> None:
        events.append(
            Event(
                event_id=f"evt-{len(events) + 1:04d}",
                timestamp=(base + timedelta(minutes=minute)).isoformat().replace("+00:00", "Z"),
                session_id=f"session-{session:03d}",
                anonymous_or_synthetic_member_id=f"synthetic-member-{session:03d}",
                channel=channel,
                device_type=device,
                event_name=name,
                page_or_feature=feature,
                outcome=outcome,
                duration_ms=duration,
            )
        )

    # Ten application journeys: web sessions 1-6 complete except 6; mobile
    # sessions 7-10 complete only 7-8. This creates a visible hypothesis, not a cause.
    for session in range(1, 11):
        channel, device = ("web", "desktop") if session <= 6 else ("mobile", "phone")
        start = (session - 1) * 10
        add(session, start, channel, device, "page_view", "account_opening", duration=420)
        add(session, start + 1, channel, device, "application_started", "account_opening", duration=900)
        add(session, start + 2, channel, device, "identity_verification_started", "identity_verification", duration=700)
        if session not in {9, 10}:
            add(session, start + 3, channel, device, "identity_verification_completed", "identity_verification", duration=1500)
            add(session, start + 4, channel, device, "application_submitted", "account_opening", duration=800)
        if session not in {6, 9, 10}:
            add(session, start + 5, channel, device, "application_completed", "account_opening", duration=1100)

    # Two ordinary self-service journeys ensure the fixture covers other digital events.
    add(11, 110, "web", "desktop", "page_view", "login", duration=250)
    add(11, 111, "web", "desktop", "login_success", "login", duration=640)
    add(11, 112, "web", "desktop", "account_view", "checking_summary", duration=310)
    add(12, 120, "mobile", "phone", "login_success", "biometric_login", duration=380)
    add(12, 121, "mobile", "phone", "transfer_started", "internal_transfer", duration=510)
    add(12, 122, "mobile", "phone", "transfer_completed", "internal_transfer", duration=760)
    return events


def write_events(path: str | Path) -> None:
    """Write the canonical fixture with stable ordering and line endings."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(generate_events())

