#!/usr/bin/env python3
"""Deterministic substance audit for Markdown chapter manuscripts.

Usage:
  audit_manuscripts.py CHAPTER_DIR_OR_ROOT [--spec SPEC_FILE_OR_DIR] [--draft] [--no-java] [--release N] [--json]

A chapter directory holds: orientation, lesson files (NN-slug.md), optional combinations and review files,
and solutions/NN-slug.md files paired with the lessons. See the authoring skill's lesson-architecture.md.
Exit code 1 when any ERROR is found. --draft downgrades missing lessons/sections to warnings.
"""
import argparse, json, re, sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import compile_java

STAGES = ["context", "naive", "bottleneck", "insight", "variables", "trace", "code", "applicability", "exercises"]
STAGES_COMBO = STAGES[:1] + ["contributions"] + STAGES[1:]
MIN_WORDS = {"context": 60, "naive": 30, "bottleneck": 60, "insight": 120, "variables": 40, "trace": 100,
             "code": 30, "applicability": 80, "contributions": 60}
BULLET_LED = {"trace", "applicability"}  # structured bullets allowed (user rule, Oct 4); context/naive/bottleneck/insight stay prose-led
NARRATIVE = {"context", "naive", "bottleneck", "insight", "trace", "applicability", "contributions"}
ROLES = ["Build", "Vary", "Boundary", "Recognize", "Extend", "Medium", "Hard", "Challenge"]
FIELDS = [("Prerequisites", 3), ("Problem", 15), ("Constraints", 5), ("Example 1", 3), ("Example 2", 3),
          ("Hint", 8), ("Changed decision", 6)]
FILLER = ["let's dive in", "let us dive in", "in this lesson, we will", "it is important to remember",
          "it's important to note", "in conclusion,", "in summary,", "powerful technique", "game changer",
          "without further ado", "buckle up", "needless to say", "as we all know",
          "before coding, state the input contract"]
ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]{2,60}$")
NORM = lambda s: re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()
FIELD_PARA = re.compile(r"\*\*(Prerequisites|Constraints|Example \d|Changed decision|Complexity)\.\*\*")
WORDS = lambda s: re.findall(r"[A-Za-z0-9_']+", s)


class Report:
    def __init__(self):
        self.items = []

    def add(self, level, where, code, msg):
        self.items.append({"level": level, "where": str(where), "code": code, "msg": msg})

    def err(self, where, code, msg): self.add("ERROR", where, code, msg)
    def warn(self, where, code, msg): self.add("WARN", where, code, msg)


def read(p):
    return Path(p).read_text(encoding="utf-8").replace("\r\n", "\n")


def strip_fences(text, keep_info=False):
    out, infence = [], False
    for line in text.split("\n"):
        if line.startswith("```"):
            infence = not infence
            continue
        if not infence:
            out.append(line)
    return "\n".join(out)


def fences(text):
    res, cur, info = [], None, None
    for line in text.split("\n"):
        if line.startswith("```"):
            if cur is None:
                cur, info = [], line[3:].strip()
            else:
                res.append((info, "\n".join(cur))); cur = None
        elif cur is not None:
            cur.append(line)
    return res


def split_stages(text):
    parts = re.split(r"<!--\s*stage:\s*([a-z-]+)\s*-->", text)
    return [(parts[i], parts[i + 1]) for i in range(1, len(parts), 2)]


def prose(text):
    t = strip_fences(text)
    t = re.sub(r"<!--.*?-->", "", t, flags=re.S)
    return "\n".join(l for l in t.split("\n") if not l.startswith("#"))


