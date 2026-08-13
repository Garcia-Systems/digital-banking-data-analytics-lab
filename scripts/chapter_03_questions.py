#!/usr/bin/env python3
"""Classify Harbor questions before deciding whether evidence supports them."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from harbor_analytics.analysis import load_events  # noqa: E402
from harbor_analytics.questions import HARBOR_QUESTIONS, assess_evidence  # noqa: E402

events = load_events(ROOT / "data/synthetic/digital_events.csv")
for question in HARBOR_QUESTIONS:
    readiness = assess_evidence(question, events)
    print(f"Question: {question.name}\nType: {question.question_type}")
    print("Status: answerable from current dataset" if readiness.answerable else "Status: not answerable from current dataset")
    missing = (*readiness.missing_fields, *readiness.missing_evidence)
    if missing:
        print("Missing evidence:")
        for item in missing:
            print(f"- {item}")
    print()
print("The ability to calculate a number is not the same as having evidence for a conclusion.")
