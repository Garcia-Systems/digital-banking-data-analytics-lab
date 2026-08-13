#!/usr/bin/env python3
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src'))
from harbor_analytics.analysis import load_events
from harbor_analytics.database import build_database, add_engineering_telemetry
from harbor_analytics.engineering import FIELDS, read_fixture
from harbor_analytics.capstone import FILES as CAPSTONE_FILES, load_capstone
import sqlite3
if __name__ == '__main__':
    target=ROOT/'data/generated/harbor_analytics.sqlite'
    build_database(target, load_events(ROOT/'data/synthetic/digital_events.csv'))
    add_engineering_telemetry(target, {name: read_fixture(ROOT/'data/synthetic'/f'{name}.csv') for name in FIELDS})
    capstone=load_capstone(ROOT/'data/synthetic')
    with sqlite3.connect(target) as connection:
        for name in CAPSTONE_FILES:
            rows=capstone[name]; columns=list(rows[0])
            connection.execute(f'DROP TABLE IF EXISTS {name}')
            connection.execute(f'CREATE TABLE {name} ({", ".join(c+" TEXT" for c in columns)})')
            connection.executemany(f'INSERT INTO {name} VALUES ({",".join("?" for _ in columns)})',([r[c] for c in columns] for r in rows))
    print(f'Built {target.relative_to(ROOT)} from the reproducible CSV fixture')
