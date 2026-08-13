from datetime import datetime, timezone
from pathlib import Path
import sqlite3
from harbor_analytics.analysis import count_events, load_events
from harbor_analytics.database import build_database
from harbor_analytics.dataset import generate_events, write_events
from harbor_analytics.dirty import generate_dirty_events
from harbor_analytics.quality import (find_duplicate_event_ids, find_invalid_categories, find_invalid_durations,
 find_journey_order_violations, find_missing_required_fields, find_timestamp_errors)
from harbor_analytics.segmentation import completion_by_segment
from harbor_analytics.time_analysis import compare_periods, daily_event_counts, events_between, group_by_day

def test_sqlite_generation_counts_and_python_agreement(tmp_path: Path):
 events=generate_events(); db=tmp_path/'a.sqlite'; build_database(db,events)
 with sqlite3.connect(db) as con:
  assert con.execute('select count(*) from events').fetchone()[0]==len(events)
  assert con.execute('select count(distinct session_id) from events').fetchone()[0]==210
  assert con.execute("select count(*) from events where event_name='application_completed'").fetchone()[0]==count_events(events,'application_completed')
  assert dict(con.execute("select channel,count(*) from events where event_name='application_started' group by channel"))=={'mobile':85,'web':83}

def test_daily_grouping_and_half_open_window():
 events=generate_events(); groups=group_by_day(events)
 assert len(groups)==21 and daily_event_counts(events,'application_started')['2025-01-06']==8
 selected=events_between(events,datetime(2025,1,6,tzinfo=timezone.utc),datetime(2025,1,7,tzinfo=timezone.utc))
 assert selected==groups['2025-01-06']

def test_comparison_differences_and_zero_baseline():
 result=compare_periods(70,63)
 assert result=={'absolute_difference':-7,'percentage_point_difference':-7,'relative_percentage_change':-10.0}
 assert compare_periods(0,5)['relative_percentage_change'] is None

def test_segmentation_multiple_dimensions_and_empty():
 events=generate_events(); by_channel=completion_by_segment(events,('channel',))
 assert by_channel[('mobile',)]['starts']==85 and by_channel[('web',)]['completions']==78
 assert completion_by_segment(events,('channel','device_type'))[('mobile','phone')]['rate']==70/85*100
 assert completion_by_segment([],('channel',))=={}

def test_all_dirty_findings():
 dirty=generate_dirty_events()
 assert find_duplicate_event_ids(dirty)==['evt-00011']
 assert find_missing_required_fields(dirty)
 assert find_invalid_categories(dirty)==[(2,'channel','Mobile')]
 assert find_invalid_durations(dirty)==[3]
 assert find_timestamp_errors(dirty)==[5]
 assert 'd03-app-03' in find_journey_order_violations(dirty)
 assert 'd02-app-02' in find_journey_order_violations(dirty)

def test_clean_has_no_findings():
 clean=generate_events()
 assert not any((find_duplicate_event_ids(clean),find_missing_required_fields(clean),find_invalid_categories(clean),find_invalid_durations(clean),find_timestamp_errors(clean),find_journey_order_violations(clean)))

def test_dirty_and_clean_fixture_reproducibility(tmp_path: Path):
 one=tmp_path/'one.csv'; two=tmp_path/'two.csv'; write_events(one,generate_dirty_events()); write_events(two,generate_dirty_events())
 assert one.read_bytes()==two.read_bytes()
 clean=tmp_path/'clean.csv'; write_events(clean); assert load_events(clean)==generate_events()
