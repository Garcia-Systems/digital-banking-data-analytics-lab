"""Transparent, standard-library decision analytics for fictional Harbor data."""
from __future__ import annotations

import csv
import hashlib
import math
import random
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from html import escape
from pathlib import Path


TARGETS = {
    "application completion": (0.80, ">="), "mobile completion": (0.80, ">="),
    "verification completion": (0.82, ">="), "API error rate": (0.04, "<="),
    "API p95 latency": (900, "<="), "vendor timeout rate": (0.05, "<="),
}


def absolute_difference(baseline: float, comparison: float) -> float:
    return comparison - baseline


def percentage_point_difference(baseline: float, comparison: float) -> float:
    """Difference in proportions, expressed as percentage points."""
    return (comparison - baseline) * 100


def relative_change(baseline: float, comparison: float) -> float | None:
    """Relative change as a proportion; undefined for a zero baseline."""
    return (comparison - baseline) / baseline if baseline else None


def target_met(value: float, target: float, operator: str = ">=") -> bool:
    if operator == ">=": return value >= target
    if operator == "<=": return value <= target
    raise ValueError("operator must be >= or <=")


def before_after_rows() -> list[dict]:
    """Declared deterministic observations surrounding fictional release hv-next."""
    values = {
        "application completion": (.76, .82), "mobile completion": (.74, .81),
        "verification completion": (.75, .84), "API error rate": (.075, .035),
        "API p95 latency": (1180, 820), "vendor timeout rate": (.09, .04),
    }
    denominator_units = {
        "application completion": "applications", "mobile completion": "mobile applications",
        "verification completion": "verification operations", "API error rate": "API requests",
        "API p95 latency": "API requests", "vendor timeout rate": "provider calls",
    }
    return [{"metric": k, "baseline": v[0], "comparison": v[1],
             "difference": absolute_difference(*v), "target": TARGETS[k][0],
             "operator": TARGETS[k][1], "target_met": target_met(v[1], *TARGETS[k]),
             "baseline_n": 200, "comparison_n": 200, "denominator_unit": denominator_units[k]}
            for k, v in values.items()]


def assign_start_cohort(started_at: str) -> str:
    dt = datetime.fromisoformat(started_at.replace("Z", "+00:00"))
    monday = dt.date() - timedelta(days=dt.weekday())
    return monday.isoformat()


def observation_mature(started_at: str, observed_through: str, days: int = 7) -> bool:
    start = datetime.fromisoformat(started_at.replace("Z", "+00:00"))
    end = datetime.fromisoformat(observed_through.replace("Z", "+00:00"))
    return end - start >= timedelta(days=days)


def cohort_counts(rows: list[dict]) -> dict[str, int]:
    result: dict[str, int] = defaultdict(int)
    for row in rows: result[assign_start_cohort(row["started_at"])] += 1
    return dict(result)


def cohort_completion(rows: list[dict], observed_through: str, maturity_days: int = 7) -> list[dict]:
    groups: dict[str, list[dict]] = defaultdict(list)
    for row in rows: groups[assign_start_cohort(row["started_at"])].append(row)
    output=[]
    for cohort, group in sorted(groups.items()):
        complete=sum(bool(r["completed"]) for r in group); verified=sum(bool(r["verification_completed"]) for r in group)
        mature=all(observation_mature(r["started_at"], observed_through, maturity_days) for r in group)
        output.append({"cohort":cohort,"size":len(group),"completion_count":complete,
                       "completion_rate":complete/len(group),"verification_rate":verified/len(group),"mature":mature})
    return output


def cohort_stage_conversion(rows: list[dict], stage: str) -> dict[str, float]:
    return {r["cohort"]: r[stage] / r["size"] if r["size"] else 0 for r in rows}


EXPERIMENT_FIELDS = ["experiment_id","application_id","variant","assigned_at","channel","device_type",
                     "completed","verification_completed","duration_ms","api_error","verification_retries","support_request"]


