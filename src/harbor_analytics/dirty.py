"""Known, deterministic corruptions kept separate from the canonical fixture."""
from copy import deepcopy
from .analysis import Event
from .dataset import generate_events

def generate_dirty_events() -> list[Event]:
    rows = deepcopy(generate_events())
    duplicate = deepcopy(next(e for e in rows if e["event_name"] == "application_completed")); rows.append(duplicate)
    missing_session = "d02-app-02"
    rows[:] = [e for e in rows if not (e["session_id"] == missing_session and e["event_name"] == "application_started")]
    rows[2]["channel"] = "Mobile"
    rows[3]["duration_ms"] = -50
    rows[4]["channel"] = ""
    rows[5]["timestamp"] = "not-a-timestamp"
    completion = next(e for e in rows if e["session_id"] == "d03-app-03" and e["event_name"] == "application_completed")
    completion["timestamp"] = "2025-01-01T00:00:00Z"
    return rows
