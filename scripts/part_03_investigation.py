#!/usr/bin/env python3
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src'))
from harbor_analytics.analysis import load_events
from harbor_analytics.journeys import build_funnel,overall_conversion_rate
from harbor_analytics.experience import completion_by_dimension,funnel_by_dimension
from harbor_analytics.navigation import search_summary
from harbor_analytics.campaigns import campaign_metrics

if __name__ == '__main__':
 e=load_events(ROOT/'data/synthetic/digital_events.csv'); f=build_funnel(e); search=search_summary(e)
 sections=[
 ('1. Overall observation',f'{f["application_completed"]} of {f["application_started"]} applications completed ({overall_conversion_rate(f):.1f}%).'),
 ('2. Segment analysis',str(completion_by_dimension(e,'channel'))+'; '+str(completion_by_dimension(e,'device_type'))),
 ('3. Funnel location',str(funnel_by_dimension(e,'channel'))),
 ('4. Navigation/search evidence',f'{search["no_results"]} of {search["searches"]} searches had no results ({search["no_result_rate"]:.1f}%); this is a signal, not a cause.'),
 ('5. Campaign evidence',str(campaign_metrics(e))),
 ('6. Confounders','Campaign, channel, and device populations have different mixes; compare like with like.'),
 ('7. Technical investigation leads','Inspect responsive flow, client errors, identity API latency/outcomes, and device compatibility next.'),
 ('8. Supported conclusions','Observed completion, funnel, search, campaign, and segment differences in the fixed window are established.'),
 ('9. Hypotheses','Mobile identity-verification behavior or discoverability might contribute; telemetry must test these ideas.'),
 ('10. Unsupported claims','Do not claim that mobile UI, a campaign, or a vendor caused abandonment or that tags measure every ad exposure.')]
 print('PART III — EVIDENCE-BOUNDED HARBOR INVESTIGATION')
 for title,body in sections: print(f'\n{title}\n{body}')