def generate_experiment(seed: int = 20250320, size: int = 400) -> list[dict]:
    """Seeded fixture. Assignment draws occur before independent outcome draws.

    B intentionally has higher completion probability but slightly more retries/latency.
    """
    rng=random.Random(seed); rows=[]
    assignments=["B" if rng.random() < .5 else "A" for _ in range(size)]
    for i, variant in enumerate(assignments, 1):
        completed=rng.random() < (.79 if variant=="B" else .73)
        verified=rng.random() < (.84 if variant=="B" else .78)
        error=rng.random() < (.045 if variant=="B" else .04)
        retries=1 if rng.random() < (.12 if variant=="B" else .07) else 0
        support=rng.random() < (.025 if variant=="B" else .03)
        duration=int(rng.gauss(790 if variant=="B" else 720, 110))
        rows.append({"experiment_id":"verification-guidance-01","application_id":f"exp-app-{i:04d}","variant":variant,
          "assigned_at":f"2025-03-{10+(i-1)//40:02d}T{(i-1)%24:02d}:00:00Z","channel":"mobile","device_type":"phone",
          "completed":completed,"verification_completed":verified,"duration_ms":max(duration,100),"api_error":error,
          "verification_retries":retries,"support_request":support})
    return rows


def write_experiment(path: str | Path, seed: int = 20250320, size: int = 400) -> None:
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=EXPERIMENT_FIELDS); w.writeheader(); w.writerows(generate_experiment(seed,size))


def difference_interval(success_a: int, n_a: int, success_b: int, n_b: int, z: float = 1.96) -> tuple[float,float]:
    """Unpooled normal 95% interval for p(B)-p(A); useful, not a causal guarantee."""
    if not n_a or not n_b: raise ValueError("both variants need observations")
    pa=success_a/n_a; pb=success_b/n_b
    se=math.sqrt(pa*(1-pa)/n_a + pb*(1-pb)/n_b)
    return pb-pa-z*se, pb-pa+z*se


def experiment_metrics(rows: list[dict]) -> dict:
    groups={v:[r for r in rows if r["variant"]==v] for v in ("A","B")}
    result={}
    for v,g in groups.items():
        n=len(g); completed=sum(_truth(r["completed"]) for r in g)
        result[v]={"sample_size":n,"completion_count":completed,"completion_rate":completed/n if n else 0,
                   "api_error_rate":sum(_truth(r["api_error"]) for r in g)/n if n else 0,
                   "retry_rate":sum(int(r["verification_retries"])>0 for r in g)/n if n else 0,
                   "support_rate":sum(_truth(r["support_request"]) for r in g)/n if n else 0,
                   "average_duration_ms":sum(int(r["duration_ms"]) for r in g)/n if n else 0}
    a,b=result["A"],result["B"]
    result["difference"]={"absolute":b["completion_rate"]-a["completion_rate"],
      "percentage_points":percentage_point_difference(a["completion_rate"],b["completion_rate"]),
      "relative":relative_change(a["completion_rate"],b["completion_rate"]),
      "confidence_interval":difference_interval(a["completion_count"],a["sample_size"],b["completion_count"],b["sample_size"])}
    return result


def _truth(value) -> bool: return value is True or str(value).lower()=="true"


def communication_reports(metrics: dict | None = None) -> dict[str, dict]:
    m=metrics or experiment_metrics(generate_experiment()); d=m["difference"]["percentage_points"]
    facts={"a_n":m["A"]["sample_size"],"b_n":m["B"]["sample_size"],"a_rate":m["A"]["completion_rate"],"b_rate":m["B"]["completion_rate"],"difference_pp":d}
    wording={
      "engineering":f"EXPERIMENTAL EVIDENCE: mobile completion was {facts['a_rate']:.1%} for A and {facts['b_rate']:.1%} for B ({d:+.1f} pp). Inspect latency and retry guardrails before rollout. NOT ESTABLISHED: behavior outside assigned traffic.",
      "product":f"COMPARISON: revised verification guidance observed {facts['b_rate']:.1%} completion versus {facts['a_rate']:.1%} for existing guidance ({d:+.1f} pp). The experiment supports an experience effect in this sample; practical importance remains a decision.",
      "executive":f"OBSERVED: across {facts['a_n']+facts['b_n']} synthetic mobile applications, B completion was {d:+.1f} pp versus A. Recommendation: review uncertainty and guardrails, then choose rollout, more data, revision, or rollback."}
    return {audience:{"facts":dict(facts),"text":text} for audience,text in wording.items()}


