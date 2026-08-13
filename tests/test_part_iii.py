from copy import deepcopy
from pathlib import Path
import sqlite3

from harbor_analytics.database import build_database
from harbor_analytics.dataset import generate_events, write_events
from harbor_analytics.journeys import *


def test_grouping_order_complete_incomplete_and_repeat():
    events=generate_events(); grouped=group_by_application(events)
    assert len(grouped)==168 and events_for_application(events,'app-0002')==grouped['app-0002']
    assert journey_is_complete(grouped['app-0002']) and not journey_is_complete(grouped['app-0001'])
    repeated=deepcopy(grouped['app-0002']); repeated.insert(3,deepcopy(repeated[2]))
    assert ordered_journey(repeated)==list(ACCOUNT_OPENING_STAGES)
    assert last_reached_stage(grouped['app-0001'])=='application_submitted'


def test_missing_and_malformed_order_do_not_imply_progress():
    journey=deepcopy(group_by_application(generate_events())['app-0002'])
    missing=[e for e in journey if e['event_name']!='identity_verification_completed']
    assert ordered_journey(missing)==['application_started','identity_verification_started']
    completion=next(e for e in journey if e['event_name']=='application_completed')
    completion['timestamp']='2020-01-01T00:00:00Z'
    assert not journey_is_complete(journey)


def test_funnel_rates_dropoffs_and_zero_denominators():
    events=generate_events(); funnel=build_funnel(events)
    assert funnel=={'application_started':168,'identity_verification_started':168,'identity_verification_completed':159,'application_submitted':159,'application_completed':148}
    assert stage_count(events,'application_completed')==148
    assert stage_conversion_rate(funnel,'identity_verification_completed')==159/168*100
    assert overall_conversion_rate(funnel)==148/168*100
    assert stage_dropoff_count(funnel,'identity_verification_completed')==9
    assert stage_dropoff_rate(funnel,'identity_verification_completed')==9/168*100
    empty={stage:0 for stage in ACCOUNT_OPENING_STAGES}
    assert overall_conversion_rate(empty)==stage_conversion_rate(empty,'identity_verification_started')==stage_dropoff_rate(empty,'identity_verification_started')==0


def test_abandonment_segmentation_and_durations():
    events=generate_events(); grouped=group_by_application(events)
    assert abandonment_by_stage(events)=={'application_started':0,'identity_verification_started':9,'identity_verification_completed':0,'application_submitted':11,'application_completed':148}
    assert incomplete_by_segment(events,'channel')=={'mobile':15,'web':5}
    assert stage_duration(grouped['app-0002'],'identity_verification_started','identity_verification_completed')==60
    assert journey_duration(grouped['app-0002'])==240 and journey_duration(grouped['app-0001']) is None


def test_python_sql_agreement_and_deterministic_regeneration(tmp_path: Path):
    events=generate_events(); db=tmp_path/'events.sqlite'; build_database(db,events)
    sql=Path('sql/03_account_opening_funnel.sql').read_text()
    with sqlite3.connect(db) as connection: assert dict(connection.execute(sql))==build_funnel(events)
    one=tmp_path/'one.csv'; two=tmp_path/'two.csv'; write_events(one); write_events(two)
    assert one.read_bytes()==two.read_bytes()
