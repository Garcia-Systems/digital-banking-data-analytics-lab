# Chapter 23 review — evidence-bounded interpretation

[← Return to the investigation](../chapters/23-the-harbor-federal-digital-experience-investigation.md)

Read this only after completing the worksheet. Values below come from the committed deterministic fixture; they are not a field naming a root cause.

## Expected observations

* The application-grain baseline has **280 starts, 254 completions, 90.7%** completion. The comparison has **280, 212, 75.7%**: a **−15.0 percentage-point** difference (not “15%”). Daily counts shift beginning May 15.
* Mobile moves from **128/140 (91.4%)** to **111/168 (66.1%)** while web is essentially stable: **126/140 (90.0%)** to **101/112 (90.2%)**. Mobile's traffic share also rises from 50% to 60%, so mix amplifies—but cannot alone explain—the within-mobile deterioration. iOS and Android both deteriorate.
* Partner traffic rises from 42 to 84 starts and its observed rate changes from 95.2% to 59.5%. Direct also deteriorates while email is comparatively stable. Campaign composition is relevant, but mobile deterioration across sources means it is not a complete explanation.

## Funnel and friction

The largest transition change is verification started → completed: **266/280 (95.0%)** versus **221/280 (78.9%)**. Submitted → completed remains similar (**254/266, 95.5%** versus **212/221, 95.9%**). Thus “the final completion endpoint broke” is poorly supported. Affected incomplete traces end at verification started and contain longer operations, timeout errors, and unrecovered attempts. These are correlated friction signals, not experimental proof of cause.

## Engineering layers

For `/v1/identity/verify`, request volume remains 280 per period, but error rate moves from **5.0% to 21.1%**, average from **785 ms to 1,464.6 ms**, median only from **785 to 820 ms**, and p95 from **890 to 3,760 ms**. `/v1/profile/prefill` retains a 5.7% recovered-error rate and stable p95 of 227 ms; it is a useful distraction rather than a leading path-aligned signal.

Provider-call grain and logical-operation grain differ. Baseline contains **280 calls / 280 operations**, no timeouts or retries, and 14 final unsuccessful outcomes. Comparison contains **348 calls / 280 operations**, **102 timeout attempts**, **68 retried operations**, **34 recovered operations**, and **55 final unsuccessful operations**. Counting 102 timeouts as 102 member-visible failures would be wrong because retries recover 34 operations.

The relevant `application_state` database observations are stable: 280 per period, average about 49 ms, and p95 56 ms. `help_search` p95 increases from 108 to 286 ms and slow observations rise, but this category is not on the verification state path. It is interesting, warrants its own follow-up, and does not make database degradation the leading explanation for this journey change.

Release 4.8.0 appears at the comparison boundary and remains a possible alternative or interaction: observational coincidence cannot rule out a client behavior change. Its recorded scope is copy/accessibility, and stable web plus provider-correlated traces contradict a broad release-only story, but code review and reproduction are still appropriate. Temporal order aligns experience, API, vendor, and error signals; it does not prove causation.

## Hypothesis review

| Hypothesis | Defensible status | Why |
| --- | --- | --- |
| Mobile UI issue | POSSIBLE | Mobile concentration and release timing support inspection; provider attempts and stable web contradict a UI-only account. |
| Campaign traffic mix | WEAKLY SUPPORTED / contributing | Mix changed and partner results are worse; within-mobile and cross-layer changes remain. |
| Harbor API regression | POSSIBLE | `/verify` tail/error behavior changed, but its timing follows the same correlated provider attempts; instrumentation cannot isolate all server handling. |
| Identity integration degradation | SUPPORTED LEAD | Path, time, tail latency, timeout/retry, final outcomes, and trace evidence align. |
| Database slowdown | NOT SUPPORTED BY CURRENT EVIDENCE | Relevant query behavior is stable; the slow category is unrelated. |

The best-supported **leading engineering hypothesis** is degradation in the identity integration path affecting mobile verification. It is a direction for investigation, not a proven statement that the fictional provider alone caused each abandonment. More than one interpretation remains defensible: client timeout handling or a Harbor/provider interaction could produce the same observational pattern.

## Recommendation and measurement

Reproduce mobile verification against a controlled provider stub; inspect client/server timeout budgets, retry policy, idempotency, provider response timing, and the 4.8.0 diff. Preserve correlation and record logical final outcome distinctly from attempts. Consider a safely controlled timeout/handling rollout rather than replacing a provider based on this fixture.

Use **mobile verification completion** as primary, **mobile account-opening completion** as member outcome, and `/verify` p95, provider timeout rate, retry-recovery rate, and final-unrecovered rate as technical measures. Guard API errors, total latency, retry volume, duplicate operations, and web completion. Compare sufficiently mature equivalent windows; a randomized controlled rollout is stronger than before/after when feasible because it better separates the change from campaign and traffic mix.

All Engineering, Product/Operations, and Executive versions must reuse the 90.7%, 75.7%, −15.0 pp, mobile, funnel, API, and operation-level facts above. The executive version should explicitly call the integration explanation “leading” and state that observational correlation is not proof.
