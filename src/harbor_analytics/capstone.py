"""Deterministic evidence and calculations for the Chapter 23 investigation.

All records describe the fictional Harbor Federal Credit Union.  Identifiers are
synthetic correlation keys, not member identifiers.
"""
from __future__ import annotations

import csv
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from statistics import mean, median

BASELINE_END = "2025-05-14"
COMPARISON_START = "2025-05-15"
STAGES = ["application_started", "identity_verification_started",
          "identity_verification_completed", "application_submitted", "application_completed"]
FILES = ("capstone_journey_events", "capstone_api_requests", "capstone_vendor_calls",
         "capstone_database_observations", "capstone_errors", "capstone_navigation",
         "capstone_releases")

def period(timestamp: str) -> str:
    return "baseline" if timestamp[:10] <= BASELINE_END else "comparison"

def percentile(values, p=.95):
    values = sorted(values)
    if not values: return 0
    return values[max(0, int(len(values) * p + .999999) - 1)]

def generate_capstone():
    tables = {name: [] for name in FILES}
    start = datetime(2025, 5, 1, 9, tzinfo=timezone.utc)
    for day in range(28):
        comparison = day >= 14
        for i in range(20):
            n = day * 20 + i + 1
            app, session = f"cap-app-{n:04d}", f"cap-session-{n:04d}"
            mobile = i < (12 if comparison else 10)
            channel = "mobile" if mobile else "web"
            device = "ios" if mobile and i % 2 == 0 else ("android" if mobile else "desktop")
            campaign = "partner" if i < (6 if comparison else 3) else ("email" if i % 4 == 0 else "direct")
            version = "4.8.0" if comparison else "4.7.2"
            t = start + timedelta(days=day, minutes=i * 17)
            req, corr = f"cap-req-{n:04d}", f"cap-corr-{n:04d}"
            # A modest, concentrated deterioration. Partner mix contributes some
            # incomplete journeys, while comparison-mobile adds integration friction.
            mix_drop = campaign == "partner" and n % 5 == 0
            ordinary_drop = n % 19 == 0
            affected_failure = comparison and mobile and (day + i) % 5 == 1
            recovered = comparison and mobile and (day + i) % 5 == 2
            verified = not (mix_drop or ordinary_drop or affected_failure)
            completed = verified and n % 23 != 0
            def event(name, offset):
                tables["capstone_journey_events"].append({"event_timestamp":(t+timedelta(milliseconds=offset)).isoformat().replace('+00:00','Z'),"session_id":session,"application_id":app,"event_name":name,"channel":channel,"device_type":device,"campaign_source":campaign,"request_id":req if name.startswith("identity") else "","correlation_id":corr if name.startswith("identity") else "","app_version":version})
            event(STAGES[0], 0); event(STAGES[1], 1200)
            # All calls have one provider attempt; selected affected calls timeout.
            first_timeout = affected_failure or recovered
            first_latency = 2350 + (n % 8) * 80 if first_timeout else 590 + (n % 7) * 35
            tables["capstone_vendor_calls"].append({"timestamp":(t+timedelta(milliseconds=1350)).isoformat().replace('+00:00','Z'),"application_id":app,"request_id":req,"correlation_id":corr,"provider":"Northstar Identity (fictional)","operation":"verify_identity","attempt":1,"outcome":"timeout" if first_timeout else ("declined" if not verified else "success"),"duration_ms":first_latency})
            if first_timeout:
                retry_success = recovered
                tables["capstone_vendor_calls"].append({"timestamp":(t+timedelta(milliseconds=3900)).isoformat().replace('+00:00','Z'),"application_id":app,"request_id":req,"correlation_id":corr,"provider":"Northstar Identity (fictional)","operation":"verify_identity","attempt":2,"outcome":"success" if retry_success else "timeout","duration_ms":900+(n%6)*70})
            api_status = 200 if verified else (504 if affected_failure else 422)
            api_latency = first_latency + (1050 if recovered else (850 if affected_failure else 90))
            tables["capstone_api_requests"].append({"timestamp":(t+timedelta(milliseconds=1250)).isoformat().replace('+00:00','Z'),"application_id":app,"session_id":session,"request_id":req,"correlation_id":corr,"endpoint":"/v1/identity/verify","method":"POST","status_code":api_status,"duration_ms":api_latency,"app_version":version})
            # Harmless recovered profile errors form a distraction.
            profile_status = 503 if n % 17 == 0 else 200
            tables["capstone_api_requests"].append({"timestamp":(t+timedelta(milliseconds=300)).isoformat().replace('+00:00','Z'),"application_id":app,"session_id":session,"request_id":f"{req}-p","correlation_id":f"{corr}-p","endpoint":"/v1/profile/prefill","method":"GET","status_code":profile_status,"duration_ms":180+n%50,"app_version":version})
            if profile_status == 503:
                tables["capstone_errors"].append({"timestamp":(t+timedelta(milliseconds=350)).isoformat().replace('+00:00','Z'),"application_id":app,"correlation_id":f"{corr}-p","layer":"api","error_code":"PREFILL_RETRY","recovered":"true"})
            if not verified:
                code = "IDENTITY_TIMEOUT" if affected_failure else "IDENTITY_NOT_COMPLETED"
                tables["capstone_errors"].append({"timestamp":(t+timedelta(milliseconds=api_latency+1300)).isoformat().replace('+00:00','Z'),"application_id":app,"correlation_id":corr,"layer":"integration" if affected_failure else "journey","error_code":code,"recovered":"false"})
            if verified:
                event(STAGES[2], api_latency + 1400); event(STAGES[3], api_latency + 4000)
                if completed: event(STAGES[4], api_latency + 6200)
            # Relevant writes remain stable. An unrelated search query slows after day 14.
            tables["capstone_database_observations"].append({"timestamp":(t+timedelta(milliseconds=1100)).isoformat().replace('+00:00','Z'),"application_id":app,"correlation_id":corr,"query_category":"application_state","duration_ms":42+n%15,"rows_examined":1,"slow_query":"false"})
            search_ms = 210+(n%80) if comparison else 75+(n%35)
            tables["capstone_database_observations"].append({"timestamp":(t+timedelta(milliseconds=500)).isoformat().replace('+00:00','Z'),"application_id":app,"correlation_id":f"{corr}-s","query_category":"help_search","duration_ms":search_ms,"rows_examined":350+n%100,"slow_query":str(search_ms>=250).lower()})
            tables["capstone_navigation"].append({"timestamp":t.isoformat().replace('+00:00','Z'),"session_id":session,"application_id":app,"campaign_source":campaign,"entry_page":"/open-account" if campaign!="partner" else "/offers/checking","search_used":str(n%13==0).lower()})
    tables["capstone_releases"] = [
        {"timestamp":"2025-05-01T07:00:00Z","app_version":"4.7.2","component":"digital-onboarding","change_summary":"Routine fictional baseline release"},
        {"timestamp":"2025-05-15T07:00:00Z","app_version":"4.8.0","component":"digital-onboarding","change_summary":"Accessibility labels and copy update"},
    ]
    return tables

