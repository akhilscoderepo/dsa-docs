#!/usr/bin/env python3
"""Split a monolithic chapter spec into a chapter map plus one small file per lesson blueprint.

Usage: split_spec.py SPEC.md OUTDIR
Writes OUTDIR/chapter-map.md (purpose, entry contract, ordered lesson index, exit check, practice contract,
combination preview) and OUTDIR/NN-lesson-slug.md for each `### ` blueprint. A writing run loads the map and ONE slice,
not the whole spec, which keeps the per-lesson prompt small.
"""
import re, sys
from pathlib import Path

spec, out = Path(sys.argv[1]), Path(sys.argv[2])
text = spec.read_text(encoding="utf-8")
out.mkdir(parents=True, exist_ok=True)
for old in out.glob("[0-9][0-9]-*.md"):
    old.unlink()   # slices are generated; stale numbering must not linger
m = re.search(r"(?ms)^## Lesson Blueprints\s*\n(.*?)(?=^## |\Z)", text)
if not m:
    sys.exit("no '## Lesson Blueprints' section")
body = m.group(1)
slug = lambda s: re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
parts = re.findall(r"(?ms)^### (.+?)\n(.*?)(?=^### |\Z)", body)
intro = body.split("### ", 1)[0].strip()
rest = text.replace(m.group(0), "")
rest = re.sub(r"(?ms)<!-- BEGIN VERIFIED-CANDIDATE-BANK -->.*?<!-- END VERIFIED-CANDIDATE-BANK -->", "", rest)
index = []
n = 0
for h, blk in parts:
    if h.strip().lower().startswith("deferred"):
        continue
    n += 1
    name = f"{n:02d}-{slug(h)}.md"
    (out / name).write_text(f"# Lesson spec: {h.strip()}\n\n{blk.strip()}\n", encoding="utf-8")
    index.append(f"{n:02d}. {h.strip()}  ->  {name}")
(out / "chapter-map.md").write_text(
    "# Chapter map (generated; do not edit, edit the source spec)\n\n" + intro + "\n\n## Lesson order\n\n" + "\n".join(index) + "\n\n" + rest.strip() + "\n",
    encoding="utf-8")
print(f"{out}: map + {n} lesson slices")
