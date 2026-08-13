"""Deterministic, wholly fictional Harbor Federal event generation."""

from __future__ import annotations

import csv
from datetime import datetime, timedelta, timezone
from pathlib import Path

from .analysis import Event

FIELDNAMES = list(Event.__annotations__)


def generate_events() -> list[Event]:
    """Build 21 UTC days with a stable baseline and a visible mobile decline."""
    events: list[Event] = []
    base = datetime(2025, 1, 6, 9, 0, tzinfo=timezone.utc)

    def add(day: int, session: str, minute: int, channel: str, device: str,
            name: str, feature: str, outcome: str = "success", duration: int = 0,
            source: str | None = None, application_id: str = "",
            attempt_number: int = 0, error_category: str = "",
            vendor_result: str = "", api_duration_ms: int = 0) -> None:
        events.append(Event(
            event_id=f"evt-{len(events) + 1:05d}",
            timestamp=(base + timedelta(days=day, minutes=minute)).isoformat().replace("+00:00", "Z"),
            session_id=session,
            anonymous_or_synthetic_member_id=f"synthetic-member-{session}",
            channel=channel,
            device_type=device,
            event_name=name,
            page_or_feature=feature,
            outcome=outcome,
            duration_ms=duration,
            source_system=source or ("member_web" if channel == "web" else "mobile_app"),
            application_id=application_id,
            attempt_number=attempt_number,
            error_category=error_category,
            vendor_result=vendor_result,
            api_duration_ms=api_duration_ms,
        ))

    for day in range(21):
        # Mobile grows from three to five of eight daily application sessions.
        mobile_count = 3 if day < 10 else 5
        for number in range(8):
            session = f"d{day + 1:02d}-app-{number + 1:02d}"
            application = f"app-{day * 8 + number + 1:04d}"
            mobile = number >= 8 - mobile_count
            channel, device = ("mobile", "phone") if mobile else ("web", "desktop")
            minute = number * 45
            common = {"application_id": application, "attempt_number": 1}
            add(day, session, minute, channel, device, "page_view", "account_opening", duration=420, **common)
            add(day, session, minute + 1, channel, device, "application_started", "account_opening", duration=900, source="account_opening", **common)
            add(day, session, minute + 2, channel, device, "identity_verification_started", "identity_verification", duration=700, source="identity_provider", api_duration_ms=900 if mobile else 520, **common)
            # Days 14-16 have a short-lived issue concentrated on mobile phones.
            identity_failed = 13 <= day <= 15 and mobile and number % 2 == 1
            ordinary_abandonment = (day + number) % 13 == 0
            if identity_failed:
                add(day, session, minute + 3, channel, device, "identity_verification_failed", "identity_verification", "failure", 1400, "identity_provider", error_category="verification_unavailable", vendor_result="retryable_failure", api_duration_ms=2400, **common)
            else:
                add(day, session, minute + 3, channel, device, "identity_verification_completed", "identity_verification", duration=1500, source="identity_provider", vendor_result="verified", api_duration_ms=1100 if mobile else 700, **common)
                add(day, session, minute + 4, channel, device, "application_submitted", "account_opening", duration=800, source="account_opening", **common)
                if not ordinary_abandonment:
                    add(day, session, minute + 5, channel, device, "application_completed", "account_opening", duration=1100, source="account_opening", **common)

        # One ordinary self-service session per day broadens source-system coverage.
        session = f"d{day + 1:02d}-service"
        channel, device = (("mobile", "phone") if day % 2 else ("web", "desktop"))
        add(day, session, 400, channel, device, "login_success", "login", duration=380, source="harbor_api")
        add(day, session, 401, channel, device, "account_view", "checking_summary", duration=310, source="harbor_api")
    return events


def write_events(path: str | Path, events: list[Event] | None = None) -> None:
    """Write a stable CSV (optionally supplied events, useful for dirty fixtures)."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(generate_events() if events is None else events)