def parse_exercises(body):
    ex = []
    pieces = re.split(r"(?m)^####\s+(?=\[)", body)
    for piece in pieces[1:]:
        head, _, rest = piece.partition("\n")
        idm = re.match(r"\s*<!--\s*id:\s*([^\s>]+)\s*-->\s*\n?", rest)
        eid = idm.group(1) if idm else None
        if idm:
            rest = rest[idm.end():]
        m = re.match(r"\[(\w+)\]\s+(.*?)\s*$", head)
        if not m:
            ex.append({"role": None, "title": head.strip(), "body": rest, "id": eid}); continue
        title = m.group(2)
        src = re.search(r"\((LeetCode\s+(\d+)|Author exercise)\)\s*$", title)
        ex.append({"role": m.group(1), "title": title, "body": rest, "id": eid, "src": src.group(1) if src else None,
                   "lc": int(src.group(2)) if src and src.group(2) else None,
                   "base": NORM(re.sub(r"\((?:LeetCode\s+\d+|Author exercise)\)\s*$", "", title))})
    return ex


def field(body, label):
    m = re.search(rf"\*\*{re.escape(label)}\.\*\*\s*(.+?)(?:\n\s*\n|\Z)", body, re.S)
    return m.group(1).strip() if m else None


def parse_spec(path):
    text, lessons = read(path), {}
    for sec in ("Lesson Blueprints", "Released Combination Lessons"):
        m = re.search(rf"(?ms)^## {sec}\s*\n(.*?)(?=^## |\Z)", text)
        if not m:
            continue
        for h, block in re.findall(r"(?ms)^### (.+?)\n(.*?)(?=^### |\Z)", m.group(1)):
            if h.strip().lower().startswith("deferred"):
                continue
            exs = []
            for role, title in re.findall(r"(?m)^- \*\*(\w+)\s*[-\u2013\u2014]\s*(.+?)\.\*\*", block):
                lc = re.match(r"LC\s+(\d+)\s*(.*)", title)
                if lc:
                    exs.append({"role": role, "lc": int(lc.group(1)), "base": NORM(lc.group(2))})
                else:
                    exs.append({"role": role, "lc": None, "base": NORM(re.sub(r"^Author exercise:\s*", "", title))})
            lessons[NORM(h)] = {"title": h.strip(), "exercises": exs}
    return lessons


def find_spec(spec, chapter_dir):
    p = Path(spec)
    if p.is_file():
        return p
    num = re.match(r"(\d+)", chapter_dir.name)
    if p.is_dir() and num:
        c = sorted(p.glob(f"{num.group(1)}-*.md"))
        return c[0] if c else None
    return None


