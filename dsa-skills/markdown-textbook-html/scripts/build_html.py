#!/usr/bin/env python3
"""Build one self-contained interactive HTML textbook chapter from a Markdown manuscript directory.

Usage:
  build_html.py CHAPTER_DIR -o OUT.html [--chapter NN] [--title "Sliding Window"] [--series "Java DSA Interview Curriculum"]
                [--validation STAMP.json]

Reads the same directory layout the audit scripts read (orientation, NN-lesson.md, solutions/NN-lesson.md,
unlocked-combinations, review). CSS and JS come from ../assets and are inlined, so the output is one file with no
external requests. Requires: pip install markdown-it-py
"""
import argparse, html, json, re, sys
from html.parser import HTMLParser
from pathlib import Path
from markdown_it import MarkdownIt

HERE = Path(__file__).resolve().parent
ASSETS = HERE.parent / "assets"
sys.path.insert(0, str(HERE.parent.parent / "dsa-curriculum-auditor" / "scripts"))
import compile_java  # shared digest so the stamp and the build can never disagree about what was validated


class VisibleText(HTMLParser):
    """Text a reader can see without opening anything: skips hints, solutions, notes controls, scripts, trace/quiz data."""
    SKIP_CLASSES = ("hint", "solution", "notes-wrap", "lesson-done", "trace", "quiz")
    SKIP_TAGS = ("script", "style", "textarea", "select", "button", "details")
    VOID = ("br", "hr", "img", "input", "meta", "link", "wbr")

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.stack, self.skip = [], [], 0

    def handle_starttag(self, tag, attrs):
        if tag in self.VOID:
            return
        cls = dict(attrs).get("class", "") or ""
        hide = tag in self.SKIP_TAGS or any(c in cls.split() for c in self.SKIP_CLASSES)
        self.stack.append(hide)
        self.skip += hide

    def handle_endtag(self, tag):
        if tag in self.VOID or not self.stack:
            return
        self.skip -= self.stack.pop()

    def handle_data(self, data):
        if not self.skip:
            self.out.append(data)


def visible_text(fragment):
    p = VisibleText()
    p.feed(fragment)
    return re.sub(r"\s+", " ", " ".join(p.out)).strip()
KW = ("abstract assert boolean break byte case catch char class continue default do double else enum extends final finally "
      "float for if implements import instanceof int interface long new package private protected public return short static "
      "super switch this throw throws try var void while record null true false").split()
TOK = re.compile(r"(//[^\n]*|/\*.*?\*/)|(\"(?:\\.|[^\"\\])*\"|'(?:\\.|[^'\\])*')|\b(" + "|".join(KW) + r")\b|\b(\d[\d_]*(?:\.\d+)?[LlFfDd]?)\b", re.S)
NORM = lambda s: re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()
SLUG = lambda s: re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-") or "x"
STATUS = [("new", "Not started"), ("attempted", "Attempted"), ("solved", "Solved"), ("revisit", "Needs review")]


def highlight(code):
    out, pos = [], 0
    for m in TOK.finditer(code):
        out.append(html.escape(code[pos:m.start()]))
        cls = "c" if m.group(1) else "s" if m.group(2) else "k" if m.group(3) else "n"
        out.append(f'<span class="{cls}">{html.escape(m.group(0))}</span>')
        pos = m.end()
    out.append(html.escape(code[pos:]))
    return "".join(out)


