#!/usr/bin/env python3
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src'))
from harbor_analytics.analysis import load_events
from harbor_analytics.journeys import events_for_application, ordered_journey, journey_is_complete, last_reached_stage

if __name__ == '__main__':
    events=load_events(ROOT/'data/synthetic/digital_events.csv')
    for application in ('app-0012','app-0001','app-0112'):
        journey=events_for_application(events,application)
        print(f"Application: {application}\nChannel: {journey[0]['channel']}\n")
        print('\n        ↓\n'.join(ordered_journey(journey)))
        status='COMPLETE' if journey_is_complete(journey) else f'LAST OBSERVED STAGE = {last_reached_stage(journey)}'
        print(f'\nStatus: {status}\n')
    print('Observation: an incomplete sequence has no later expected stage recorded; it does not establish a cause.')
