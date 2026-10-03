#!/usr/bin/env python3
"""Audit built HTML chapters.

Usage: audit_html.py CHAPTER.html [more.html ...] [--manuscripts DIR] [--smoke]

Checks: single self-contained file (no external scripts, styles, images, fonts or @imports), viewport meta,
unique ids, JS syntax (needs node), one notes box + status selector + solution block per exercise, a chapter
notes box, trace/quiz JSON validity, and, with --manuscripts, exercise-count parity with the Markdown source.
--smoke also runs smoke_html.mjs (needs node and jsdom). Exit 1 on any ERROR.
"""
import argparse, html, json, re, shutil, subprocess, sys, tempfile
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "markdown-textbook-html" / "scripts"))
from html.parser import HTMLParser
from build_html import VisibleText


class _Plain(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True); self.out = []
    def handle_data(self, d): self.out.append(d)



def md_exercise_count(ch):
    n = 0
    for f in ch.glob("*.md"):
        t = f.read_text(encoding="utf-8")
        if "lesson-kind:" in t:
            n += len(re.findall(r"(?m)^####\s+\[(?:Build|Vary|Boundary|Recognize|Extend|Medium|Hard|Challenge)\]", t))
    return n


def audit(path, manuscripts, smoke, stamp_path=None):
    t = Path(path).read_text(encoding="utf-8")
    errs, warns = [], []
    e, w = errs.append, warns.append
    # external resources
    for m in re.finditer(r'<(?:script|img|iframe|source|video|audio|embed)\b[^>]*\bsrc\s*=\s*["\']([^"\']+)', t, re.I):
        e(f"external or file resource via src: {m.group(1)[:80]}")
    for m in re.finditer(r'<link\b[^>]*\bhref\s*=\s*["\']([^"\']+)', t, re.I):
        e(f"linked resource: {m.group(1)[:80]}")
    if re.search(r"@import|url\(\s*['\"]?(?:https?:)?//", t):
        e("CSS @import or remote url() found")
    if '<meta name="viewport"' not in t:
        e("missing viewport meta tag (breaks mobile layout)")
    if "<title>" not in t:
        e("missing <title>")
    ids = re.findall(r'\sid="([^"]+)"', t)
    dup = [k for k, c in Counter(ids).items() if c > 1]
    if dup:
        e(f"duplicate ids: {dup[:5]}")
    # per-exercise controls
    ex = re.findall(r'<article class="exercise" data-id="([^"]+)"', t)
    if not ex:
        e("no exercise cards found")
    if len(set(ex)) != len(ex):
        e("duplicate exercise ids (notes would collide)")
    for label, pat in (("notes box", r'<textarea id="n-[^"]+" class="note"'), ("status selector", r'<select class="status-sel"'),
                       ("solution block", r'<details class="solution"')):
        n = len(re.findall(pat, t))
        if n != len(ex):
            e(f"{n} {label} elements for {len(ex)} exercises")
    if "No solution recorded yet" in t:
        e(f"{t.count('No solution recorded yet')} exercise(s) have no solution")
    if 'id="chapter-notes"' not in t:
        e("missing chapter notes box")
    for kind in ("trace", "quiz"):
        for m in re.finditer(rf'<div class="{kind}" data-{kind}="([^"]*)"', t):
            try:
                json.loads(html.unescape(m.group(1)))
            except Exception as x:
                e(f"invalid {kind} JSON: {x}")
    key = re.search(r'data-chapter-key="([^"]*)"', t)
    if not key or not re.fullmatch(r"dsa:chapter-\d+", key.group(1)):
        e("data-chapter-key must be dsa:chapter-NN so saved notes survive a retitle")
    unvalidated = "Java examples in this file were not machine-validated" in t
    if unvalidated:
        w("footer says Java was not machine-validated")
        if 'class="badge"' in t:
            e("'verified' badges are present but the footer says Java was not validated")
    elif not re.search(r"Java: \d+ of \d+ blocks compiled on JDK", t):
        e("footer has no Java validation line")
    if stamp_path:
        st = json.loads(Path(stamp_path).read_text(encoding="utf-8"))
        j = st.get("jdk") or {}
        if st.get("status") == "validated" and f"JDK {j.get('version')}" not in t:
            e("footer JDK version does not match the validation stamp")
        if st.get("release_effective") not in (None, "default") and f"--release {st['release_effective']}" not in t:
            e("footer does not state the --release level recorded in the stamp")
        if manuscripts:
            sys.path.insert(0, str(HERE))
            import compile_java
            if st.get("digest") != compile_java.digest_for_dir(manuscripts):
                e("validation stamp digest does not match the manuscripts (stale validation)")
    if len(t) > 3_000_000:
        w(f"file is {len(t) // 1024} KB; consider splitting the chapter")
    # search must not reveal hints, solutions or notes
    sm = re.search(r'<script type="application/json" id="search-index">(.*?)</script>', t, re.S)
    if not sm:
        e("no build-time search index (search would read hidden text)")
    else:
        try:
            idx = json.loads(sm.group(1).replace("<\\/", "</"))
            norm = lambda s: re.findall(r"[a-z0-9]+", s.lower())
            grams = lambda ws: {" ".join(ws[i:i + 8]) for i in range(len(ws) - 7)}
            vis = VisibleText(); vis.feed(re.sub(r'<script type="application/json".*?</script>', "", t, flags=re.S))
            visible = grams(norm(" ".join(vis.out)))
            hidden = set()
            for m in re.finditer(r'<details class="(?:hint|solution)"[^>]*>(.*?)</details>', t, re.S):
                hp = _Plain(); hp.feed(m.group(1)); hidden |= grams(norm(" ".join(hp.out)))
            hidden -= visible
            leaked = [d["id"] for d in idx if grams(norm(d["text"])) & hidden]
            if leaked:
                e(f"search index leaks hint/solution text in: {leaked[:5]}")
            if not idx:
                e("search index is empty")
        except Exception as x:
            e(f"search index unreadable: {x}")
    # js syntax
    scripts = re.findall(r"<script>(.*?)</script>", t, re.S)
    if shutil.which("node") and scripts:
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as fh:
            fh.write("\n".join(scripts))
        r = subprocess.run(["node", "--check", fh.name], capture_output=True, text=True)
        if r.returncode:
            e("JS syntax error: " + r.stderr.strip().splitlines()[0])
    elif not shutil.which("node"):
        w("node not found: JS syntax not checked")
    # manuscript parity
    if manuscripts:
        n = md_exercise_count(Path(manuscripts))
        if n != len(ex):
            e(f"manuscript has {n} exercises but the HTML has {len(ex)}")
    if smoke:
        r = subprocess.run(["node", str(HERE / "smoke_html.mjs"), str(path)], capture_output=True, text=True)
        if r.returncode == 2:
            w("smoke test skipped: jsdom not installed")
        elif r.returncode:
            e("smoke test failed:\n" + "\n".join(l for l in r.stdout.splitlines() if l.startswith("FAIL")))
    return errs, warns, len(ex)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+"); ap.add_argument("--manuscripts"); ap.add_argument("--smoke", action="store_true"); ap.add_argument("--stamp")
    a = ap.parse_args()
    bad = 0
    for f in a.files:
        errs, warns, n = audit(f, a.manuscripts, a.smoke, a.stamp)
        print(f"{f}: {n} exercises, {len(errs)} errors, {len(warns)} warnings")
        for x in errs: print("  ERROR", x)
        for x in warns: print("  WARN ", x)
        bad += bool(errs)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
