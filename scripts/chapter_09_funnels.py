#!/usr/bin/env python3
from pathlib import Path
import sqlite3, sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src'))
from harbor_analytics.analysis import load_events
from harbor_analytics.journeys import *

if __name__ == '__main__':
    events=load_events(ROOT/'data/synthetic/digital_events.csv'); funnel=build_funnel(events)
    print('HARBOR ACCOUNT OPENING FUNNEL\n\nStage                              Applications  Stage conversion  Drop-off')
    print('-'*79)
    for i,stage in enumerate(ACCOUNT_OPENING_STAGES):
        conversion='—' if i==0 else f'{stage_conversion_rate(funnel,stage):.1f}%'
        print(f"{stage.replace('_',' ').title():35} {funnel[stage]:12} {conversion:>17} {stage_dropoff_count(funnel,stage):9}")
    first=funnel[ACCOUNT_OPENING_STAGES[0]]; last=funnel[ACCOUNT_OPENING_STAGES[-1]]
    print(f'\nOverall completion: {last} / {first} = {overall_conversion_rate(funnel):.1f}%\n')
    print('TEXT FUNNEL (percentage of started applications)')
    labels=('Started','Verify start','Verify done','Submitted','Completed')
    for label,stage in zip(labels,ACCOUNT_OPENING_STAGES):
        pct=100*funnel[stage]/first if first else 0
        print(f'{label:13} {"█"*round(pct/5):20} {pct:5.1f}%')
    db=ROOT/'data/generated/harbor_analytics.sqlite'
    if db.exists():
        with sqlite3.connect(db) as connection:
            sql=dict(connection.execute((ROOT/'sql/03_account_opening_funnel.sql').read_text()))
        print(f'\nPython/SQL funnel agreement: {sql == funnel}')
