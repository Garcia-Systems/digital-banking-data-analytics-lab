# Glossary

These definitions are canonical across the Harbor Federal textbook. All institutions, systems, people, identifiers, and observations are fictional and synthetic.

| Term | Definition and analytical grain |
| --- | --- |
| **Event** | One recorded occurrence or state transition. An event row is not automatically a session, application, request, or person. |
| **Metric** | A numeric measurement calculated under a stated population, unit, window, numerator, and—when applicable—denominator. |
| **Dimension** | A field used to group or compare a metric, such as channel or device type. |
| **KPI** | A metric deliberately selected to track an important objective, with an owner, definition, target, and review cadence. |
| **Analytical unit** | The entity counted or compared: for example, an event, session, application, API request, integration operation, or provider call. |
| **Session** | A synthetic grouping of related digital-experience events. It may contain no application or one application in these fixtures; it is not a person. |
| **Application** | One synthetic account-opening attempt, identified by `application_id`; it is the funnel's analytical unit. |
| **Journey** | An ordered interpretation of observations belonging to an analytical unit. Missing observations do not reveal intent. |
| **Funnel** | Counts of eligible journeys reaching successive, predefined stages. |
| **Stage conversion** | Distinct applications reaching the current stage divided by distinct applications reaching the immediately preceding stage. |
| **Overall conversion** | Distinct applications reaching the final stage divided by distinct applications reaching the first stage. |
| **Abandonment** | In this book, an eligible application with no later expected stage observed by the declared horizon. It does not establish intent or failure. |
| **Friction signal** | Recorded evidence worth investigating, such as a retry, error, long interval, or no-result search; it is not itself a cause. |
| **Baseline** | A declared earlier reference population and observation window. |
| **Comparison period** | A declared later population and window evaluated against a baseline. It is not automatically an experiment. |
| **Cohort** | A group sharing a defined starting characteristic and observation horizon. |
| **Experiment** | A planned comparison in which eligible analytical units are assigned to controlled conditions. |
| **Variant** | One assigned experiment condition; assignment counts form the completion-rate denominator. |
| **API request** | One observed inbound request to a Harbor endpoint. Retries are separate requests. |
| **Integration operation** | One logical task Harbor asks an external provider to perform; it may contain multiple provider calls. |
| **Provider call** | One attempt sent to the fictional provider. Call-level and operation-level reliability have different denominators. |
| **Retry** | A subsequent attempt for the same logical operation. A failed call followed by success is a recovered operation. |
| **Correlation ID** | A synthetic metadata key used to connect observations across layers. It is neither a credential nor proof of causation or trace completeness. |
| **Latency** | Elapsed time for the explicitly named request, call, query, stage, or journey, expressed in milliseconds unless stated otherwise. |
| **p95** | The nearest-rank 95th-percentile latency: at least 95% of recorded values are at or below it. Always name the measured unit. |
| **Error** | One structured record of an undesired technical outcome. Errors may be recovered and need not be member-visible. |
| **Incident** | A bounded service event requiring coordinated attention; not every error or recurring pattern is an incident. |
| **Observation** | A value or condition directly recorded in the selected evidence. |
| **Calculated** | Arithmetic derived from observations under explicit definitions. |
| **Interpretation** | Evidence-bounded meaning assigned to observations; reasonable interpretations may differ. |
| **Association** | Variables or conditions occur together; this alone does not establish cause. |
| **Hypothesis** | A testable candidate explanation requiring additional evidence. |
| **Causal claim** | A claim that a condition produced an outcome; it requires a design or evidence stronger than observational co-occurrence. |
| **Guardrail metric** | A secondary measure checked to detect unacceptable harm while evaluating a primary outcome. |

For rate changes, **percentage-point change** subtracts two percentages; **relative change** divides that difference by the baseline. Always label which is reported.
