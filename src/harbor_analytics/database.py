"""Rebuildable SQLite projection of the authoritative CSV fixture."""
import sqlite3
from pathlib import Path
from .analysis import Event
from .engineering import FIELDS

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

def add_engineering_telemetry(path: str | Path, fixtures: dict[str, list[dict]]) -> None:
    """Project distinct telemetry sources into distinct SQLite tables."""
    with sqlite3.connect(path) as connection:
        for table, rows in fixtures.items():
            columns=FIELDS[table]
            connection.execute(f"DROP TABLE IF EXISTS {table}")
            connection.execute(f"CREATE TABLE {table} ({','.join(f'{c} TEXT' for c in columns)})")
            connection.executemany(f"INSERT INTO {table} VALUES ({','.join('?' for _ in columns)})",
                                   [[row[c] for c in columns] for row in rows])
