#!/usr/bin/env python3
"""Print each analytical SQL statement beside its answer."""
from pathlib import Path
import sqlite3, sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src'))
from harbor_analytics.analysis import count_events, load_events
QUERIES={
'Total event count':'SELECT COUNT(*) AS events FROM events',
'Unique session count':'SELECT COUNT(DISTINCT session_id) AS sessions FROM events',
'Application starts':"SELECT COUNT(*) AS starts FROM events WHERE event_name='application_started'",
'Application completions':"SELECT COUNT(*) AS completions FROM events WHERE event_name='application_completed'",
'Completion by channel':"SELECT channel, COUNT(DISTINCT CASE WHEN event_name='application_started' THEN session_id END) starts, COUNT(DISTINCT CASE WHEN event_name='application_completed' THEN session_id END) completions, ROUND(100.0*COUNT(DISTINCT CASE WHEN event_name='application_completed' THEN session_id END)/NULLIF(COUNT(DISTINCT CASE WHEN event_name='application_started' THEN session_id END),0),1) rate FROM events GROUP BY channel ORDER BY channel",
'Identity-verification outcomes':"SELECT event_name, outcome, COUNT(*) count FROM events WHERE event_name LIKE 'identity_verification_%' GROUP BY event_name,outcome ORDER BY event_name",
'Events by source system':'SELECT source_system, COUNT(*) count FROM events GROUP BY source_system ORDER BY count DESC'
}
if __name__=='__main__':
    db=ROOT/'data/generated/harbor_analytics.sqlite'
    if not db.exists(): raise SystemExit('Run python3 scripts/build_analytics_db.py first')
    with sqlite3.connect(db) as con:
        for name,sql in QUERIES.items():
            print(f'\n=== {name} ===\n{sql}\nResult:'); print(*con.execute(sql).fetchall(),sep='\n')
        sql_count=con.execute("SELECT COUNT(*) FROM events WHERE event_name='application_completed'").fetchone()[0]
    python_count=count_events(load_events(ROOT/'data/synthetic/digital_events.csv'),'application_completed')
    print(f'\nIndependent check: SQL={sql_count}, Python={python_count}, agree={sql_count==python_count}')
    print('Independent implementations can expose duplicated rows, wrong filters, or denominator mistakes.')
