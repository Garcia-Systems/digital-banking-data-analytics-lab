#!/usr/bin/env python3
"""Regenerate deterministic Part V experiment data."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"src"))
from harbor_analytics.decisions import write_experiment
path=ROOT/"data/synthetic/verification_guidance_experiment.csv"
write_experiment(path); print(f"Wrote {path.relative_to(ROOT)}")
