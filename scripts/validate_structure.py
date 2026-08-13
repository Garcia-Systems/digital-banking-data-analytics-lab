#!/usr/bin/env python3
"""Validate durable book structure without coupling checks to prose wording."""
from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
errors: list[str] = []
chapters = sorted((ROOT / "chapters").glob("[0-9][0-9]-*.md"))
numbers = [int(path.name[:2]) for path in chapters]

if len(chapters) != 24 or numbers != list(range(24)):
    errors.append(f"expected exactly Chapters 00–23; found {numbers}")

contents = (ROOT / "CONTENTS.md").read_text(encoding="utf-8")
parts = ["Part I", "Part II", "Part III", "Part IV", "Part V", "Part VI"]
positions = [contents.find(f"## {part}") for part in parts]
if any(position < 0 for position in positions) or positions != sorted(positions):
    errors.append("CONTENTS must contain Parts I–VI in order")

content_chapters = re.findall(r"^\d+\. \[[^]]+\]\(chapters/(\d\d-[^)]+\.md)\)", contents, re.M)
if content_chapters != [path.name for path in chapters]:
    errors.append("CONTENTS chapter links are missing or out of order")

for number, path in enumerate(chapters):
    chapter_text = path.read_text(encoding="utf-8")
    for heading in ("## Chapter contract", "## Exercise", "## Navigation"):
        if heading not in chapter_text:
            errors.append(f"{path.name} missing {heading}")
    if "[Contents](../CONTENTS.md)" not in chapter_text:
        errors.append(f"{path.name} missing Contents navigation")
    if number > 0 and f"[← Chapter {number - 1}]({chapters[number - 1].name})" not in chapter_text:
        errors.append(f"{path.name} missing previous navigation")
    if number < 23 and f"[Chapter {number + 1} →]({chapters[number + 1].name})" not in chapter_text:
        errors.append(f"{path.name} missing next navigation")
    if number == 0 and "[← Chapter" in chapter_text:
        errors.append("Chapter 0 must not link to a previous chapter")
    if number == 23 and "Chapter 24" in chapter_text:
        errors.append("Chapter 23 must not reference Chapter 24")

required = [
    "README.md", "CONTENTS.md", "docs/GLOSSARY.md", "docs/DATA_PROVENANCE.md",
    "docs/LEARNING_MAP.md", "docs/FULL_STACK_ENGINEER_SKILLS_MAP.md",
    "docs/COMPLETION_CHECKLIST.md", "docs/CAPSTONE_REVIEW.md",
    "scripts/generate_synthetic_data.py", "scripts/generate_dirty_fixture.py",
    "scripts/generate_engineering_telemetry.py", "scripts/generate_decision_data.py",
    "scripts/generate_capstone_data.py", "scripts/build_dashboard.py",
    "scripts/validate-labs.sh", "sql/07_capstone_investigation.sql",
]
required.extend(
    f"data/synthetic/{name}.csv"
    for name in (
        "digital_events", "digital_events_dirty", "api_requests", "integration_calls",
        "database_queries", "error_events", "verification_guidance_experiment",
        "capstone_journey_events", "capstone_api_requests", "capstone_vendor_calls",
        "capstone_database_observations", "capstone_errors", "capstone_navigation",
        "capstone_releases",
    )
)
for item in required:
    if not (ROOT / item).is_file():
        errors.append(f"missing required asset: {item}")

markdown_files = [ROOT / "README.md", ROOT / "CONTENTS.md", *chapters, *(ROOT / "docs").glob("*.md")]
for markdown in markdown_files:
    text = markdown.read_text(encoding="utf-8")
    for target in re.findall(r"\[[^]]*\]\(([^)#]+)(?:#[^)]*)?\)", text):
        if "://" not in target and not (markdown.parent / target).resolve().exists():
            errors.append(f"broken link: {markdown.relative_to(ROOT)} -> {target}")
    # Validate local script and SQL paths presented in inline code or code blocks.
    for target in set(re.findall(r"\b((?:scripts|sql)/[A-Za-z0-9_.-]+(?:\.py|\.sh|\.sql))\b", text)):
        if not (ROOT / target).is_file():
            errors.append(f"missing referenced file: {markdown.relative_to(ROOT)} -> {target}")

if errors:
    print("\n".join(errors))
    sys.exit(1)
print(
    "Structure valid: exactly 24 chapters (00–23), Parts I–VI and contents order, "
    "chapter contracts/navigation, required data/generators/docs, referenced scripts/SQL, "
    "and local Markdown links."
)
