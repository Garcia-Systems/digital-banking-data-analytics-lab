#!/usr/bin/env python3
"""Show the distinct evidence contributed by each source system."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from harbor_analytics.analysis import group_count, load_events  # noqa: E402

events = load_events(ROOT / "data/synthetic/digital_events.csv")
print("Chapter 1 — source-system evidence (observed synthetic data)")
for source, count in sorted(group_count(events, "source_system").items()):
    rows = [event for event in events if event["source_system"] == source]
    sessions = sorted({event["session_id"] for event in rows})
    channels = sorted({event["channel"] for event in rows})
    types = sorted({event["event_name"] for event in rows})
    print(f"\n{source}: {count} events")
    print(f"  sessions represented: {len(sessions)}")
    print(f"  channels represented: {', '.join(channels)}")
    print(f"  event types: {', '.join(types)}")
print("\nObservation: sources contribute different evidence; this does not establish causation.")
