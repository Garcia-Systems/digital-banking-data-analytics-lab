#!/usr/bin/env python3
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"src"))
from harbor_analytics.engineering import *
rows=read_fixture(ROOT/"data/synthetic/error_events.csv")
print("CHAPTER 17 — ERROR AND INCIDENT ANALYTICS\nBy component:",error_counts(rows),"\nMember-visible:",member_visible_errors(rows))
for r in timeline(rows): print(r["timestamp"],r["component"],r["error_category"],"visible="+r["member_visible"])
print("Sequence supports investigation, not causation.")
