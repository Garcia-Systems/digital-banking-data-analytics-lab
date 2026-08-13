#!/usr/bin/env python3
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src'))
from harbor_analytics.analysis import load_events
from harbor_analytics.experience import *

if __name__ == '__main__':
    events=load_events(ROOT/'data/synthetic/digital_events.csv')
    print('ACCOUNT OPENING BY CHANNEL\n\nChannel       Applications  Completed  Completion')
    for group,row in completion_by_dimension(events,'channel').items():
        print(f"{group:<13}{row['applications']:>12}{row['completed']:>11}{row['completion_rate']:>11.1f}%")
    for dimension in ('channel','device_type'):
        print(f'\nFUNNEL BY {dimension.upper()} (same 21-day UTC window)')
        for group,funnel in funnel_by_dimension(events,dimension).items(): print(group, ' -> '.join(f'{s}: {n}' for s,n in funnel.items()))
    print('\nABANDONMENT BY CHANNEL', abandonment_by_dimension(events,'channel'))
    print('COMPLETED-JOURNEY DURATION', duration_by_dimension(events,'channel'))
    print('\nObserved: groups differ, with denominators shown. This association does not establish that the UI caused the difference.')
    print('Hypotheses to inspect: responsive forms, JavaScript errors, latency, API/vendor behavior, and compatibility.')
