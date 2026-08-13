import pytest
from harbor_analytics.decisions import *

def test_before_after_math_and_targets():
    assert absolute_difference(.74,.81)==pytest.approx(.07)
    assert round(percentage_point_difference(.74,.81),10)==7
    assert round(relative_change(.74,.81),6)==round(.07/.74,6)
    assert relative_change(0,.2) is None
    assert target_met(.81,.80) and target_met(.03,.04,"<=")
    assert len(before_after_rows())==6

def test_cohorts_and_maturity():
    rows=[{"started_at":"2025-03-03T10:00:00Z","completed":True,"verification_completed":True},{"started_at":"2025-03-04T10:00:00Z","completed":False,"verification_completed":True}]
    assert assign_start_cohort(rows[0]["started_at"])=="2025-03-03"
    assert cohort_counts(rows)=={"2025-03-03":2}
    c=cohort_completion(rows,"2025-03-12T10:00:00Z")[0]
    assert c["completion_count"]==1 and c["completion_rate"]==.5 and c["verification_rate"]==1 and c["mature"]
    assert not observation_mature("2025-03-17T00:00:00Z","2025-03-22T00:00:00Z")

def test_experiment_determinism_assignment_metrics_and_interval(tmp_path):
    a=generate_experiment(); b=generate_experiment(); assert a==b and fixture_digest(a)==fixture_digest(b)
    assert {r["variant"] for r in a}=={"A","B"}; m=experiment_metrics(a)
    assert m["A"]["sample_size"]+m["B"]["sample_size"]==400
    assert m["difference"]["absolute"]==m["B"]["completion_rate"]-m["A"]["completion_rate"]
    lo,hi=m["difference"]["confidence_interval"]; assert lo < m["difference"]["absolute"] < hi
    assert all(k in m["A"] for k in ("api_error_rate","retry_rate","support_rate","average_duration_ms"))
    p=tmp_path/"x.csv"; write_experiment(p); first=p.read_bytes(); write_experiment(p); assert p.read_bytes()==first

def test_dashboard_structure_and_metric_consistency(tmp_path):
    html=build_dashboard(tmp_path/"dashboard.html"); m=dashboard_metrics()
    for section in ("Engineering","Digital Product","Operations","Definitions and drill-down"): assert section in html
    assert f"{m['completion_rate']:.1%}" in html and "http://" not in html and "https://" not in html

def test_communication_same_facts():
    reports=communication_reports(); assert set(reports)=={"engineering","product","executive"}
    facts=[r["facts"] for r in reports.values()]; assert facts[0]==facts[1]==facts[2]
    assert all(any(label in r["text"] for label in ("OBSERVED","COMPARISON","EXPERIMENTAL EVIDENCE")) for r in reports.values())
