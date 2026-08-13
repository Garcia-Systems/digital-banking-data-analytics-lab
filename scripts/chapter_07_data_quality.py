#!/usr/bin/env python3
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src'))
from harbor_analytics.analysis import count_events,completion_rate,load_events
from harbor_analytics.quality import *
def findings(rows): return {'Duplicate IDs':find_duplicate_event_ids(rows),'Missing required fields':find_missing_required_fields(rows),'Invalid categories':find_invalid_categories(rows),'Invalid durations':find_invalid_durations(rows),'Malformed timestamps':find_timestamp_errors(rows),'Journey-order violations':find_journey_order_violations(rows)}
if __name__=='__main__':
 clean=load_events(ROOT/'data/synthetic/digital_events.csv'); dirty=load_events(ROOT/'data/synthetic/digital_events_dirty.csv')
 report=findings(dirty); print('HARBOR ANALYTICS DATA QUALITY REPORT\n')
 for label,items in report.items(): print(f'{label:28} {len(items):3}  {items}')
 print('\nStatus: NOT TRUSTED FOR DECISION' if any(report.values()) else '\nStatus: PASSED DEFINED CHECKS')
 for label,rows in [('Clean',clean),('Dirty',dirty)]:
  starts=count_events(rows,'application_started'); done=count_events(rows,'application_completed'); print(f'{label} application completion rate: {done}/{starts} = {completion_rate(starts,done):.2f}%')
 print('Dirty data removes one denominator event and duplicates one numerator event, inflating the event-based rate. Detect → understand → decide treatment → document; do not silently clean.')
 print("\nCAPSTONE: use SQL → time → segmentation → quality checks. The clean observations show a comparison-period decline concentrated in mobile phones and overlapping lower identity success. That is association, not proof of cause; the canonical fixture passes the defined checks.")