def audit_chapter(ch, spec, draft, rep, corpus):
    files = sorted(f for f in ch.glob("*.md") if f.name.lower() not in ("readme.md", "review-log.md"))
    sol_dir = ch / "solutions"
    lessons, sections, h1s = [], {}, []
    for f in files:
        text = read(f)
        if re.search(r"(?m)^# ", strip_fences(text)):
            rep.warn(f, "h1", "H1 found; the HTML builder adds the chapter title, so manuscripts start at H2")
        kind = re.search(r"<!--\s*lesson-kind:\s*(\w+)\s*-->", text)
        sec = re.search(r"<!--\s*section:\s*([\w-]+)\s*-->", text)
        if kind:
            lessons.append((f, text, kind.group(1)))
        elif sec:
            sections[sec.group(1)] = (f, text)
        else:
            rep.err(f, "untyped-file", "file has neither <!-- lesson-kind: ... --> nor <!-- section: ... --> marker")
    lvl = rep.warn if draft else rep.err
    for need in ("orientation", "unlocked-combinations", "review"):
        if need not in sections:
            lvl(ch, "missing-section", f"chapter has no '{need}' section file")
    if not lessons:
        rep.err(ch, "no-lessons", "no lesson files found")

    titles, ex_total = {}, 0
    lesson_ids, exercise_ids = {}, {}
    for f, text, kind in lessons:
        corpus["files"].append((f, text, f.stem))
        h2 = re.findall(r"(?m)^## (.+?)\s*$", strip_fences(text))
        if len(h2) != 1:
            rep.err(f, "lesson-title", f"lesson file must have exactly one H2 title, found {len(h2)}")
        title = h2[0] if h2 else f.stem
        titles[NORM(title)] = (title, f)
        lm = re.search(r"<!--\s*lesson-id:\s*([^\s>]+)\s*-->", text)
        if not lm:
            rep.err(f, "lesson-id-missing", f"[{title}] needs <!-- lesson-id: your-permanent-slug --> under the lesson-kind marker")
        elif not ID_RE.match(lm.group(1)):
            rep.err(f, "id-format", f"lesson id '{lm.group(1)}' must be lowercase letters, digits and hyphens (3 to 61 chars)")
        elif lm.group(1) in lesson_ids:
            rep.err(f, "id-duplicate", f"lesson id '{lm.group(1)}' is also used in {lesson_ids[lm.group(1)].name}")
        else:
            lesson_ids[lm.group(1)] = f
        need = STAGES_COMBO if kind == "combination" else STAGES
        stages = split_stages(text)
        names = [n for n, _ in stages]
        pos = -1
        for s in need:
            if s not in names:
                rep.err(f, "stage-missing", f"[{title}] missing <!-- stage: {s} -->")
            else:
                i = names.index(s)
                if i < pos:
                    rep.err(f, "stage-order", f"[{title}] stage '{s}' is out of order")
                pos = max(pos, i)
        sd = dict(stages)
        for s, body in stages:
            wc = len(WORDS(prose(body)))
            if s in MIN_WORDS and wc < MIN_WORDS[s]:
                rep.err(f, "stage-thin", f"[{title}] stage '{s}' has {wc} words of prose; minimum {MIN_WORDS[s]}")
            words = [w.lower() for w in WORDS(prose(body))]
            if s != "exercises" and len(words) >= 150 and len(set(words)) / len(words) < 0.38:
                rep.warn(f, "low-diversity", f"[{title}] stage '{s}' reuses a small vocabulary ({len(set(words))} distinct of {len(words)} words); check for padding")
            if s in NARRATIVE:
                lines = [l for l in strip_fences(body).split("\n") if l.strip() and not l.startswith("#") and not l.startswith("<!--")]
                bullets = sum(1 for l in lines if re.match(r"\s*([-*]|\d+\.)\s", l))
                tables = sum(1 for l in lines if l.lstrip().startswith("|"))
                cap = 0.85 if s in BULLET_LED else 0.3
                if lines and bullets / len(lines) > cap:
                    rep.err(f, "bullet-heavy", f"[{title}] stage '{s}' is {bullets}/{len(lines)} bullet lines; write narrative prose")
                if s == "trace" and lines and tables / len(lines) > 0.3:
                    rep.err(f, "trace-table", f"[{title}] the trace stage is mostly a table; narrate it")
        if "code" in sd and not any(i.split()[:1] == ["java"] for i, _ in fences(sd["code"])):
            rep.err(f, "no-code", f"[{title}] code stage has no ```java block")
        if "naive" in sd and not any(i.split()[:1] == ["java"] for i, _ in fences(sd["naive"])):
            rep.warn(f, "naive-no-code", f"[{title}] naive stage has no ```java block")
        if "bottleneck" in sd and not re.search(r"O\(", sd["bottleneck"]):
            rep.err(f, "no-complexity", f"[{title}] bottleneck stage states no Big-O cost")
        if "applicability" in sd:
            a = sd["applicability"].lower()
            if "invariant" not in a:
                rep.err(f, "no-invariant", f"[{title}] applicability stage never states the invariant")
            if "false friend" not in a:
                rep.warn(f, "no-false-friend", f"[{title}] applicability stage names no false friend")
        if "insight" in sd:
            m = re.search(r"<!--\s*names:\s*(.+?)\s*-->", sd["insight"])
            if not m:
                rep.err(f, "no-names", f"[{title}] insight stage needs <!-- names: term, term --> listing the vocabulary it introduces")
            else:
                ptxt = prose(sd["insight"]).lower()
                for nm in [x.strip() for x in m.group(1).split(",") if x.strip()]:
                    if nm.lower() not in ptxt:
                        rep.err(f, "name-not-introduced", f"[{title}] '{nm}' is listed in names but never appears in the insight prose")
                    for early in ("context", "naive"):
                        if early in sd and nm.lower() in prose(sd[early]).lower():
                            rep.warn(f, "jargon-early", f"[{title}] '{nm}' appears in the {early} stage, before the idea earns its name")
        if "trace" in sd:
            tb = [b for i, b in fences(sd["trace"]) if i == "trace"]
            if not tb:
                rep.warn(f, "no-stepper", f"[{title}] no ```trace block, so the HTML lesson has no interactive stepper")
            for b in tb:
                try:
                    o = json.loads(b); n = len(o["cells"])
                    assert len(o["steps"]) >= 3, "a trace needs at least 3 steps"
                    for st in o["steps"]:
                        for k, v in st["at"].items():
                            assert isinstance(v, int) and -1 <= v <= n, f"pointer {k}={v} out of range"
                except Exception as e:
                    rep.err(f, "bad-trace", f"[{title}] invalid trace block: {e}")
        # exercises
        exs = parse_exercises(sd.get("exercises", ""))
        ex_total += len(exs)
        if not exs:
            rep.err(f, "no-exercises", f"[{title}] no exercise records")
        last = -1
        roles = set()
        for e in exs:
            where = f"{f.name} :: {e['title']}"
            if not e.get("id"):
                rep.err(where, "exercise-id-missing", "add <!-- id: your-permanent-slug --> on the line after the #### heading; notes and progress are keyed to it")
            elif not ID_RE.match(e["id"]):
                rep.err(where, "id-format", f"exercise id '{e['id']}' must be lowercase letters, digits and hyphens (3 to 61 chars)")
            elif e["id"] in exercise_ids or e["id"] in lesson_ids:
                rep.err(where, "id-duplicate", f"exercise id '{e['id']}' is already used")
            else:
                exercise_ids[e["id"]] = f
            if e["role"] not in ROLES:
                rep.err(where, "bad-role", f"role must be one of {ROLES}"); continue
            roles.add(e["role"])
            if ROLES.index(e["role"]) < last:
                rep.err(where, "role-order", "ladder roles must not go backward")
            last = max(last, ROLES.index(e["role"]))
            if not e.get("src"):
                rep.err(where, "no-source", "title must end with (LeetCode N) or (Author exercise)")
            for lab, minw in FIELDS:
                v = field(e["body"], lab)
                if v is None:
                    rep.err(where, "field-missing", f"missing **{lab}.**")
                elif len(WORDS(v)) < minw:
                    rep.err(where, "field-thin", f"**{lab}.** has {len(WORDS(v))} words; minimum {minw}")
                elif lab.startswith("Example") and not ("input" in v.lower() and "output" in v.lower()):
                    rep.err(where, "example-shape", f"**{lab}.** must state an Input and an output")
        for r in ("Build", "Vary", "Boundary", "Recognize"):
            if exs and r not in roles:
                rep.err(f, "ladder-gap", f"[{title}] practice ladder has no {r} step")
        if len(exs) < 4:
            rep.err(f, "ladder-short", f"[{title}] {len(exs)} exercises; minimum 4")
        if len(exs) > 7:
            rep.warn(f, "ladder-long", f"[{title}] {len(exs)} exercises; more than 7 should be justified")
        # solutions
        sp = sol_dir / f.name
        if not sp.exists():
            rep.err(f, "no-solutions", f"[{title}] missing solutions/{f.name}")
        else:
            st = read(sp)
            corpus["files"].append((sp, st, f.stem))
            sols = {}
            for piece in re.split(r"(?m)^####\s+Solution:\s+", st)[1:]:
                head, _, rest = piece.partition("\n")
                im = re.match(r"\s*<!--\s*id:\s*([^\s>]+)\s*-->\s*\n?", rest)
                if not im:
                    rep.err(sp, "solution-id-missing", f"solution '{head.strip()}' needs <!-- id: ... --> matching its exercise")
                    continue
                if im.group(1) in sols:
                    rep.err(sp, "id-duplicate", f"two solutions share id '{im.group(1)}'")
                sols[im.group(1)] = rest[im.end():]
            have = {e.get("id") for e in exs}
            for e in exs:
                body = sols.get(e.get("id"))
                if body is None:
                    rep.err(f"{sp.name} :: {e['title']}", "solution-missing", f"no '#### Solution:' record with <!-- id: {e.get('id')} -->")
                    continue
                for lab in ("Approach", "Complexity"):
                    if field(body, lab) is None:
                        rep.err(f"{sp.name} :: {e['title']}", "solution-field", f"missing **{lab}.**")
                if not any(i.split()[:1] == ["java"] for i, _ in fences(body)):
                    rep.err(f"{sp.name} :: {e['title']}", "solution-code", "solution has no ```java block")
            for k in sols:
                if k not in have:
                    rep.warn(sp, "solution-orphan", f"solution '{k}' matches no exercise")
        corpus["lessons"] += 1
    for kind, (f, text) in sections.items():
        corpus["files"].append((f, text, f.stem))
        for info, body in fences(text):
            if info.split()[:1] == ["quiz"]:
                try:
                    qs = json.loads(body)
                    qs = qs if isinstance(qs, list) else [qs]
                    for q in qs:
                        if not q.get("id"):
                            rep.warn(f, "quiz-id-missing", "quiz question has no \"id\"; its saved answer is keyed by position and is lost if blocks are reordered")
                        if not isinstance(q.get("answer"), int) or not (0 <= q["answer"] < len(q.get("options", []))):
                            rep.err(f, "bad-quiz", f"quiz '{str(q.get('q'))[:40]}' needs options and a valid zero-based answer index")
                except Exception as e:
                    rep.err(f, "bad-quiz", f"invalid quiz JSON: {e}")
        if kind == "unlocked-combinations" and len(WORDS(prose(text))) < 20:
            rep.err(f, "section-thin", "unlocked-combinations needs content, or an explicit 'No new teach-now combinations' statement")
    corpus["exercises"] += ex_total
    corpus["ids"][str(ch)] = (set(lesson_ids), set(exercise_ids))

    # spec parity
    if spec:
        sl = parse_spec(spec)
        for key, sv in sl.items():
            if key not in titles:
                (rep.warn if draft else rep.err)(ch, "spec-lesson-missing", f"spec lesson '{sv['title']}' has no manuscript lesson")
                continue
            title, f = titles[key]
            text = read(f)
            exs = parse_exercises(dict(split_stages(text)).get("exercises", ""))
            for se in sv["exercises"]:
                hit = [e for e in exs if (se["lc"] and e.get("lc") == se["lc"]) or (not se["lc"] and e.get("base") == se["base"])]
                if not hit:
                    rep.err(f"{f.name}", "spec-exercise-missing", f"spec {se['role']} exercise '{se['base']}' (LC {se['lc']}) not found")
                elif hit[0]["role"] != se["role"]:
                    rep.warn(f"{f.name}", "spec-role", f"'{se['base']}' is {hit[0]['role']} in the manuscript but {se['role']} in the spec")
        for key, (title, f) in titles.items():
            if key not in sl:
                rep.warn(f, "lesson-not-in-spec", f"lesson '{title}' does not appear in the spec")


