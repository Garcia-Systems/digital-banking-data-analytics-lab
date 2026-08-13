#!/usr/bin/env python3
from pathlib import Path
import argparse, sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src'))
from harbor_analytics.capstone import load_capstone, trace
if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('application_id'); a=p.parse_args()
    rows=trace(load_capstone(ROOT/'data/synthetic'),a.application_id)
    if not rows: raise SystemExit(f'No evidence for {a.application_id}')
    print('TIME\tSOURCE\tOBSERVATION')
    for r in rows: print(f"{r['timestamp']}\t{r['source']}\t{r['observation']}")