class Builder:
    def __init__(self, validated):
        self.validated, self.ids, self.counters = validated, {}, {"trace": 0, "quiz": 0}
        self.stem = "x"
        self.index = []
        md = MarkdownIt("commonmark", {"html": False}).enable("table")
        b = self

        def fence(self_, tokens, idx, options, env):
            t = tokens[idx]
            parts = t.info.split()
            lang, flags = (parts[0] if parts else ""), set(parts[1:])
            if lang in ("trace", "quiz"):
                try:
                    json.loads(t.content)
                except Exception as e:
                    raise SystemExit(f"{b.stem}: invalid {lang} JSON: {e}")
                b.counters[lang] += 1
                n = b.counters[lang]
                return f'<div class="{lang}" data-{lang}="{html.escape(t.content.strip(), quote=True)}" data-{"tid" if lang == "trace" else "qid"}="{lang[0]}-{b.stem}-{n}"></div>\n'
            if lang == "java":
                badge = '<span class="badge" title="Compiled and run with assertions during the build">verified</span>' if ("run" in flags and b.validated) else ""
                return f'<pre class="code" data-lang="java"><code>{highlight(t.content.rstrip(chr(10)))}</code>{badge}</pre>\n'
            return f'<pre class="code plain"><code>{html.escape(t.content.rstrip(chr(10)))}</code></pre>\n'

        def heading_open(self_, tokens, idx, options, env):
            t = tokens[idx]
            text = tokens[idx + 1].content
            base = f"{b.stem}-{SLUG(text)}"
            n = b.ids.get(base, 0); b.ids[base] = n + 1
            return f'<{t.tag} id="{base}{"" if n == 0 else "-" + str(n)}">'

        md.add_render_rule("fence", fence)
        md.add_render_rule("heading_open", heading_open)
        md.add_render_rule("table_open", lambda s, t, i, o, e: '<div class="tablewrap"><table>')
        md.add_render_rule("table_close", lambda s, t, i, o, e: "</table></div>")
        self.md = md

    def render(self, text):
        return self.md.render(re.sub(r"<!--.*?-->", "", text, flags=re.S))

    # ---- exercises ----
    def exercise(self, stem, piece, solutions):
        head, _, body = piece.partition("\n")
        im = re.match(r"\s*<!--\s*id:\s*([^\s>]+)\s*-->\s*\n?", body)
        if not im:
            raise SystemExit(f"{stem}: exercise '{head.strip()}' has no <!-- id: ... -->; run the manuscript audit first")
        ex_id = im.group(1)
        body = body[im.end():]
        m = re.match(r"\[(\w+)\]\s+(.*?)\s*$", head)
        role, title = m.group(1), m.group(2)
        src = re.search(r"\((LeetCode\s+\d+|Author exercise)\)\s*$", title)
        base = re.sub(r"\s*\((?:LeetCode\s+\d+|Author exercise)\)\s*$", "", title)
        fields = {}
        for para in re.split(r"\n\s*\n", body.strip()):
            fm = re.match(r"\*\*([^*]+?)\.\*\*", para.strip())
            if fm:
                fields[fm.group(1)] = para.strip()
        def f(label, cls=None):
            return f'<div class="f f-{SLUG(label)}">{self.md.render(fields[label])}</div>' if label in fields else ""
        sol = solutions.get(ex_id)
        sol_html = (f'<details class="solution"><summary>Show solution (attempt it first)</summary><div>{self.render(sol)}</div></details>'
                    if sol else '<p class="src">No solution recorded yet.</p>')
        hint = (f'<details class="hint"><summary>Hint</summary><div>{self.md.render(re.sub(r"^[*][*]Hint[.][*][*]\s*", "", fields["Hint"]))}</div></details>'
                if "Hint" in fields else "")
        opts = "".join(f'<option value="{v}">{l}</option>' for v, l in STATUS)
        return (f'<article class="exercise" data-id="{ex_id}"><header><span class="role role-{SLUG(role)}">{html.escape(role)}</span>'
                f'<h4>{html.escape(base)}</h4><span class="src">{html.escape(src.group(1)) if src else ""}</span>'
                f'<select class="status-sel" data-id="{ex_id}" aria-label="Status for {html.escape(base)}">{opts}</select></header>'
                f'<div class="body">{f("Problem")}{f("Constraints")}{f("Example 1")}{f("Example 2")}{f("Prerequisites")}{f("Changed decision")}{hint}</div>'
                f'<div class="notes-wrap"><label for="n-{ex_id}">My solution notes <span class="saved"></span></label>'
                f'<textarea id="n-{ex_id}" class="note" data-id="{ex_id}" placeholder="Your approach, the invariant, bugs you hit, and what to revisit."></textarea>'
                f'<div class="row"><button type="button" class="clear-note" data-id="{ex_id}">Clear</button></div>{sol_html}</div></article>')

    def lesson(self, f, text, solutions_dir):
        self.stem = f.stem
        title = re.search(r"(?m)^## (.+?)\s*$", text).group(1)
        parts = re.split(r"<!--\s*stage:\s*([a-z-]+)\s*-->", text)
        sols = {}
        sp = solutions_dir / f.name
        if sp.exists():
            st = sp.read_text(encoding="utf-8").replace("\r\n", "\n")
            for piece in re.split(r"(?m)^####\s+Solution:\s+", st)[1:]:
                h, _, rest = piece.partition("\n")
                im = re.match(r"\s*<!--\s*id:\s*([^\s>]+)\s*-->\s*\n?", rest)
                if not im:
                    raise SystemExit(f"{f.name}: solution '{h.strip()}' has no <!-- id: ... -->")
                sols[im.group(1)] = rest[im.end():]
        lm = re.search(r"<!--\s*lesson-id:\s*([^\s>]+)\s*-->", text)
        if not lm:
            raise SystemExit(f"{f.name}: missing <!-- lesson-id: ... -->; run the manuscript audit first")
        lid = f"lesson-{lm.group(1)}"
        body, n_ex = [], 0
        for i in range(1, len(parts), 2):
            stage, chunk = parts[i], parts[i + 1]
            if stage == "exercises":
                pieces = re.split(r"(?m)^####\s+(?=\[)", chunk)
                intro = self.render(pieces[0])
                cards = "".join(self.exercise(f.stem, p, sols) for p in pieces[1:])
                n_ex = len(pieces) - 1
                body.append(f'<div class="stage stage-exercises">{intro}{cards}</div>')
            else:
                body.append(f'<div class="stage stage-{stage}">{self.render(chunk)}</div>')
        done = (f'<label class="lesson-done"><input type="checkbox" data-id="{lid}"><span><strong>Rebuild check.</strong> I can state the invariant, '
                f'explain why the naive version is too slow, and write the method again without looking.</span></label>')
        sec = f'<section class="lesson" id="{lid}"><h2 id="{lid}-title">{html.escape(title)}</h2>' + "".join(body) + done + "</section>"
        self.index.append({"id": lid, "title": title, "text": visible_text(sec)})
        return lid, title, n_ex, sec


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("chapter_dir"); ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--chapter"); ap.add_argument("--key", help="override the storage key (migrations only; default dsa:chapter-NN)"); ap.add_argument("--title"); ap.add_argument("--series", default="Java DSA Interview Curriculum")
    ap.add_argument("--validation", help="JSON stamp written by audit_manuscripts.py --stamp; adds verified badges and an accurate footer")
    a = ap.parse_args()
    d = Path(a.chapter_dir)
    m = re.match(r"(\d+)-(.*)", d.name)
    num = a.chapter or (m.group(1) if m else "00")
    title = a.title or (m.group(2).replace("-", " ").title() if m else d.name)
    stamp = None
    if a.validation:
        stamp = json.loads(Path(a.validation).read_text(encoding="utf-8"))
        have = compile_java.digest_for_dir(d)
        if stamp.get("digest") != have:
            raise SystemExit("stale validation stamp: the Java in the manuscripts changed after validation (or the stamp has no digest). "
                             "Re-run audit_manuscripts.py --stamp, then build again.")
        if stamp.get("failed"):
            raise SystemExit(f"validation stamp records {stamp['failed']} failing Java block(s); fix them before building")
    verified = bool(stamp and stamp.get("status") == "validated" and stamp.get("blocks"))
    B = Builder(verified)
    nav, main_parts, sections = [], [], 0
    for f in sorted(x for x in d.glob("*.md") if x.name.lower() not in ("readme.md", "review-log.md")):
        text = f.read_text(encoding="utf-8").replace("\r\n", "\n")
        B.stem = f.stem
        k = re.search(r"<!--\s*lesson-kind:\s*(\w+)\s*-->", text)
        s = re.search(r"<!--\s*section:\s*([\w-]+)\s*-->", text)
        if k:
            lid, t, n, h = B.lesson(f, text, d / "solutions")
            nav.append(("lesson", f'<li><a href="#{lid}" data-lesson="{lid}"><span>{html.escape(t)} <small>({n})</small></span><span class="tick">\u2713</span></a></li>'))
            main_parts.append(h)
        elif s:
            kind = s.group(1)
            label = {"orientation": "Orientation", "unlocked-combinations": "Unlocked combinations", "review": "Review"}.get(kind, kind.title())
            sid = f"sec-{f.stem}"
            nav.append(("front" if kind == "orientation" else "back", f'<li><a href="#{sid}"><span>{label}</span></a></li>'))
            sec = f'<section class="chapter-section" id="{sid}">{B.render(text)}</section>'
            B.index.append({"id": sid, "title": label, "text": visible_text(sec)})
            main_parts.append(sec)
        else:
            print(f"warning: {f.name} has no lesson-kind or section marker; skipped", file=sys.stderr)
    front = "".join(x for g, x in nav if g == "front")
    lessons = "".join(x for g, x in nav if g == "lesson")
    back = "".join(x for g, x in nav if g == "back")
    navhtml = ('<input id="search" type="search" placeholder="Search this chapter" aria-label="Search this chapter"><div id="search-results"></div>'
               f'<ol>{front}</ol><div class="grp">Lessons</div><ol>{lessons}</ol><div class="grp">Wrap-up</div><ol>{back}<li><a href="#my-notes"><span>My notes</span></a></li></ol>')
    notes = ('<section class="mynotes" id="my-notes"><h2>My Notes</h2><p>Write what you would tell yourself before an interview: the recognition cues you missed, '
             'the invariants you broke, and the problems to repeat. Notes are saved in this browser only, so export a backup now and then.</p>'
             '<label for="chapter-notes"><strong>Chapter notes</strong> <span id="chapter-saved" class="src"></span></label>'
             '<textarea id="chapter-notes" class="big" placeholder="Cues I missed, bugs I hit, problems to redo..."></textarea>'
             '<div class="row"><button type="button" class="primary" id="export-md">Export notes (.md)</button><button type="button" id="copy-notes">Copy notes</button>'
             '<button type="button" id="export-json">Backup (.json)</button><label class="btn" for="import-json">Import backup</label>'
             '<input id="import-json" type="file" accept="application/json,.json" hidden><button type="button" id="reset-all">Reset chapter</button></div></section>')
    css = (ASSETS / "textbook.css").read_text(encoding="utf-8")
    js = (ASSETS / "textbook.js").read_text(encoding="utf-8")
    if verified:
        j = stamp["jdk"] or {}
        rel = stamp.get("release_effective")
        rel_txt = "" if rel in (None, "default") else f", --release {rel}"
        note = (f"Java: {stamp['ok']} of {stamp['blocks']} blocks compiled on JDK {j.get('version', '?')} ({j.get('vendor', '?')}{rel_txt}) on {stamp['date']}; "
                f"{stamp['ran_with_assertions']} ran with assertions.")
    else:
        note = "Java examples in this file were not machine-validated."
    page = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Chapter {html.escape(num)} - {html.escape(title)}</title><style>{css}</style></head>
