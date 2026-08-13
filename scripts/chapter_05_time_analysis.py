#!/usr/bin/env python3
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src'))
from harbor_analytics.analysis import load_events
from harbor_analytics.time_analysis import daily_event_counts,daily_rate
if __name__=='__main__':
 e=load_events(ROOT/'data/synthetic/digital_events.csv')
 starts=daily_event_counts(e,'application_started'); completions=daily_event_counts(e,'application_completed')
 completion=daily_rate(e,'application_completed','application_started'); identity=daily_rate(e,'identity_verification_completed','identity_verification_started')
 print('day        starts completed completion (completed/starts) identity-success (completed/started) mobile-events')
 for day, row in completion.items():
  mobile=sum(x['channel']=='mobile' for x in e if x['timestamp'].startswith(day))
  print(f"{day} {starts[day]:6} {completions[day]:9} {row['numerator']}/{row['denominator']}={row['rate']:.1f}% {identity[day]['numerator']}/{identity[day]['denominator']}={identity[day]['rate']:.1f}% {mobile:13}")
 print("\nObservation: recorded rates dip on some days. The overlap with identity failures is an association; these events alone cannot establish vendor causation.")
