#!/usr/bin/env python3
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src'))
from harbor_analytics.dataset import write_events
from harbor_analytics.dirty import generate_dirty_events
if __name__ == '__main__':
    target=ROOT/'data/synthetic/digital_events_dirty.csv'; write_events(target, generate_dirty_events()); print(f'Wrote {target.relative_to(ROOT)}')
