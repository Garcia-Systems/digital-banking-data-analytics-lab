#!/usr/bin/env python3
from pathlib import Path
from statistics import mean
import sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src'))
from harbor_analytics.analysis import load_events
from harbor_analytics.journeys import *

if __name__ == '__main__':
    events=load_events(ROOT/'data/synthetic/digital_events.csv'); grouped=group_by_application(events); funnel=build_funnel(events)
    drops={s:stage_dropoff_count(funnel,s) for s in ACCOUNT_OPENING_STAGES[1:]}; largest=max(drops,key=drops.get)
    failed=sum(e['event_name']=='identity_verification_failed' for e in events)
    latencies=[e['api_duration_ms'] for e in events if e['api_duration_ms']]
    print('HARBOR ENGINEERING ANALYTICS REPORT\n')
    print('QUESTION\nWhere in the recorded account-opening journey should engineering investigate?')
    print(f'\nPOPULATION\n{len(grouped)} synthetic applications observed 2025-01-06 through 2025-01-26 UTC.')
    print('\nFUNNEL')
    for stage,count in funnel.items(): print(f'{stage:35} {count:3} ({count/funnel[ACCOUNT_OPENING_STAGES[0]]*100:5.1f}% of starts)')
    print(f'\nLARGEST OBSERVED DROP\n{drops[largest]} applications before {largest}.')
    print('\nLAST OBSERVED STAGE')
    for stage,count in abandonment_by_stage(events).items(): print(f'{stage:35} {count:3}')
    print(f'\nSEGMENTATION\nIncomplete applications by channel: {incomplete_by_segment(events,"channel")}')
    print(f'\nFRICTION EVIDENCE\nRecorded verification failures: {failed}; mean nonzero API duration: {mean(latencies):.0f} ms.')
    print('\nOBSERVATIONS\nThe counts, channel grouping, recorded outcomes, and timing fields above are established by this fixture.')
    print('\nHYPOTHESES TO INVESTIGATE\nThe mobile verification flow or its integration may merit investigation. Corroborate with API, vendor, and application telemetry.')
    print('\nUNSUPPORTED CONCLUSIONS\nThese data do not prove intent, malfunction, dissatisfaction, or vendor causation.')
