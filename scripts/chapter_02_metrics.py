#!/usr/bin/env python3
"""Calculate carefully labelled event counts, dimensions, metrics, and candidates."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from harbor_analytics.analysis import average_duration, count_events, filter_events, load_events, rate  # noqa: E402

events = load_events(ROOT / "data/synthetic/digital_events.csv")
starts = filter_events(events, "application_started")
completions = filter_events(events, "application_completed")
print(f"[event count] application starts: {len(starts)}")
print(f"[event count] application completions: {len(completions)}")
print(f"[KPI candidate] observed application completion: {len(completions)} completion events / {len(starts)} start events = {rate(len(completions), len(starts)):.1f}%")
for channel in ("mobile", "web"):
    channel_starts = filter_events(starts, channel=channel)
    channel_completions = filter_events(completions, channel=channel)
    print(f"[dimension breakdown] {channel} completion: {len(channel_completions)} completion events / {len(channel_starts)} start events = {rate(len(channel_completions), len(channel_starts)):.1f}%")
identity_starts = count_events(events, "identity_verification_started")
identity_success = count_events(events, "identity_verification_completed")
print(f"[KPI candidate] identity-verification success: {identity_success} success events / {identity_starts} start events = {rate(identity_success, identity_starts):.1f}%")
print(f"[metric] average recorded application-completion event duration: {average_duration(completions):.1f} ms")
print("Interpretation: these are calculated observations; differences suggest investigation, not a cause.")
