#!/usr/bin/env python3
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"src"))
from harbor_analytics.engineering import *
app=sys.argv[1] if len(sys.argv)>1 else "app-0111"; data={n:read_fixture(ROOT/"data/synthetic"/f"{n}.csv") for n in FIELDS}
print("APPLICATION JOURNEY\napplication_started",app)
for row in trace_application(app,data):
    if "request_id" in row: print("HARBOR API",row["method"],row["endpoint"],"duration:",row["duration_ms"],"response:",row["outcome"])
    else: print("VENDOR",row["operation"],"attempt",row["attempt_number"],row["outcome"])
print("APPLICATION JOURNEY\nidentity_verification_completed (only when API outcome succeeded)")
