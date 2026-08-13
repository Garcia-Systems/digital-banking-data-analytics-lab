#!/usr/bin/env python3
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src'))
from harbor_analytics.analysis import load_events
from harbor_analytics.database import build_database
if __name__ == '__main__':
    target=ROOT/'data/generated/harbor_analytics.sqlite'
    build_database(target, load_events(ROOT/'data/synthetic/digital_events.csv'))
    print(f'Built {target.relative_to(ROOT)} from the reproducible CSV fixture')
