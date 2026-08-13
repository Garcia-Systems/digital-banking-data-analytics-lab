#!/usr/bin/env python3
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"src"))
from harbor_analytics.decisions import build_dashboard
path=ROOT/"dist/dashboard.html"; build_dashboard(path); print(f"Wrote {path.relative_to(ROOT)} (offline; no external assets)")
