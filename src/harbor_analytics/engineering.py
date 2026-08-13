"""Synthetic application-layer telemetry and transparent Part IV calculations."""
from __future__ import annotations

import csv
import math
import sqlite3
from collections import Counter, defaultdict
from pathlib import Path

FIELDS = {
    "api_requests": ["request_id", "timestamp", "correlation_id", "session_id", "application_id", "endpoint", "method", "status_code", "duration_ms", "outcome", "channel", "device_type", "period"],
    "integration_calls": ["integration_request_id", "correlation_id", "timestamp", "provider", "operation", "outcome", "provider_status", "duration_ms", "attempt_number", "retryable", "period"],
    "database_queries": ["query_id", "timestamp", "correlation_id", "query_name", "operation_type", "table_category", "duration_ms", "rows_examined", "rows_returned", "outcome", "period"],
    "error_events": ["error_id", "timestamp", "correlation_id", "component", "error_category", "severity", "endpoint", "provider", "recoverable", "member_visible", "period"],
}

def percentile(values: list[int], percentage: float) -> int | float:
    """Nearest-rank percentile: sorted value at ceil(p/100*n), with rank >= 1."""
    if not values: return 0
    if not 0 <= percentage <= 100: raise ValueError("percentage must be 0..100")
    ordered = sorted(values)
    return ordered[max(1, math.ceil(percentage / 100 * len(ordered))) - 1]

def api_metrics(rows):
    durations = [int(r["duration_ms"]) for r in rows]; successes = sum(r["outcome"] == "success" for r in rows)
    return {"volume": len(rows), "success_count": successes, "error_count": len(rows)-successes,
            "success_rate": successes/len(rows) if rows else 0, "error_rate": (len(rows)-successes)/len(rows) if rows else 0,
            "average_latency": sum(durations)/len(durations) if durations else 0,
            "median_latency": percentile(durations, 50), "p95_latency": percentile(durations, 95)}

def group_by(rows, field):
    result = defaultdict(list)
    for row in rows: result[row[field]].append(row)
    return dict(result)

def requests_by_endpoint(rows): return {k: len(v) for k, v in group_by(rows, "endpoint").items()}
def error_rate_by_endpoint(rows): return {k: api_metrics(v)["error_rate"] for k, v in group_by(rows, "endpoint").items()}
def latency_by_endpoint(rows): return {k: api_metrics(v) for k, v in group_by(rows, "endpoint").items()}
def status_codes_by_endpoint(rows): return {k: dict(Counter(r["status_code"] for r in v)) for k, v in group_by(rows, "endpoint").items()}

def integration_metrics(rows):
    n=len(rows); successes=sum(r["outcome"]=="success" for r in rows); timeouts=sum(r["outcome"]=="timeout" for r in rows)
    operations=group_by(rows, "correlation_id"); retried={k:v for k,v in operations.items() if len(v)>1}
    recovered=sum(any(r["outcome"]!="success" for r in v[:-1]) and v[-1]["outcome"]=="success" for v in retried.values())
    op_success=sum(v[-1]["outcome"]=="success" for v in operations.values())
    durations=[int(r["duration_ms"]) for r in rows]
    return {"call_volume":n, "success_rate":successes/n if n else 0, "timeout_rate":timeouts/n if n else 0,
            "average_latency":sum(durations)/n if n else 0, "p95_latency":percentile(durations,95),
            "retry_rate":len(retried)/len(operations) if operations else 0, "recovered_operations":recovered,
            "unrecovered_operations":sum(v[-1]["outcome"]!="success" for v in operations.values()),
            "retry_recovery_rate":recovered/len(retried) if retried else 0,
            "operation_success_rate":op_success/len(operations) if operations else 0}

def slow_queries(rows, threshold=250): return [r for r in rows if int(r["duration_ms"]) >= threshold]
def repeated_queries(rows, threshold=5):
    counts=Counter((r["correlation_id"],r["query_name"]) for r in rows)
    return {key:n for key,n in counts.items() if n>=threshold}
def error_counts(rows, field="component"): return dict(Counter(r[field] for r in rows))
def member_visible_errors(rows): return sum(str(r["member_visible"]).lower()=="true" for r in rows)
def timeline(rows): return sorted(rows, key=lambda r:r["timestamp"])

