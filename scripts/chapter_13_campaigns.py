#!/usr/bin/env python3
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src'))
from harbor_analytics.analysis import load_events
from harbor_analytics.campaigns import campaign_metrics,campaign_funnels
from harbor_analytics.experience import completion_by_dimension

if __name__ == '__main__':
    events=load_events(ROOT/'data/synthetic/digital_events.csv')
    print('OBSERVED CAMPAIGN ARRIVALS AND APPLICATIONS')
    for campaign,row in campaign_metrics(events).items():
        print(campaign, row)
    print('\nCAMPAIGN FUNNELS',campaign_funnels(events))
    print('\nDEVICE CHECK',completion_by_dimension((e for e in events if e['campaign_id']),'device_type'))
    print('\nThese campaign tags describe behavior after observed arrival, not ad exposure or causal attribution.')
    print('Before blaming a campaign, compare its channel/device mix and funnel stage. Technical telemetry is not analyzed yet.')
    print('\nNEXT: Digital experience -> Harbor API -> vendor integration -> database -> errors/latency/outcomes.')
    print('Part IV asks: what was the application/API/vendor actually doing during these sessions?')
