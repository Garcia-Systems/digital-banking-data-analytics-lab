from pathlib import Path
import sqlite3
from harbor_analytics.dataset import generate_events,write_events
from harbor_analytics.database import build_database
from harbor_analytics.experience import completion_by_dimension,funnel_by_dimension,abandonment_by_dimension
from harbor_analytics.navigation import navigation_transitions,search_summary,searches_by_category
from harbor_analytics.campaigns import campaign_metrics,campaign_funnels


def test_channel_device_counts_completion_and_denominators():
 e=generate_events(); channel=completion_by_dimension(e,'channel'); device=completion_by_dimension(e,'device_type')
 assert channel['mobile']=={'applications':85,'completed':70,'completion_rate':70/85*100}
 assert channel['web']=={'applications':83,'completed':78,'completion_rate':78/83*100}
 assert device['phone']==channel['mobile'] and device['desktop']==channel['web']
 assert sum(row['applications'] for row in channel.values())==168


def test_dimension_funnel_and_abandonment_are_application_grain():
 e=generate_events(); funnels=funnel_by_dimension(e,'channel'); abandoned=abandonment_by_dimension(e,'channel')
 assert funnels['mobile']['identity_verification_completed']==76
 assert funnels['web']['application_completed']==78
 assert abandoned['mobile']['identity_verification_started']==9
 assert abandoned['web']['application_submitted']==5


def test_navigation_search_event_and_session_denominators():
 e=generate_events(); summary=search_summary(e)
 assert navigation_transitions(e)=={('dashboard','card_management'):6,('dashboard','search'):15}
 assert searches_by_category(e)=={'replace_card':13,'transfer_status':5}
 assert summary['searches']==18 and summary['search_sessions']==16
 assert summary['no_results']==3 and summary['no_result_rate']==3/18*100
 assert summary['selected_results']==12 and summary['selection_rate']==12/18*100
 assert summary['repeated_search_sessions']==2


def test_campaign_counts_rates_and_funnels():
 e=generate_events(); metrics=campaign_metrics(e); funnels=campaign_funnels(e)
 checking=metrics['campaign-checking-summer']; mobile=metrics['campaign-mobile-banking']
 assert (checking['sessions'],checking['application_starts'],checking['completed_applications'])==(42,42,37)
 assert checking['completion_rate']==37/42*100
 assert (mobile['sessions'],mobile['application_starts'],mobile['completed_applications'])==(84,84,72)
 assert mobile['completion_rate']==72/84*100
 assert funnels['campaign-checking-summer']['identity_verification_completed']==39
 assert funnels['campaign-mobile-banking']['application_completed']==72


def test_python_sql_navigation_agreement_and_regeneration(tmp_path: Path):
 e=generate_events(); db=tmp_path/'events.sqlite'; build_database(db,e)
 with sqlite3.connect(db) as con:
  sql_rate=con.execute("SELECT 100.0*SUM(event_name='search_no_results')/NULLIF(SUM(event_name='search_started'),0) FROM events").fetchone()[0]
  sql_campaign=dict(con.execute("SELECT campaign_id,COUNT(DISTINCT CASE WHEN event_name='application_completed' THEN application_id END) FROM events WHERE campaign_id<>'' GROUP BY campaign_id"))
 assert abs(sql_rate-search_summary(e)['no_result_rate']) < 1e-12
 assert sql_campaign=={key:value['completed_applications'] for key,value in campaign_metrics(e).items()}
 a=tmp_path/'a.csv'; b=tmp_path/'b.csv'; write_events(a); write_events(b); assert a.read_bytes()==b.read_bytes()
