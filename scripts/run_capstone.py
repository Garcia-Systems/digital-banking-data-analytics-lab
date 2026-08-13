#!/usr/bin/env python3
from pathlib import Path
import argparse, json, sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src'))
from harbor_analytics.capstone import *

MENU='''HARBOR FEDERAL DIGITAL EXPERIENCE INVESTIGATION

Problem:
Digital account-opening completion has declined. Find out why.

Available analyses:
1. Overview                 7. Vendor integrations
2. Time trend               8. Database
3. Segmentation             9. Errors/timeline
4. Funnel                  10. Application trace
5. Abandonment             11. Hypothesis worksheet
6. API                     12. Final report template

Use --analysis NAME (overview, time, segment, funnel, abandonment, api,
vendor, database, timeline, hypothesis, report) or capstone_trace.py APP_ID.'''
def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--analysis'); args=parser.parse_args()
    data_dir=ROOT/'data/synthetic'
    if not all((data_dir/f'{n}.csv').exists() for n in FILES): write_capstone(data_dir)
    t=load_capstone(data_dir); name=args.analysis
    if not name: print(MENU); return
    events=t['capstone_journey_events']
    if name=='overview': result=overview(events)
    elif name=='time': result=daily(events)
    elif name=='segment': result={f:segment(events,f) for f in ('channel','device_type','campaign_source')}
    elif name=='funnel': result=funnel(events)
    elif name=='abandonment':
        result=Counter(next((s for s in reversed(STAGES) if s in a['stages']),'none') for a in applications(events).values())
    elif name=='api': result=telemetry(t['capstone_api_requests'],'endpoint')
    elif name=='vendor': result={'calls':telemetry(t['capstone_vendor_calls'],'operation'),'operations':vendor_operations(t['capstone_vendor_calls'])}
    elif name=='database': result=telemetry(t['capstone_database_observations'],'query_category')
    elif name=='timeline': result=sorted([r for source in ('capstone_errors','capstone_releases') for r in t[source]],key=lambda x:x['timestamp'])
    elif name=='hypothesis': result={h:{'supporting_evidence':'','contradicting_evidence':'','status':''} for h in ('Mobile UI issue','Campaign traffic mix','Harbor API regression','Identity integration degradation','Database slowdown')}
    elif name=='report': result={k:'' for k in ('OBSERVATION','CROSS-LAYER EVIDENCE','LEADING HYPOTHESIS','ALTERNATIVES','LIMITATION','NEXT ACTION','MEASUREMENT PLAN','ENGINEERING VERSION','PRODUCT / OPERATIONS VERSION','EXECUTIVE VERSION')}
    else: raise SystemExit(f'Unknown analysis: {name}')
    print(json.dumps(result,indent=2,default=dict))
if __name__=='__main__': main()
