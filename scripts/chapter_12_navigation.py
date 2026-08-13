#!/usr/bin/env python3
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src'))
from harbor_analytics.analysis import load_events
from harbor_analytics.navigation import *

if __name__ == '__main__':
    events=load_events(ROOT/'data/synthetic/digital_events.csv'); summary=search_summary(events)
    print('NAVIGATION AND SEARCH (21-day UTC window)')
    print('Entry pages:',entry_pages(events)); print('Transitions:',navigation_transitions(events))
    print('Searches by normalized category:',searches_by_category(events)); print('Search summary:',summary)
    print(f"No-result rate = {summary['no_results']} no-result searches / {summary['searches']} searches = {summary['no_result_rate']:.1f}%")
    print(f"Selection rate = {summary['selected_results']} selections / {summary['searches']} searches = {summary['selection_rate']:.1f}%")
    print('\nObserved search and navigation paths are friction signals, not causes. Raw member-entered search text is not collected.')
    print('Hypothesis for the lab: card-management navigation may be difficult to discover; validate with further evidence.')
