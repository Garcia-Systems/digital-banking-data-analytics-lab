# Digital Banking Data Analytics for Full-Stack Engineers

*An Executable Textbook Using Harbor Federal Credit Union*

This book teaches full-stack engineers to use application, database, integration, and digital-experience data to understand behavior, diagnose problems, and support engineering and product decisions. It centers on a repeatable workflow:

> **Question → Instrument → Collect → Query → Analyze → Explain → Decide → Change → Measure**

The setting—**Harbor Federal Credit Union, its members, systems, vendors, and data—is entirely fictional**. The repository contains small deterministic synthetic data only. It contains no real financial institution or member data.

## Why this book exists

A full-stack engineer already works where useful evidence originates: browser and mobile events, APIs, application logs, vendor calls, and SQL databases. Analytics turns those records into grounded answers about self-service journeys, conversion, abandonment, navigation, integrations, database behavior, and errors. That improves debugging and makes conversations with product and operations more precise.

This is not a data-science or machine-learning textbook. It begins with descriptive analytics (what happened) and diagnostic analytics (where and under what conditions). Prediction appears only to clarify the boundary with ML.

> **Analytics helps us understand what the system and digital experience are doing. Measurement helps us determine whether a change improved them. Machine learning can help predict or classify what may happen next.**

Measurement will use analytical evidence later, but this book first develops the ability to discover and explain what is happening rather than duplicating a measurable-outcomes curriculum.

## Audience

The material is for web, mobile, API, integration, and database engineers who know basic programming but do not need to become dedicated data scientists. Exercises favor visible loops, filters, sets, counts, and arithmetic over abstractions.

## Executable-textbook method

This **completed executable textbook** connects all 24 chapters to inspectable data, runnable terminal commands, reusable Python, and tests. The learner can follow this path:

> **This is an executable textbook: the reader does not merely read analytics concepts. They query, calculate, segment, trace, diagnose, compare, experiment, and communicate using deterministic synthetic digital-banking evidence.**

```text
events
↓
filter
↓
group/count
↓
calculate
↓
observation
```

Python 3.11+, SQLite in later chapters, and the standard library keep the environment lightweight. Pandas, cloud services, paid APIs, and notebooks are not required.

## Repository map

| Path | Purpose |
| --- | --- |
| `chapters/` | Complete Chapters 0–23 across Parts I–VI |
| `data/synthetic/` | Regenerable, inspectable fictional fixtures |
| `src/harbor_analytics/` | Readable reusable calculations and generation |
| `scripts/` | Direct executable entry points |
| `labs/` | Learner worksheets and artifacts |
| `sql/` | SQL introduced in later chapters |
| `tests/` | Determinism and analytics behavior checks |
| `docs/` | Architecture and cross-cutting guidance |

See the complete curriculum in [CONTENTS.md](CONTENTS.md), the fictional system map in [the architecture document](docs/HARBOR_ANALYTICS_ARCHITECTURE.md), and field definitions in the [data dictionary](docs/DATA_DICTIONARY.md).

## Curriculum

```text
Part I   — Analytics thinking
Part II  — SQL, time, segmentation, data quality
Part III — Member journeys and digital experience
Part IV  — API/vendor/database/incident analytics
Part V   — Decisions, experiments, dashboards, communication
Part VI  — Integrated digital banking investigation
```

Readers learn to define answerable questions and metrics; validate, query, segment, and trace synthetic evidence; analyze journeys and engineering telemetry; rule alternatives in or out; measure changes; and communicate without overstating observational evidence.

## Prerequisites and install

You need Git, Python 3.11 or newer, a POSIX-compatible shell for the full-book validator, and a browser to inspect the offline dashboard. Python's bundled `sqlite3` module builds and queries the teaching database; a separate SQLite CLI is optional.

From the repository root:

```bash
python3 --version  # must be 3.11 or newer
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements-dev.txt
```

Chapter 0 itself has no third-party runtime dependency. `pytest` is needed only for tests.

## Quick start: Chapter 0

Clone the repository, enter its root, complete the installation above, then read [Chapter 0](chapters/00-from-application-data-to-engineering-decisions.md). Its executable contract is:

```bash
python3 scripts/generate_synthetic_data.py
python3 scripts/chapter_00_summary.py
```

Predict first, run the command, inspect its denominators, complete the exercise, and use the navigation footer to continue. Later chapters deliberately reuse definitions introduced earlier; keep the [glossary](docs/GLOSSARY.md) and [learning map](docs/LEARNING_MAP.md) nearby.

## Build the SQLite teaching database

