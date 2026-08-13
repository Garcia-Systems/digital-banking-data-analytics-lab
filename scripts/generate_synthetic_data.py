#!/usr/bin/env python3
"""Regenerate the deterministic Chapter 0 event fixture."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from harbor_analytics.dataset import write_events  # noqa: E402

OUTPUT = ROOT / "data" / "synthetic" / "digital_events.csv"

if __name__ == "__main__":
    write_events(OUTPUT)
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")

