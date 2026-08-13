#!/usr/bin/env python3
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"src"))
from harbor_analytics.decisions import communication_reports
reports=communication_reports(); assert len({tuple(sorted(r['facts'].items())) for r in reports.values()})==1
for audience,r in reports.items(): print(f"\n{audience.upper()} REPORT\n{r['text']}")
print("\nConsistency check: PASS — every audience uses the same numeric fact object.")