```bash
python3 scripts/generate_synthetic_data.py
python3 scripts/generate_engineering_telemetry.py
python3 scripts/build_analytics_db.py
```

The result, `data/generated/harbor_analytics.sqlite`, is disposable and rebuildable. CSV fixtures remain authoritative; see [data provenance](docs/DATA_PROVENANCE.md).

## Run Chapters 0–13

Regenerate the committed CSV byte-for-byte, inspect it, then calculate the summary:

```bash
python3 scripts/generate_synthetic_data.py
head -n 6 data/synthetic/digital_events.csv
python3 scripts/chapter_00_summary.py
python3 scripts/chapter_01_sources.py
python3 scripts/chapter_02_metrics.py
python3 scripts/chapter_03_questions.py
python3 scripts/build_analytics_db.py
python3 scripts/chapter_04_sql.py
python3 scripts/chapter_05_time_analysis.py
python3 scripts/chapter_06_segmentation.py
python3 scripts/generate_dirty_fixture.py
python3 scripts/chapter_07_data_quality.py
python3 scripts/chapter_08_journeys.py
python3 scripts/chapter_09_funnels.py
python3 scripts/chapter_10_abandonment.py
python3 scripts/chapter_11_mobile_desktop.py
python3 scripts/chapter_12_navigation.py
python3 scripts/chapter_13_campaigns.py
python3 scripts/part_03_investigation.py
```

## Run Part IV

```bash
python3 scripts/generate_engineering_telemetry.py
python3 scripts/build_analytics_db.py
python3 scripts/chapter_14_api_analytics.py
python3 scripts/chapter_15_vendor_analytics.py
python3 scripts/trace_application.py app-0111
python3 scripts/chapter_16_database_analytics.py
python3 scripts/chapter_17_error_incident_analytics.py
python3 scripts/part_04_investigation.py
```

Four separate API, integration-attempt, query, and error sources preserve their grains. Correlation IDs bridge observed metadata without sensitive payloads; they neither promise perfect tracing nor prove cause.

Read [Chapter 0](chapters/00-from-application-data-to-engineering-decisions.md), then continue through the linked Chapters 1–13 in [CONTENTS.md](CONTENTS.md). The [data dictionary](docs/DATA_DICTIONARY.md) defines every field. Calculations live in `src/harbor_analytics/analysis.py`; no analytics framework conceals them.

## Run Part V

```bash
python3 scripts/generate_decision_data.py
python3 scripts/chapter_18_before_after.py
python3 scripts/chapter_19_cohorts.py
python3 scripts/chapter_20_experiment.py
python3 scripts/build_dashboard.py       # writes dist/dashboard.html
python3 scripts/chapter_22_communication.py
python3 scripts/part_05_decision_review.py
```

Part V moves from observation through declared baselines, comparable cohorts, controlled synthetic assignment, guardrails, audience-specific dashboards, and evidence-bounded communication. Analytics presents decision options; it does not silently make a product decision.

## Test and validate

```bash
python3 -m pytest
python3 -m compileall -q src scripts tests
./scripts/validate-labs.sh
python3 scripts/validate_structure.py
```

The tests verify fixture reproducibility, sources, reusable calculations, question readiness, segmentation, and safe empty-input behavior. None depends on the current date.

## Final capstone

Start with the deliberately ambiguous request—without revealing its answer:

```bash
python3 scripts/generate_capstone_data.py
python3 scripts/run_capstone.py
python3 scripts/run_capstone.py --analysis overview
```

[Chapter 23](chapters/23-the-harbor-federal-digital-experience-investigation.md) integrates journey, campaign, API, fictional-provider, database, release, error, and cross-layer trace evidence. Its [review](docs/CAPSTONE_REVIEW.md) is separate so the investigation remains genuine. Build the offline, dependency-free Chapter 21 dashboard with `python3 scripts/build_dashboard.py`; it writes `dist/dashboard.html` without network assets.

## Completed learning path

The six parts progress from analytical thinking, through SQL and journey analysis, to engineering signals, decision-making, and the integrated final investigation. Chapters 0–3 establish sources, metrics, and question framing; 4–7 add SQL, time, segmentation, and trust; 8–13 cover member journeys; 14–17 cross the application stack; 18–22 turn evidence into decisions; and Chapter 23 integrates the entire loop.

## Privacy and scope

Analytics collection should be purpose-limited: retain only fields needed to answer an explicit question. This fixture uses synthetic session and member identifiers and excludes names, contact details, government identifiers, account numbers, credentials, tokens, and financial facts. Operational systems may require sensitive data to deliver service; that does **not** imply those fields belong in an analytics dataset. See [Privacy-conscious analytics](docs/PRIVACY.md).
