#!/usr/bin/env python3
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src'))
from harbor_analytics.analysis import load_events
from harbor_analytics.segmentation import completion_by_segment
if __name__=='__main__':
 e=load_events(ROOT/'data/synthetic/digital_events.csv')
 for dimensions in [('channel',),('device_type',),('channel','device_type'),('source_system',)]:
  print('\nBY '+' + '.join(dimensions))
  for key,value in completion_by_segment(e,dimensions).items(): print(key, value)
 mobile=[x for x in e if x['channel']=='mobile' and x['device_type']=='phone']
 attempts=sum(x['event_name']=='identity_verification_started' for x in mobile); successes=sum(x['event_name']=='identity_verification_completed' for x in mobile)
 print(f'\nDrill-down: overall → mobile → phone → identity verification: {successes}/{attempts}')
 print('Always retain sample size: 1/1 at 100% is less evidence than 9,500/10,000 at 95%.')
 print("Simpson's paradox: a changing group mix can reverse an aggregate comparison even when each group's direction is unchanged.")
