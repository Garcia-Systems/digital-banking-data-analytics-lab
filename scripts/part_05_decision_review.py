#!/usr/bin/env python3
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"src"))
from harbor_analytics.decisions import before_after_rows, experiment_metrics, generate_experiment
m=experiment_metrics(generate_experiment()); mobile=next(r for r in before_after_rows() if r['metric']=="mobile completion")
print("PART V DECISION REVIEW — fictional Harbor mobile account opening")
print(f"Baseline/before-after: {mobile['baseline']:.1%} → {mobile['comparison']:.1%} ({mobile['difference']:+.1%}). This observation is not causal evidence.")
print("Cohort check: compare only cohorts with a mature, equal seven-day observation window.")
print(f"Experiment: A={m['A']['completion_rate']:.1%} (n={m['A']['sample_size']}), B={m['B']['completion_rate']:.1%} (n={m['B']['sample_size']}), B-A={m['difference']['percentage_points']:+.1f} pp.")
print(f"Guardrails: retry A={m['A']['retry_rate']:.1%}, B={m['B']['retry_rate']:.1%}; latency A={m['A']['average_duration_ms']:.0f} ms, B={m['B']['average_duration_ms']:.0f} ms.")
print("\nDecision options: ROLL OUT | COLLECT MORE DATA | REVISE | ROLL BACK")
print("Learner recommendation required: What improved, by how much, and for whom? Are groups valid? What does assignment add? Which guardrails worsened? What supports rollout? What remains uncertain? What should engineering monitor next?")
