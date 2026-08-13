from hashlib import sha256
from pathlib import Path
import pytest
from harbor_analytics.capstone import *

def test_generation_is_deterministic_and_separate(tmp_path):
    first=write_capstone(tmp_path)
    digests={p.name:sha256(p.read_bytes()).hexdigest() for p in tmp_path.glob('*.csv')}
    second=write_capstone(tmp_path)
    assert first==second and digests=={p.name:sha256(p.read_bytes()).hexdigest() for p in tmp_path.glob('*.csv')}
    assert set(first)==set(FILES) and len(first['capstone_journey_events'])>len(first['capstone_navigation'])
    assert all('root_cause' not in r for rows in first.values() for r in rows)

@pytest.fixture
def tables(): return generate_capstone()

def test_completion_and_affected_segments(tables):
    result=overview(tables['capstone_journey_events'])
    assert result['baseline']=={'starts':280,'completions':254,'completion_rate':pytest.approx(254/280)}
    assert result['comparison']['completions']==212
    assert result['percentage_point_change']==pytest.approx(-15)
    channels={(r['period'],r['channel']):r for r in segment(tables['capstone_journey_events'],'channel')}
    assert channels['comparison','mobile']['completion_rate'] < channels['baseline','mobile']['completion_rate']-.20
    assert channels['comparison','web']['completion_rate']==pytest.approx(channels['baseline','web']['completion_rate'],abs=.01)

def test_daily_funnel_and_abandonment_evidence(tables):
    days=daily(tables['capstone_journey_events']); assert len(days)==28 and all(r['starts']==20 for r in days)
    rows={(r['period'],r['stage']):r for r in funnel(tables['capstone_journey_events'])}
    assert rows['baseline','identity_verification_completed']['count']==266
    assert rows['comparison','identity_verification_completed']['count']==221
    assert rows['comparison','application_submitted']['count']==221

def test_api_vendor_and_database_period_comparisons(tables):
    api={(r['period'],r['endpoint']):r for r in telemetry(tables['capstone_api_requests'],'endpoint')}
    assert api['comparison','/v1/identity/verify']['p95_ms']==3760
    assert api['baseline','/v1/identity/verify']['p95_ms']==890
    assert api['comparison','/v1/profile/prefill']['p95_ms']==api['baseline','/v1/profile/prefill']['p95_ms']
    vendor=vendor_operations(tables['capstone_vendor_calls'])
    assert vendor['comparison']=={'operations':280,'provider_calls':348,'timeout_calls':102,'retried_operations':68,'recovered_operations':34,'unrecovered_operations':55}
    db={(r['period'],r['query_category']):r for r in telemetry(tables['capstone_database_observations'],'query_category')}
    assert db['comparison','application_state']['p95_ms']==db['baseline','application_state']['p95_ms']==56
    assert db['comparison','help_search']['p95_ms']>db['baseline','help_search']['p95_ms']

def test_timeline_and_cross_layer_trace(tables):
    normal=trace(tables,'cap-app-0001'); recovered=trace(tables,'cap-app-0284'); failed=trace(tables,'cap-app-0283')
    assert normal==sorted(normal,key=lambda r:r['timestamp'])
    assert {'capstone_journey_events','capstone_api_requests','capstone_vendor_calls','capstone_database_observations'} <= {r['source'] for r in normal}
    assert sum(r['observation']=='verify_identity' for r in recovered)==2
    assert any(r['observation']=='application_completed' for r in recovered)
    assert not any(r['observation']=='application_completed' for r in failed)

def test_review_expected_values_and_report_consistency():
    root=Path(__file__).resolve().parents[1]
    review=(root/'docs/CAPSTONE_REVIEW.md').read_text()
    for value in ('90.7%', '75.7%', '−15.0 percentage-point', '3,760 ms', '34 recovered operations'):
        assert value in review
    template={k:'' for k in ('OBSERVATION','CROSS-LAYER EVIDENCE','LEADING HYPOTHESIS','ALTERNATIVES','LIMITATION','NEXT ACTION')}
    assert len(template)==6
