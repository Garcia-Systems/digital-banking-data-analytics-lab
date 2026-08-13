# Harbor synthetic analytics data dictionary

Both fixtures are fictional. `data/synthetic/digital_events.csv` is the canonical, deterministically generated clean fixture; `digital_events_dirty.csv` is a reproducible teaching derivative and must not replace it.

| Field | Meaning / valid values |
|---|---|
| `event_id` | Unique synthetic event key (`evt-...`) |
| `timestamp` | ISO-8601 UTC timestamp ending `Z`; day/hour are derived in UTC |
| `session_id` | Synthetic journey/session key |
| `anonymous_or_synthetic_member_id` | Explicitly synthetic member key |
| `channel` | `web`, `mobile` |
| `device_type` | `desktop`, `phone` |
| `event_name` | Recorded action, including application and identity start/completion/failure events |
| `page_or_feature` | Fictional feature context |
| `outcome` | `success` or `failure`; absence must not be interpreted as failure |
| `duration_ms` | Nonnegative recorded milliseconds |
| `source_system` | `member_web`, `mobile_app`, `account_opening`, `identity_provider`, or `harbor_api` |

| `application_id` | Non-identifying synthetic account-opening attempt (`app-...`); blank for non-application events |
| `attempt_number` | Attempt ordinal within the synthetic application; `0` when not applicable |
| `error_category` | Coarse fictional error classification; blank means no category was recorded |
| `vendor_result` | Fictional identity observation (`verified`, `retryable_failure`, or blank) |
| `api_duration_ms` | Nonnegative fictional boundary duration; `0` means not recorded/not applicable |

The application attempt is the funnel grain. Member, session, and application are not interchangeable. Stage-to-stage rates divide by the prior-stage application count; overall completion divides completed by started applications. Observed abandonment means no later defined stage was recorded in the fixed window. Errors, retries, durations, and vendor results are friction signals, never causal findings.

The dirty derivative deliberately violates several rules. No fixture contains names, accounts, money, credentials, or real vendor/member data.

## Part III experience and arrival fields

| Field | Meaning / valid values |
|---|---|
| `traffic_source` | Normalized arrival source (`campaign`, `direct`) |
| `campaign_id` | Fictional campaign tag or blank; association is not attribution |
| `landing_page` | Normalized intended arrival page |
| `referral_category` | Coarse referral class (`owned`, `partner`, `none`) |
| `search_category` | Allowlisted intent category; arbitrary/raw query text is never retained |
| `navigation_from` | Normalized origin for a `navigation_click` |
| `navigation_to` | Normalized destination for a `navigation_click` |

`channel` is the delivery surface and `device_type` is hardware form; they are not interchangeable. A **navigation event** is a page view or explicit navigation action. A **search** is one `search_started`; a **search session** is a distinct session containing searches. A **no-result search** has a `search_no_results` observation. A **campaign** is a fictional tagged initiative. **Observed conversion** is tagged completions / tagged starts, not causal attribution.
