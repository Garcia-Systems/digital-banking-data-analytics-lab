#!/usr/bin/env python3
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"src"))
from harbor_analytics.engineering import *
rows=read_fixture(ROOT/"data/synthetic/integration_calls.csv"); print("CHAPTER 15 — VENDOR ANALYTICS",integration_metrics(rows),sep="\n")
print("Evidence justifies investigating fictional Beacon Identity Labs. It does not show that it caused the entire conversion decline.")
