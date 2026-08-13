#!/usr/bin/env python3
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"src"))
from harbor_analytics.engineering import write_fixtures
write_fixtures(ROOT/"data/synthetic"); print("Wrote four deterministic Part IV telemetry fixtures")
