#!/usr/bin/env python3
"""Calculate Chapter 0 observations using transparent Python operations."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from harbor_analytics import (  # noqa: E402
    completion_rate, count_events, group_by_channel, load_events, unique_sessions,
)

DATA = ROOT / "data" / "synthetic" / "digital_events.csv"


def main() -> None:
    events = load_events(DATA)
    starts = count_events(events, "application_started")
    completions = count_events(events, "application_completed")
    starts_by_channel = group_by_channel(events, "application_started")
    completions_by_channel = group_by_channel(events, "application_completed")

    print("Harbor Federal — Chapter 0 observations")
    print("=" * 42)
    print(f"Total events: {len(events)}")
    print(f"Unique sessions: {unique_sessions(events)}")
    print(f"Web sessions: {unique_sessions(events, 'web')}")
    print(f"Mobile sessions: {unique_sessions(events, 'mobile')}")
    print(f"Application starts: {starts}")
    print(f"Application completions: {completions}")
    print(f"Overall application completion rate: {completion_rate(starts, completions):.1f}%")
    for channel in ("web", "mobile"):
        channel_starts = starts_by_channel.get(channel, 0)
        channel_completions = completions_by_channel.get(channel, 0)
        print(
            f"{channel.title()} application completion rate: "
            f"{channel_completions}/{channel_starts} "
            f"({completion_rate(channel_starts, channel_completions):.1f}%)"
        )


if __name__ == "__main__":
    main()