def dashboard_metrics() -> dict:
    exp=experiment_metrics(generate_experiment()); ba={r["metric"]:r for r in before_after_rows()}
    completion_count=exp["A"]["completion_count"]+exp["B"]["completion_count"]
    return {"observation_period":"2025-03-10 through 2025-03-19 UTC (synthetic)","applications":400,
      "completion_count":completion_count,"completion_rate":completion_count/400,
      "api_error_rate":ba["API error rate"]["comparison"],"api_p95_latency":ba["API p95 latency"]["comparison"],
      "vendor_timeout_rate":ba["vendor timeout rate"]["comparison"],"variant_b_count":exp["B"]["completion_count"],
      "variant_b_n":exp["B"]["sample_size"],"variant_b_rate":exp["B"]["completion_rate"]}


def build_dashboard(path: str | Path) -> str:
    m=dashboard_metrics(); cards=[("Applications",str(m["applications"]),"assigned applications"),("Completion",f"{m['completion_count']} / {m['applications']} = {m['completion_rate']:.1%}","completed / assigned applications"),("API error rate",f"{m['api_error_rate']:.1%}","errors / 200 API requests"),("API p95",f"{m['api_p95_latency']:.0f} ms","nearest-rank p95 of 200 API requests")]
    card_html="".join(f'<article class="card"><h3>{escape(a)}</h3><strong>{b}</strong><p>{c}</p></article>' for a,b,c in cards)
    html=f'''<!doctype html><html><head><meta charset="utf-8"><title>Harbor decision dashboard</title><style>body{{font:16px system-ui;max-width:1100px;margin:auto;padding:2rem;background:#f4f7fa;color:#17324d}}.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:1rem}}.card,section{{background:white;padding:1rem;margin:1rem 0;border-radius:8px}}table{{border-collapse:collapse;width:100%}}td,th{{padding:.5rem;border-bottom:1px solid #ccd6df;text-align:left}}</style></head><body><header><h1>Harbor Federal decision dashboard</h1><p><strong>Audience:</strong> engineering, digital product, and operations decision partners.</p><p>Entirely fictional and synthetic. Observation period: {m['observation_period']}.</p></header><main><section id="engineering"><h2>Engineering</h2><p>Question: are technical guardrails healthy enough to consider a product decision?</p><div class="cards">{card_html}</div><table><tr><th>Metric</th><th>Value</th><th>Denominator/context</th></tr><tr><td>Vendor timeout rate</td><td>{m['vendor_timeout_rate']:.1%}</td><td>timeouts / 200 provider calls</td></tr><tr><td>Database/query behavior</td><td>Monitor drill-down</td><td>query executions</td></tr><tr><td>Member-visible errors</td><td>Monitor drill-down</td><td>structured error events</td></tr></table></section><section id="product"><h2>Digital Product</h2><p>Question: did assigned experience B change application completion without unacceptable friction?</p><p>Variant B completion: {m['variant_b_count']} / {m['variant_b_n']} assigned applications = {m['variant_b_rate']:.1%}. Recent incomplete applications may be immature, not abandoned.</p></section><section id="operations"><h2>Operations</h2><p>Question: which observed exceptions need follow-up?</p><p>Review completed/incomplete application counts, verification outcomes, and exception indicators at application grain; do not substitute request or call counts.</p></section><section id="definitions"><h2>Definitions and drill-down</h2><p>Dashboard signal → segment → journey → API/vendor/database evidence → investigation. A signal starts investigation; correlation is not explanation.</p></section></main></body></html>'''
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True); path.write_text(html,encoding="utf-8"); return html


def fixture_digest(rows: list[dict]) -> str:
    return hashlib.sha256(repr(rows).encode()).hexdigest()
