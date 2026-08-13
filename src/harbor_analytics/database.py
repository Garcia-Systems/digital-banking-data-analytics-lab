"""Rebuildable SQLite projection of the authoritative CSV fixture."""
import sqlite3
from pathlib import Path
from .analysis import Event

SCHEMA = """CREATE TABLE events (event_id TEXT PRIMARY KEY, timestamp TEXT NOT NULL,
session_id TEXT NOT NULL, anonymous_or_synthetic_member_id TEXT, channel TEXT NOT NULL,
device_type TEXT NOT NULL, event_name TEXT NOT NULL, page_or_feature TEXT, outcome TEXT,
duration_ms INTEGER, source_system TEXT NOT NULL, application_id TEXT, attempt_number INTEGER,
error_category TEXT, vendor_result TEXT, api_duration_ms INTEGER, traffic_source TEXT,
campaign_id TEXT, landing_page TEXT, referral_category TEXT, search_category TEXT,
navigation_from TEXT, navigation_to TEXT);
CREATE INDEX idx_events_name ON events(event_name);
CREATE INDEX idx_events_timestamp ON events(timestamp);"""

def build_database(path: str | Path, events: list[Event]) -> None:
    destination = Path(path); destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists(): destination.unlink()
    with sqlite3.connect(destination) as connection:
        connection.executescript(SCHEMA)
        fields = list(Event.__annotations__)
        connection.executemany(f"INSERT INTO events ({','.join(fields)}) VALUES ({','.join('?' for _ in fields)})",
                               [[event[field] for field in fields] for event in events])