def check_human_review(ch, rep, draft, lesson_ids):
    """A completion claim needs a human quality verdict per lesson in review-log.md. The AI must never write this file."""
    log = ch / "review-log.md"
    lvl = rep.warn if draft else rep.err
    if not log.exists():
        lvl(ch, "no-human-review", "review-log.md is missing; scripts check structure, a person must judge the teaching (see the auditor skill)")
        return
    t = log.read_text(encoding="utf-8")
    if not re.search(r"(?mi)^Reviewed-by:\s*\S+", t) or not re.search(r"(?mi)^Date:\s*\d{4}-\d{2}-\d{2}", t):
        lvl(log, "review-log-format", "review-log.md needs 'Reviewed-by: name' and 'Date: YYYY-MM-DD' lines")
    verdicts = dict(re.findall(r"(?mi)^-\s*([a-z0-9-]+):\s*(pass|revise)\b", t))
    for lid in sorted(lesson_ids):
        v = verdicts.get(lid)
        if v is None:
            lvl(log, "review-missing", f"no human verdict for lesson '{lid}' (add '- {lid}: pass' or '- {lid}: revise - note')")
        elif v.lower() == "revise":
            rep.err(log, "review-revise", f"lesson '{lid}' is marked revise")


def check_id_lock(ch, rep, update, lesson_ids, exercise_ids):
    lock = ch / "ids.lock"
    cur = {"lessons": sorted(lesson_ids), "exercises": sorted(exercise_ids)}
    if lock.exists():
        old = json.loads(lock.read_text(encoding="utf-8"))
        retired = set(old.get("retired", []))
        for kind in ("lessons", "exercises"):
            for i in old.get(kind, []):
                if i not in cur[kind] and i not in retired:
                    rep.err(lock, "id-removed", f"{kind[:-1]} id '{i}' was published but is gone; restore it, or list it under \"retired\" in ids.lock if you really intend to orphan saved notes")
    if update:
        old = json.loads(lock.read_text(encoding="utf-8")) if lock.exists() else {}
        merged = {k: sorted(set(old.get(k, [])) | set(cur[k])) for k in ("lessons", "exercises")}
        merged["retired"] = sorted(set(old.get("retired", [])))
        lock.write_text(json.dumps(merged, indent=1) + "\n", encoding="utf-8")


