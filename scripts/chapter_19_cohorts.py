#!/usr/bin/env python3
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"src"))
from harbor_analytics.decisions import cohort_completion
rows=[]
for week,completed,verified in [("2025-03-03",8,9),("2025-03-10",9,9),("2025-03-17",6,7)]:
    rows += [{"started_at":f"{week}T{10+i:02d}:00:00Z","completed":i<completed,"verification_completed":i<verified} for i in range(10)]
print("Cohort       Size Completed Completion Verification Mature/safe to compare")
for r in cohort_completion(rows,"2025-03-22T23:59:59Z"):
    print(f"{r['cohort']} {r['size']:5} {r['completion_count']:9} {r['completion_rate']:10.1%} {r['verification_rate']:12.1%} {str(r['mature']):>8}")
print("\nRight censoring: not completed yet is not always abandoned; compare mature cohorts with equal observation windows.")