def query_plan_demonstration():
    """Return SQLite plan details before/after an educational index."""
    db=sqlite3.connect(":memory:")
    db.execute("CREATE TABLE demo (id INTEGER, query_label TEXT)")
    db.executemany("INSERT INTO demo VALUES (?,?)", [(i, f'label-{i%10}') for i in range(100)])
    before=db.execute("EXPLAIN QUERY PLAN SELECT * FROM demo WHERE query_label='label-3'").fetchall()
    db.execute("CREATE INDEX demo_label_idx ON demo(query_label)")
    after=db.execute("EXPLAIN QUERY PLAN SELECT * FROM demo WHERE query_label='label-3'").fetchall()
    db.close()
    return [r[3] for r in before], [r[3] for r in after]

def generate():
    api=[]; calls=[]; queries=[]; errors=[]
    for i in range(1,21):
        incident=i>10; period="incident" if incident else "baseline"; app=f"app-{i+100:04d}"; corr=f"corr-{i:04d}"; session=f"p4-session-{i:02d}"
        minute=(i-1)%10; stamp=f"2025-01-{20 if incident else 19:02d}T13:{minute:02d}:00Z"
        api.append({"request_id":f"req-{i:04d}","timestamp":stamp,"correlation_id":corr,"session_id":session,"application_id":app,"endpoint":"/api/applications/{id}/verify","method":"POST","status_code":"504" if incident and i in (12,15,18) else "200","duration_ms":1950 if incident and i in (11,12,14,15,17,18) else 180+i,"outcome":"error" if incident and i in (12,15,18) else "success","channel":"mobile" if i%3 else "web","device_type":"phone" if i%3 else "desktop","period":period})
        # First-call timeout; most retries recover, one does not.
        call_out="timeout" if incident and i in (11,12,14,15,17,18) else "success"
        calls.append({"integration_request_id":f"int-{i:04d}-1","correlation_id":corr,"timestamp":stamp,"provider":"Beacon Identity Labs","operation":"identity_verification","outcome":call_out,"provider_status":"deadline_exceeded" if call_out=="timeout" else "verified","duration_ms":1800 if call_out=="timeout" else 150+i,"attempt_number":1,"retryable":str(call_out=="timeout").lower(),"period":period})
        if call_out=="timeout":
            recovered=i!=18
            calls.append({"integration_request_id":f"int-{i:04d}-2","correlation_id":corr,"timestamp":stamp[:-3]+"30Z","provider":"Beacon Identity Labs","operation":"identity_verification","outcome":"success" if recovered else "timeout","provider_status":"verified" if recovered else "deadline_exceeded","duration_ms":400 if recovered else 1800,"attempt_number":2,"retryable":str(not recovered).lower(),"period":period})
        qdur=620 if i==13 else 35+i
        queries.append({"query_id":f"qry-{i:04d}-p","timestamp":stamp,"correlation_id":corr,"query_name":"lookup_application","operation_type":"select","table_category":"applications","duration_ms":qdur,"rows_examined":5000 if i==13 else 1,"rows_returned":1,"outcome":"success","period":period})
        if i==16: # analytically visible N+1
            for child in range(1,11): queries.append({"query_id":f"qry-{i:04d}-{child}","timestamp":stamp,"correlation_id":corr,"query_name":"load_account_detail","operation_type":"select","table_category":"accounts","duration_ms":45,"rows_examined":1,"rows_returned":1,"outcome":"success","period":period})
        if call_out=="timeout": errors.append({"error_id":f"err-{i:04d}","timestamp":stamp,"correlation_id":corr,"component":"identity_adapter","error_category":"provider_timeout","severity":"warning" if i!=18 else "error","endpoint":"/api/applications/{id}/verify","provider":"Beacon Identity Labs","recoverable":str(i!=18).lower(),"member_visible":str(i in (12,15,18)).lower(),"period":period})
    return {"api_requests":api,"integration_calls":calls,"database_queries":queries,"error_events":errors}

def write_fixtures(directory: str|Path):
    directory=Path(directory); directory.mkdir(parents=True,exist_ok=True)
    for name, rows in generate().items():
        with (directory/f"{name}.csv").open("w",newline="") as f:
            writer=csv.DictWriter(f,fieldnames=FIELDS[name]); writer.writeheader(); writer.writerows(rows)

def read_fixture(path):
    with Path(path).open(newline="") as f: return list(csv.DictReader(f))

def trace_application(application_id, data):
    api=[r for r in data["api_requests"] if r["application_id"]==application_id]
    if not api: return []
    corr=api[0]["correlation_id"]
    return timeline(api+[r for r in data["integration_calls"] if r["correlation_id"]==corr])
