#!/usr/bin/env bash
# Run one authoritative executable laboratory for every chapter, in book order.
set -euo pipefail
cd "$(dirname "$0")/.."

run_chapter() {
  local number="$1"
  shift
  if ! "$@" >/dev/null; then
    printf 'Chapter %02d — FAIL: %q' "$number" "$1" >&2
    printf ' %q' "${@:2}" >&2
    printf '\n' >&2
    exit 1
  fi
  printf 'Chapter %02d — PASS\n' "$number"
}

# Deterministic prerequisite artifacts are regenerated at the point where the
# curriculum introduces them. A failed generator therefore names that chapter.
python3 scripts/generate_synthetic_data.py >/dev/null
run_chapter 0 python3 scripts/chapter_00_summary.py
run_chapter 1 python3 scripts/chapter_01_sources.py
run_chapter 2 python3 scripts/chapter_02_metrics.py
run_chapter 3 python3 scripts/chapter_03_questions.py
python3 scripts/build_analytics_db.py >/dev/null
run_chapter 4 python3 scripts/chapter_04_sql.py
run_chapter 5 python3 scripts/chapter_05_time_analysis.py
run_chapter 6 python3 scripts/chapter_06_segmentation.py
python3 scripts/generate_dirty_fixture.py >/dev/null
run_chapter 7 python3 scripts/chapter_07_data_quality.py
run_chapter 8 python3 scripts/chapter_08_journeys.py
run_chapter 9 python3 scripts/chapter_09_funnels.py
run_chapter 10 python3 scripts/chapter_10_abandonment.py
run_chapter 11 python3 scripts/chapter_11_mobile_desktop.py
run_chapter 12 python3 scripts/chapter_12_navigation.py
run_chapter 13 python3 scripts/chapter_13_campaigns.py
python3 scripts/generate_engineering_telemetry.py >/dev/null
python3 scripts/build_analytics_db.py >/dev/null
run_chapter 14 python3 scripts/chapter_14_api_analytics.py
run_chapter 15 python3 scripts/chapter_15_vendor_analytics.py
run_chapter 16 python3 scripts/chapter_16_database_analytics.py
run_chapter 17 python3 scripts/chapter_17_error_incident_analytics.py
run_chapter 18 python3 scripts/chapter_18_before_after.py
run_chapter 19 python3 scripts/chapter_19_cohorts.py
python3 scripts/generate_decision_data.py >/dev/null
run_chapter 20 python3 scripts/chapter_20_experiment.py
run_chapter 21 python3 scripts/build_dashboard.py
run_chapter 22 python3 scripts/chapter_22_communication.py
python3 scripts/generate_capstone_data.py >/dev/null
run_chapter 23 python3 scripts/run_capstone.py --analysis overview

printf '\n24 / 24 chapter laboratories passed.\n'