def style_checks(rep, corpus):
    para_seen, sent_seen, code_seen = defaultdict(list), defaultdict(list), defaultdict(set)
    gram_files = defaultdict(set)
    allow = set(corpus.get("allow", []))
    for f, text, stem in corpus["files"]:
        low = text.lower()
        for ph in FILLER:
            if ph in low:
                rep.err(f, "filler", f"filler phrase: '{ph}'")
        for h in re.findall(r"(?m)^(#{2,3}) (.+?)\s*$", strip_fences(text)):
            t = h[1]
            if ":" in t or t.endswith(".") or len(t.split()) > 7:
                rep.err(f, "heading-style", f"heading '{t}': use a short descriptive title (no colon, no period, at most 7 words)")
        for p in re.split(r"\n\s*\n", prose(text)):
            p = p.strip()
            if not p or FIELD_PARA.match(p):
                continue
            n = NORM(p)
            if len(n.split()) >= 12:
                para_seen[n].append(f)
            for s in re.split(r"(?<=[.!?])\s+", p):
                ns = NORM(s)
                if len(ns.split()) >= 9:
                    sent_seen[ns].append(f)
            ws = NORM(p).split()
            for i in range(len(ws) - 7):
                gram_files[" ".join(ws[i:i + 8])].add(str(f))
        for info, code in fences(text):
            if info.split()[:1] == ["java"] and code.count("\n") >= 2:
                code_seen[re.sub(r"\s+", " ", code).strip()].add(stem)
    for n, fs in para_seen.items():
        if len(fs) > 1:
            rep.err(fs[0], "duplicate-paragraph", f"paragraph repeated {len(fs)} times: '{n[:70]}...'")
    para_norms = {n for n, fs in para_seen.items() if len(fs) > 1}
    for n, fs in sent_seen.items():
        if len(fs) >= 2 and not any(n.startswith(a) for a in allow) and not any(n in pn for pn in para_norms):
            rep.err(fs[0], "repeated-sentence", f"sentence appears {len(fs)} times (add to allow-repeats.txt only if it is deliberate): '{n[:80]}...'")
    shared = [(g, fs) for g, fs in gram_files.items() if len(fs) >= 3 and not any(g.startswith(a) for a in allow)]
    strong = [(g, fs) for g, fs in shared if len(fs) >= 4]
    if strong:
        g, fs = max(strong, key=lambda x: len(x[1]))
        rep.err(sorted(fs)[0], "template-phrase", f"{len(strong)} word sequences recur in 4+ files, e.g. '{g}' in {len(fs)} files: lessons look templated")
    elif shared:
        g, fs = max(shared, key=lambda x: len(x[1]))
        rep.warn(sorted(fs)[0], "template-phrase", f"{len(shared)} word sequences recur in 3 files, e.g. '{g}'")
    for c, stems in code_seen.items():
        if len(stems) > 1:
            rep.err(sorted(stems)[0], "duplicate-code", f"identical Java block appears in lessons {sorted(stems)}: '{c[:50]}...'")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path")
    ap.add_argument("--spec")
    ap.add_argument("--draft", action="store_true")
    ap.add_argument("--no-java", action="store_true")
    ap.add_argument("--release", default="21")
    ap.add_argument("--allow-missing-jdk", action="store_true")
    ap.add_argument("--workdir", help="scratch directory for Java compilation")
    ap.add_argument("--stamp", help="write a Java validation stamp JSON here (read by build_html.py --validation)")
    ap.add_argument("--update-ids", action="store_true", help="record current lesson and exercise ids in each chapter's ids.lock")
    ap.add_argument("--allow-repeats", help="file of normalized sentence prefixes that may repeat")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    root = Path(a.path)
    chapters = [root] if any(root.glob("*.md")) else sorted(d for d in root.iterdir() if d.is_dir() and re.match(r"\d\d-", d.name))
    rep, corpus = Report(), {"files": [], "lessons": 0, "exercises": 0, "ids": {}}
    allow_file = Path(a.allow_repeats) if a.allow_repeats else None
    corpus["allow"] = []
    for cand in [allow_file] + [c / "allow-repeats.txt" for c in chapters]:
        if cand and cand.exists():
            corpus["allow"] += [NORM(l) for l in cand.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")]
    for ch in chapters:
        spec = find_spec(a.spec, ch) if a.spec else None
        if a.spec and not spec:
            rep.warn(ch, "no-spec", "no matching spec file found")
        audit_chapter(ch, spec, a.draft, rep, corpus)
    for ch in chapters:
        li, ei = corpus["ids"].get(str(ch), (set(), set()))
        check_id_lock(ch, rep, a.update_ids, li, ei)
        check_human_review(ch, rep, a.draft, li)
    style_checks(rep, corpus)
    java_status = "skipped"
    root_dir = chapters[0] if len(chapters) == 1 else None
    if not a.no_java:
        results, jinfo = compile_java.check_files([f for f, _, _ in corpus["files"]], a.release, a.workdir)
        java_status = jinfo["status"]
        if a.stamp:
            compile_java.write_stamp(a.stamp, results, jinfo, root_dir)
        for r in results:
            if r["status"] == "fail":
                rep.err(f"{Path(r['file']).name}:{r['line']}", "java", r["msg"])
        if java_status == "not-validated":
            (rep.warn if a.allow_missing_jdk else rep.err)(root, "java-not-validated", "NOT VALIDATED: no JDK compiler available; Java was not compiled")
    errs = [i for i in rep.items if i["level"] == "ERROR"]
    if a.json:
        print(json.dumps({"errors": len(errs), "items": rep.items, "lessons": corpus["lessons"], "exercises": corpus["exercises"], "java": java_status}, indent=1))
    else:
        for i in rep.items:
            print(f"{i['level']:5} {i['code']:22} {i['where']}\n        {i['msg']}")
        c = Counter(i["code"] for i in errs)
        if not a.no_java and jinfo.get("jdk"):
            print(f"\njdk: {jinfo['jdk']['version']} ({jinfo['jdk']['vendor']}); release flag: {jinfo['release_effective']}")
        print(f"\nchapters={len(chapters)} lessons={corpus['lessons']} exercises={corpus['exercises']} java={java_status}")
        print(f"errors={len(errs)} warnings={len(rep.items) - len(errs)}" + (f"  top: {c.most_common(4)}" if c else ""))
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
