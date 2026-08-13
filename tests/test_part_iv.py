import hashlib
from harbor_analytics.engineering import *

def data(): return generate()

def test_api_core_metrics_grouping_and_percentiles():
    rows=data()["api_requests"]; m=api_metrics(rows)
    assert m["volume"]==20 and m["success_count"]==17 and m["error_count"]==3
    assert m["success_rate"]==.85 and m["error_rate"]==.15
    assert m["average_latency"]==717.15 and m["median_latency"]==190 and m["p95_latency"]==1950
    assert requests_by_endpoint(rows)=={"/api/applications/{id}/verify":20}
    assert status_codes_by_endpoint(rows)["/api/applications/{id}/verify"]=={"200":17,"504":3}
    assert error_rate_by_endpoint(rows)["/api/applications/{id}/verify"]==.15
    assert percentile([1,2,3,4,100],95)==100

def test_integration_call_and_operation_reliability_retries():
    m=integration_metrics(data()["integration_calls"])
    assert m["call_volume"]==26 and m["timeout_rate"]==7/26
    assert m["success_rate"]==19/26 and m["retry_rate"]==6/20
    assert m["recovered_operations"]==5 and m["unrecovered_operations"]==1
    assert m["retry_recovery_rate"]==5/6
    assert m["operation_success_rate"]==19/20 > m["success_rate"]

def test_correlation_and_application_trace():
    d=data(); assert all(r["correlation_id"] for rows in d.values() for r in rows)
    trace=trace_application("app-0111",d)
    assert len(trace)==3 and {r["correlation_id"] for r in trace}=={"corr-0011"}
    assert [r["outcome"] for r in trace if "integration_request_id" in r]==["timeout","success"]

def test_database_grouping_slow_n_plus_one_and_plan():
    rows=data()["database_queries"]
    assert len(group_by(rows,"query_name")["lookup_application"])==20
    assert [r["correlation_id"] for r in slow_queries(rows)]==["corr-0013"]
    assert repeated_queries(rows)=={("corr-0016","load_account_detail"):10}
    before,after=query_plan_demonstration(); assert any("SCAN" in x for x in before); assert any("INDEX" in x for x in after)

def test_errors_incident_and_timeline():
    rows=data()["error_events"]
    assert error_counts(rows)=={"identity_adapter":6}; assert member_visible_errors(rows)==3
    assert all(r["period"]=="incident" for r in rows)
    assert timeline(rows)==sorted(rows,key=lambda r:r["timestamp"])
    api=data()["api_requests"]
    assert api_metrics([r for r in api if r["period"]=="incident"])["p95_latency"] > api_metrics([r for r in api if r["period"]=="baseline"])["p95_latency"]

def test_fixture_regeneration_is_byte_deterministic(tmp_path):
    a=tmp_path/"a"; b=tmp_path/"b"; write_fixtures(a); write_fixtures(b)
    for name in FIELDS:
        assert hashlib.sha256((a/f"{name}.csv").read_bytes()).digest()==hashlib.sha256((b/f"{name}.csv").read_bytes()).digest()
