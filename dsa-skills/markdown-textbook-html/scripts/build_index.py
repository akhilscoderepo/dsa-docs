#!/usr/bin/env python3
"""Generate a curriculum index page that links to the per-chapter HTML files in one folder.
Usage: build_index.py MANUSCRIPTS_ROOT OUTPUT_DIR [--title T]
Chapter titles come from each chapter's built HTML <title>; counts come from the manuscripts."""
import argparse, html, re
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("manuscripts"); ap.add_argument("outdir"); ap.add_argument("--title", default="DSA curriculum")
a = ap.parse_args()
root, out = Path(a.manuscripts), Path(a.outdir)
rows = []
for d in sorted(p for p in root.iterdir() if p.is_dir() and re.match(r"\d\d-", p.name)):
    page = out / f"{d.name}.html"
    if not page.exists():
        continue
    lessons = sum(1 for f in d.glob("*.md") if "lesson-kind:" in f.read_text(encoding="utf-8"))
    ex = sum(len(re.findall(r"(?m)^#### \[", f.read_text(encoding="utf-8"))) for f in d.glob("*.md") if "lesson-kind:" in f.read_text(encoding="utf-8"))
    m = re.search(r"<title>(.*?)</title>", page.read_text(encoding="utf-8"), re.S)
    rows.append((d.name[:2], html.unescape(m.group(1)).strip() if m else d.name, page.name, lessons, ex, page.stat().st_size // 1024))
cards = "\n".join(
    f'<a class="card" href="{html.escape(n)}"><span class="num">{num}</span><span class="t">{html.escape(t)}</span>'
    f'<span class="m">{l} lessons, {e} exercises, {k} KB</span></a>' for num, t, n, l, e, k in rows)
open(out / "index.html", "w", encoding="utf-8").write(f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(a.title)}</title>
<style>
:root{{--bg:#fbfaf7;--fg:#1f2328;--mut:#5b6470;--card:#fff;--line:#d9d6cf;--acc:#2457c5}}
@media (prefers-color-scheme:dark){{:root{{--bg:#16181c;--fg:#e8e6e1;--mut:#9aa3ae;--card:#1e2126;--line:#33383f;--acc:#7da2ff}}}}
body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 system-ui,sans-serif}}
main{{max-width:44rem;margin:0 auto;padding:2rem 16px}}
h1{{font-size:1.6rem;margin:0 0 .25rem}} p{{color:var(--mut);margin:.25rem 0 1.5rem}}
.card{{display:grid;grid-template-columns:3rem 1fr;gap:0 .75rem;padding:.9rem 1rem;margin:.6rem 0;background:var(--card);border:1px solid var(--line);border-radius:10px;text-decoration:none;color:inherit;min-height:44px}}
.card:hover{{border-color:var(--acc)}} .num{{grid-row:span 2;font-size:1.5rem;font-weight:700;color:var(--acc)}}
.t{{font-weight:600}} .m{{color:var(--mut);font-size:.9rem}}
</style></head><body><main><h1>{html.escape(a.title)}</h1>
<p>One self-contained file per chapter. Notes and progress are saved per chapter in this browser. Content complete, human review pending.</p>
{cards}
</main></body></html>""")
print("wrote", out / "index.html", len(rows), "chapters")
