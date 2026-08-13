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

Each implemented chapter connects prose to inspectable data, runnable terminal commands, reusable Python, and tests. The learner can follow this path:

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
| `chapters/` | Textbook prose; Chapters 0–7 are complete |
| `data/synthetic/` | Regenerable, inspectable fictional fixtures |
| `src/harbor_analytics/` | Readable reusable calculations and generation |
| `scripts/` | Direct executable entry points |
| `labs/` | Learner worksheets and artifacts |
| `sql/` | SQL introduced in later chapters |
| `tests/` | Determinism and analytics behavior checks |
| `docs/` | Architecture and cross-cutting guidance |

See the full 24-chapter plan in [CONTENTS.md](CONTENTS.md) and the fictional system map in [the architecture document](docs/HARBOR_ANALYTICS_ARCHITECTURE.md).

## Install

From the repository root:

```bash
python3 --version  # must be 3.11 or newer
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements-dev.txt
```

Chapter 0 itself has no third-party runtime dependency. `pytest` is needed only for tests.

## Run Chapters 0–7

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
```

Read [Chapter 0](chapters/00-from-application-data-to-engineering-decisions.md), then continue through the linked Chapters 1–7 in [CONTENTS.md](CONTENTS.md). The [data dictionary](docs/DATA_DICTIONARY.md) defines every field. Calculations live in `src/harbor_analytics/analysis.py`; no analytics framework conceals them.

## Test and validate

```bash
python3 -m pytest
python3 -m compileall -q src scripts tests
```

The tests verify fixture reproducibility, sources, reusable calculations, question readiness, segmentation, and safe empty-input behavior. None depends on the current date.

## Roadmap

The six parts progress from analytical thinking, through SQL and journey analysis, to engineering signals, decision-making, and a final investigation. Chapters 0–3 establish sources, metrics, and question framing. Chapters 4–7 add SQL, time, segmentation, and analytical trust. Chapters 8–23 remain a roadmap in [CONTENTS.md](CONTENTS.md); Part III journey modeling, funnels, abandonment, experience, navigation, and campaign analysis is intentionally deferred.

## Privacy and scope

Analytics collection should be purpose-limited: retain only fields needed to answer an explicit question. This fixture uses synthetic session and member identifiers and excludes names, contact details, government identifiers, account numbers, credentials, tokens, and financial facts. Operational systems may require sensitive data to deliver service; that does **not** imply those fields belong in an analytics dataset. See [Privacy-conscious analytics](docs/PRIVACY.md).