<body data-chapter-key="{html.escape(a.key or 'dsa:chapter-' + num)}" data-chapter-title="Chapter {html.escape(num)}: {html.escape(title)}">
<div class="topbar"><button type="button" id="menu-btn" aria-label="Contents">Menu</button><div class="title"><small>{html.escape(a.series)}</small>Chapter {html.escape(num)}: {html.escape(title)}</div>
<div class="progress"><div class="bar"><i id="progress-bar"></i></div><span id="progress-text"></span></div><button type="button" id="theme-toggle" aria-label="Toggle theme">Theme</button><button type="button" id="print-btn">Print</button></div>
<div class="layout"><nav class="side" aria-label="Chapter contents">{navhtml}</nav><main>
<div class="chapter-head"><div class="kicker">Chapter {html.escape(num)}</div><h1>{html.escape(title)}</h1></div>
{"".join(main_parts)}{notes}<footer class="page">{html.escape(a.series)} - built from Markdown manuscripts. {note}</footer></main></div>
<script type="application/json" id="search-index">{json.dumps(B.index, ensure_ascii=False).replace("</", "<\\/")}</script>
<script>{js}</script></body></html>"""
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(page, encoding="utf-8")
    print(f"wrote {a.out} ({len(page) // 1024} KB, {len(main_parts)} sections)")


if __name__ == "__main__":
    main()
