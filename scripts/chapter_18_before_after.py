#!/usr/bin/env python3
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"src"))
from harbor_analytics.decisions import before_after_rows
print("Harbor fictional release: harbor-experience-next | baseline 2025-03-01..07 | comparison 2025-03-10..16")
print(f"{'Metric':30} {'Baseline':>10} {'Comparison':>12} {'Difference':>12} {'Declared target':>17} {'Status':>8}")
for r in before_after_rows():
    rate=r['metric'] not in ('API p95 latency',); fmt=lambda x: f"{x:.1%}" if rate else f"{x:.0f} ms"
    diff=f"{r['difference']:+.1%}" if rate else f"{r['difference']:+.0f} ms"
    print(f"{r['metric']:30} {fmt(r['baseline']):>10} {fmt(r['comparison']):>12} {diff:>12} {(r['operator']+' '+fmt(r['target'])):>17} {('MET' if r['target_met'] else 'NOT MET'):>8}")
print("\nEvidence note: Observed improvement after the release does not by itself prove that the release caused the improvement.")
