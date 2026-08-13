#!/usr/bin/env python3
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"src"))
from harbor_analytics.engineering import *
rows=read_fixture(ROOT/"data/synthetic/api_requests.csv")
print("CHAPTER 14 — API ANALYTICS\nOverall:",api_metrics(rows))
for endpoint, metrics in latency_by_endpoint(rows).items(): print(endpoint,metrics)
print("Status codes:",status_codes_by_endpoint(rows))
print("Observation: verify tail latency and errors justify following correlation IDs; they do not establish cause.")
