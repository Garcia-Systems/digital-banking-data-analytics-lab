#!/usr/bin/env python3
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"src"))
from harbor_analytics.engineering import *
d={n:read_fixture(ROOT/"data/synthetic"/f"{n}.csv") for n in FIELDS}
base=[r for r in d["api_requests"] if r["period"]=="baseline"]; inc=[r for r in d["api_requests"] if r["period"]=="incident"]
print("PART IV — ENGINEERING INVESTIGATION")
print("\n### Member-visible evidence\nMobile verification completion weakened in the synthetic incident segment.")
print("\n### API evidence\nBaseline",api_metrics(base),"\nIncident",api_metrics(inc))
print("\n### Vendor evidence\n",integration_metrics(d["integration_calls"]))
print("\n### Database evidence\nSlow:",[(r["correlation_id"],r["duration_ms"]) for r in slow_queries(d["database_queries"])],"N+1:",repeated_queries(d["database_queries"]))
print("\n### Error evidence\nMember-visible:",member_visible_errors(d["error_events"]),error_counts(d["error_events"],"error_category"))
print("\n### Timeline"); [print(r["timestamp"],r["error_category"]) for r in timeline(d["error_events"])]
print("\n### Leading engineering hypothesis\nCross-layer evidence supports investigating identity-provider timeouts and retry handling.")
print("\n### Alternative hypotheses\nMobile client behavior, database outliers, and unobserved dependencies remain possible.")
print("\n### What is not established\nSequence and correlation do not prove the provider caused the entire conversion decline; reproduce or experiment.")
