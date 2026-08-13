# Synthetic digital-event data dictionary

One CSV row is one fictional recorded event. All identifiers and values are deterministic and synthetic. Empty values are not currently generated.

| Field | Type | Definition | Example | Analytical role |
| --- | --- | --- | --- | --- |
| `event_id` | string | Unique identifier for the recorded event. | `evt-0001` | Identifier |
| `timestamp` | ISO-8601 UTC string | Fixed time at which the event was recorded. | `2025-01-13T14:00:00Z` | Metric input / time dimension |
| `session_id` | string | Synthetic identifier linking events in one digital visit. | `session-001` | Identifier / metric input |
| `anonymous_or_synthetic_member_id` | string | Non-real identifier for the synthetic member represented by a session. | `synthetic-member-001` | Identifier / dimension |
| `channel` | string | Digital interaction channel: `web` or `mobile`. | `web` | Dimension |
| `device_type` | string | Coarse fictional client form: `desktop` or `phone`. | `desktop` | Dimension |
| `event_name` | string | Stable name of the recorded occurrence. | `application_started` | Dimension / metric input |
| `page_or_feature` | string | Feature context in which the event occurred. | `account_opening` | Dimension |
| `outcome` | string | Recorded event outcome: `success` or `failure`. Absence of an event is not itself an outcome. | `success` | Dimension / metric input |
| `duration_ms` | integer | Processing duration attached to this single event, in milliseconds; not journey duration. | `900` | Metric input |
| `source_system` | string | Layer that emitted the observation. Stable values are `member_web`, `mobile_app`, `harbor_api`, `account_opening`, `identity_provider`, and `transfer_service`. | `account_opening` | Dimension / provenance |

The fixture deliberately excludes names, real member IDs, account numbers, balances, credentials, identity documents, IP addresses, and vendor payloads. `source_system` describes provenance, not causality.
