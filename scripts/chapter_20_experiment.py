#!/usr/bin/env python3
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"src"))
from harbor_analytics.decisions import generate_experiment, experiment_metrics
m=experiment_metrics(generate_experiment())
print("Fictional experiment: existing guidance (A) vs revised mobile guidance (B)")
for v in "AB":
    x=m[v]; print(f"Variant {v}: n={x['sample_size']}, completion={x['completion_rate']:.1%}, API errors={x['api_error_rate']:.1%}, retries={x['retry_rate']:.1%}, mean latency={x['average_duration_ms']:.0f} ms")
d=m['difference']; print(f"B - A: {d['percentage_points']:+.1f} percentage points; relative={d['relative']:+.1%}; approximate 95% interval={d['confidence_interval'][0]:+.1%}..{d['confidence_interval'][1]:+.1%}")
print("\nInterpretation prompts: Is assignment obviously imbalanced? Which guardrails changed? What is supported and uncertain? Choose ROLL OUT, COLLECT MORE DATA, REVISE, or ROLL BACK—analytics does not choose for you.")
