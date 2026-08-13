#!/usr/bin/env python3
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src'))
from harbor_analytics.capstone import write_capstone
if __name__ == '__main__':
    tables=write_capstone(ROOT/'data/synthetic')
    print('Generated deterministic Chapter 23 evidence: '+', '.join(f'{k}={len(v)}' for k,v in tables.items()))