def write_capstone(directory: Path):
    tables = generate_capstone(); directory.mkdir(parents=True, exist_ok=True)
    for name, rows in tables.items():
        path = directory / f"{name}.csv"
        with path.open("w", newline="") as f:
            writer=csv.DictWriter(f, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
    return tables

def load_capstone(directory: Path):
    return {name:list(csv.DictReader((directory/f"{name}.csv").open())) for name in FILES}

def applications(events):
    apps={}
    for r in events:
        a=apps.setdefault(r["application_id"], {**r,"stages":set()})
        a["stages"].add(r["event_name"])
    return apps

def overview(events):
    apps=applications(events); out={}
    for p in ("baseline","comparison"):
        rows=[a for a in apps.values() if period(a["event_timestamp"])==p]
        done=sum("application_completed" in a["stages"] for a in rows)
        out[p]={"starts":len(rows),"completions":done,"completion_rate":done/len(rows)}
    out["percentage_point_change"]=(out["comparison"]["completion_rate"]-out["baseline"]["completion_rate"])*100
    return out

def segment(events, field):
    apps=applications(events); groups=defaultdict(lambda:Counter(starts=0, completions=0))
    for a in apps.values():
        key=(period(a["event_timestamp"]),a[field]); groups[key]["starts"]+=1
        groups[key]["completions"] += "application_completed" in a["stages"]
    return [{"period":k[0],field:k[1],**v,"completion_rate":v["completions"]/v["starts"]} for k,v in sorted(groups.items())]

def daily(events):
    apps=applications(events); groups=defaultdict(lambda:Counter(starts=0,completions=0))
    for a in apps.values():
        day=a["event_timestamp"][:10]; groups[day]["starts"]+=1
        groups[day]["completions"] += "application_completed" in a["stages"]
    return [{"date":d,**v,"completion_rate":v["completions"]/v["starts"]} for d,v in sorted(groups.items())]

def funnel(events):
    apps=applications(events); result=[]
    for p in ("baseline","comparison"):
        rows=[a for a in apps.values() if period(a["event_timestamp"])==p]; previous=len(rows)
        for stage in STAGES:
            count=sum(stage in a["stages"] for a in rows)
            result.append({"period":p,"stage":stage,"count":count,"stage_conversion":count/previous if previous else 0,"overall_conversion":count/len(rows)})
            previous=count
    return result

def telemetry(rows, group_field):
    groups=defaultdict(list)
    for r in rows: groups[(period(r["timestamp"]),r[group_field])].append(r)
    out=[]
    for (p,name), rs in sorted(groups.items()):
        durations=[int(r["duration_ms"]) for r in rs]
        failures=sum((int(r["status_code"])>=400) if "status_code" in r else
                     (r["outcome"]!="success" if "outcome" in r else r.get("slow_query")=="true") for r in rs)
        out.append({"period":p,group_field:name,"count":len(rs),"failure_rate":failures/len(rs),"average_ms":mean(durations),"median_ms":median(durations),"p95_ms":percentile(durations)})
    return out

def vendor_operations(rows):
    ops=defaultdict(list)
    for r in rows: ops[(period(r["timestamp"]),r["correlation_id"])].append(r)
    result={}
    for p in ("baseline","comparison"):
        selected=[v for (which,_),v in ops.items() if which==p]
        retries=sum(len(v)>1 for v in selected); recovered=sum(len(v)>1 and v[-1]["outcome"]=="success" for v in selected)
        result[p]={"operations":len(selected),"provider_calls":sum(map(len,selected)),"timeout_calls":sum(r["outcome"]=="timeout" for v in selected for r in v),"retried_operations":retries,"recovered_operations":recovered,"unrecovered_operations":sum(v[-1]["outcome"]!="success" for v in selected)}
    return result

def trace(tables, application_id):
    rows=[]
    for source in FILES:
        for r in tables[source]:
            if r.get("application_id")==application_id:
                rows.append({"timestamp":r.get("event_timestamp",r.get("timestamp","")),"source":source,"observation":r.get("event_name") or r.get("endpoint") or r.get("operation") or r.get("query_category") or r.get("error_code") or r.get("entry_page") or r.get("change_summary")})
    return sorted(rows,key=lambda r:r["timestamp"])
