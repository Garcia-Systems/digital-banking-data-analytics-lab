#!/usr/bin/env python3
"""Fast, standard-library structure and local Markdown-link validator."""
from pathlib import Path
import re, sys
ROOT=Path(__file__).resolve().parents[1]
errors=[]
chapters=sorted((ROOT/'chapters').glob('[0-9][0-9]-*.md'))
numbers=[int(p.name[:2]) for p in chapters]
if numbers != list(range(24)): errors.append(f'chapter numbers: {numbers}')
contents=(ROOT/'CONTENTS.md').read_text()
for part in ('Part I','Part II','Part III','Part IV','Part V','Part VI'):
    if part not in contents: errors.append(f'CONTENTS missing {part}')
for p in chapters:
    if f'chapters/{p.name}' not in contents: errors.append(f'CONTENTS missing {p.name}')
required=['README.md','CONTENTS.md','docs/CAPSTONE_REVIEW.md','sql/07_capstone_investigation.sql',
          'scripts/run_capstone.py','scripts/capstone_trace.py','scripts/generate_capstone_data.py']
required += [f'data/synthetic/{n}.csv' for n in ('capstone_journey_events','capstone_api_requests','capstone_vendor_calls','capstone_database_observations','capstone_errors','capstone_navigation','capstone_releases')]
for item in required:
    if not (ROOT/item).exists(): errors.append(f'missing {item}')
for md in [ROOT/'README.md',ROOT/'CONTENTS.md',*chapters,*((ROOT/'docs').glob('*.md'))]:
    text=md.read_text()
    for target in re.findall(r'\[[^]]*\]\(([^)#]+)(?:#[^)]*)?\)',text):
        if '://' not in target and not (md.parent/target).resolve().exists(): errors.append(f'broken link {md.relative_to(ROOT)} -> {target}')
if errors:
    print('\n'.join(errors)); sys.exit(1)
print('Structure valid: 24 chapters, Parts I–VI in contents, required capstone assets, and local Markdown links.')
