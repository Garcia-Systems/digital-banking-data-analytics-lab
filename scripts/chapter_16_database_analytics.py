#!/usr/bin/env python3
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"src"))
from harbor_analytics.engineering import *
rows=read_fixture(ROOT/"data/synthetic/database_queries.csv"); groups=group_by(rows,"query_name")
print("CHAPTER 16 — DATABASE ANALYTICS")
for name, values in groups.items(): print(name,api_metrics(values))
print("Slow queries:",[(r["correlation_id"],r["query_name"]) for r in slow_queries(rows)])
print("Repeated query patterns:",repeated_queries(rows))
print("SQLite teaching query plans (not production MySQL):",query_plan_demonstration())
print("corr-0013 has slow DB behavior; other slow verify requests with fast DB calls point elsewhere.")
