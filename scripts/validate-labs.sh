#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/generate_synthetic_data.py >/dev/null
python3 scripts/generate_engineering_telemetry.py >/dev/null
python3 scripts/generate_decision_data.py >/dev/null
python3 scripts/generate_capstone_data.py >/dev/null
python3 scripts/build_analytics_db.py >/dev/null
for n in 00_summary 01_sources 02_metrics 03_questions 04_sql 05_time_analysis 06_segmentation 07_data_quality 08_journeys 09_funnels 10_abandonment 11_mobile_desktop 12_navigation 13_campaigns 14_api_analytics 15_vendor_analytics 16_database_analytics 17_error_incident_analytics 18_before_after 19_cohorts 20_experiment 22_communication; do
  python3 "scripts/chapter_${n}.py" >/dev/null
done
python3 scripts/build_dashboard.py >/dev/null
python3 scripts/run_capstone.py --analysis overview >/dev/null
python3 scripts/capstone_trace.py cap-app-0001 >/dev/null
python3 scripts/validate_structure.py
echo "All practical chapter labs and the Chapter 23 smoke investigation passed. Chapter 21 is exercised by build_dashboard.py."
