#!/usr/bin/env python3
"""Compile (and optionally run) every ```java block found in Markdown manuscripts.

Block conventions (info string after ```java):
  (none)      compile only. A block with no top-level class/record/interface/enum is wrapped in a
              class, so it may contain one or more methods but not loose statements.
  run         compile, then run main() with assertions enabled; nonzero exit fails the block.
  nocompile   deliberately skipped (for intentionally broken code). Counted and reported.
Stub types ListNode, TreeNode and Node are supplied unless the block declares its own.

Scratch space: --workdir DIR, else $DSA_WORKDIR, else the system temp dir, else ./.dsa-scratch. The first
writable one wins. Each run creates a UUID-named directory with a plain mkdir (no tempfile.mkdtemp, which
restricts permissions in ways that break some Windows setups) and removes it afterwards.

Default --release is 21 (the language level the curriculum teaches). The stamp records the JDK that actually ran.

--stamp FILE writes a JSON record of what was actually validated (JDK version, release flag, block counts,
date). The HTML builder reads it for the chapter footer, so published claims cannot drift from reality.

Exit codes: 0 all good, 1 failures, 2 no JDK found (0 with --allow-missing-jdk, reported as NOT VALIDATED).
"""
import argparse, datetime, hashlib, json, os, re, shutil, subprocess, sys, tempfile, uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
IMPORTS = "import java.util.*;\nimport java.util.function.*;\nimport java.util.stream.*;\n"
STUBS = {
    "ListNode": "public class ListNode { public int val; public ListNode next; public ListNode() {} public ListNode(int v) { val = v; } public ListNode(int v, ListNode n) { val = v; next = n; } }\n",
    "TreeNode": "public class TreeNode { public int val; public TreeNode left, right; public TreeNode() {} public TreeNode(int v) { val = v; } public TreeNode(int v, TreeNode l, TreeNode r) { val = v; left = l; right = r; } }\n",
    "Node": "import java.util.*;\npublic class Node { public int val; public Node next, random, left, right, prev, child; public List<Node> neighbors = new ArrayList<>(), children = new ArrayList<>(); public Node() {} public Node(int v) { val = v; } }\n",
}
TOP = re.compile(r"^(?:(?:public|final|abstract|sealed|non-sealed|strictfp)\s+)*(?:class|interface|record|enum)\s+(\w+)", re.M)


def extract_blocks(md_path):
    blocks, lines, i = [], Path(md_path).read_text(encoding="utf-8").replace("\r\n", "\n").split("\n"), 0
    while i < len(lines):
        m = re.match(r"^```\s*(\S.*)?$", lines[i])
        if m:
            info, start, body = (m.group(1) or "").strip(), i + 1, []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                body.append(lines[i]); i += 1
            toks = info.split()
            if toks and toks[0] == "java":
                blocks.append({"file": str(md_path), "line": start, "flags": set(toks[1:]), "code": "\n".join(body)})
        i += 1
    return blocks


def prepare(block):
    code = block["code"]
    m = TOP.search(code)
    if m:
        src, offset, cls = IMPORTS + code + "\n", IMPORTS.count("\n"), m.group(1)
    else:
        prefix = IMPORTS + "final class Snip {\n"
        src, offset, cls = prefix + code + "\n}\n", prefix.count("\n"), "Snip"
    return src, offset, cls


def scratch_dir(workdir=None):
    for base in [workdir, os.environ.get("DSA_WORKDIR"), tempfile.gettempdir(), str(Path.cwd() / ".dsa-scratch")]:
        if not base:
            continue
        try:
            Path(base).mkdir(parents=True, exist_ok=True)
            d = Path(base) / ("dsa-java-" + uuid.uuid4().hex)
            d.mkdir()
            return d
        except OSError:
            continue
    raise SystemExit("no writable scratch directory found; pass --workdir DIR or set DSA_WORKDIR")


def jdk_version(java):
    try:
        r = subprocess.run([java, "-XshowSettings:properties", "-version"], capture_output=True, text=True, timeout=60)
        props = dict(re.findall(r"^\s+(java\.(?:version|vendor|specification\.version)) = (.+)$", r.stderr, re.M))
        return {"version": props.get("java.version", "unknown"), "vendor": props.get("java.vendor", "unknown"),
                "feature": props.get("java.specification.version", "unknown")}
    except Exception:
        return {"version": "unknown", "vendor": "unknown", "feature": "unknown"}


def check_files(md_files, release=None, workdir=None):
    """Returns (results, info). info['status'] is 'validated' or 'not-validated' and records the JDK actually used."""
    blocks = [b for f in md_files for b in extract_blocks(f)]
    results, todo = [], []
    info = {"status": "validated", "jdk": None, "release_requested": release, "release_effective": None}
    for b in blocks:
        if "nocompile" in b["flags"]:
            results.append({**b, "status": "skipped", "msg": "marked nocompile"})
        else:
            todo.append(b)
    if not todo:
        return results, info
    java = shutil.which("java")
    if not java:
        info["status"] = "not-validated"
        results += [{**b, "status": "not-validated", "msg": "no JDK on PATH"} for b in todo]
        return results, info
    info["jdk"] = jdk_version(java)
    root = scratch_dir(workdir)
    try:
        meta = {}
        for n, b in enumerate(todo):
            d = root / f"b{n:04d}"
            d.mkdir()
            src, offset, cls = prepare(b)
            (d / f"{cls}.java").write_text(src, encoding="utf-8")
            for name, text in STUBS.items():
                if not re.search(rf"\b(class|record|interface|enum)\s+{name}\b", b["code"]):
                    (d / f"{name}.java").write_text(text, encoding="utf-8")
            meta[d.name] = (b, offset, cls)
        jopt = f"-Djava.io.tmpdir={root}"
        cmd = [java, jopt, str(HERE / "JavaCheck.java"), str(root)] + ([release] if release else [])
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
        out = proc.stdout.strip().splitlines()
        if out and out[0] == "NOCOMPILER":
            info["status"] = "not-validated"
            results += [{**b, "status": "not-validated", "msg": "JRE without compiler (need a JDK)"} for b in todo]
            return results, info
        seen = set()
        for line in out:
            parts = line.split("\t")
            if parts[0] == "NOTE":
                print("note: " + parts[1], file=sys.stderr)
                info["release_effective"] = "default"
                continue
            b, offset, cls = meta[parts[1]]
            seen.add(parts[1])
            if parts[0] == "OK":
                res = {**b, "status": "ok", "msg": ""}
                if "run" in b["flags"]:
                    r = subprocess.run([java, jopt, "-ea", "-cp", str(root / parts[1] / "out"), cls], capture_output=True, text=True, timeout=60)
                    if r.returncode != 0:
                        first = (r.stderr.strip().splitlines() or ["nonzero exit"])
                        res.update(status="fail", msg="run failed: " + next((l for l in first if "Exception" in l or "Error" in l), first[0]))
                results.append(res)
            else:
                msg = parts[2]
                m = re.match(r"L(\d+): (.*)", msg)
                if m:
                    msg = f"line {max(1, int(m.group(1)) - offset)} of block: {m.group(2)}"
                results.append({**b, "status": "fail", "msg": msg})
        for name, (b, _, _) in meta.items():
            if name not in seen:
                results.append({**b, "status": "fail", "msg": "compiler produced no result: " + proc.stderr.strip()[:200]})
    finally:
        shutil.rmtree(root, ignore_errors=True)
    if info["release_effective"] is None:
        info["release_effective"] = release or "default"
    return results, info


def source_digest(blocks, root):
    """SHA-256 over every Java block: manuscript path relative to root, ordinal in file, sorted flags, code.
    The builder recomputes this, so editing any Java after validation makes the stamp stale."""
    root = Path(root).resolve()
    per, rows = {}, []
    for b in sorted(blocks, key=lambda b: (str(b["file"]), b["line"])):
        f = Path(b["file"]).resolve()
        try:
            rel = f.relative_to(root).as_posix()
        except ValueError:
            rel = f.name
        per[rel] = per.get(rel, 0) + 1
        rows.append([rel, per[rel], sorted(b["flags"]), b["code"]])
    return hashlib.sha256(json.dumps(rows, ensure_ascii=False, separators=(",", ":")).encode("utf-8")).hexdigest()


def digest_for_dir(chapter_dir):
    files = sorted(Path(chapter_dir).rglob("*.md"))
    return source_digest([b for f in files for b in extract_blocks(f)], chapter_dir)


def make_stamp(results, info, root=None):
    n = lambda s: sum(1 for r in results if r["status"] == s)
    return {"schema": 1, "date": datetime.date.today().isoformat(), "status": info["status"],
            "jdk": info["jdk"], "release_requested": info["release_requested"], "release_effective": info["release_effective"],
            "blocks": len(results), "ok": n("ok"), "failed": n("fail"), "skipped": n("skipped"), "not_validated": n("not-validated"),
            "ran_with_assertions": sum(1 for r in results if r["status"] == "ok" and "run" in r["flags"]),
            "digest": digest_for_dir(root) if root else None}


def write_stamp(path, results, info, root=None):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(make_stamp(results, info, root), indent=1), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+", help="Markdown files or directories")
    ap.add_argument("--release", default="21", help="javac --release value (default 21)")
    ap.add_argument("--allow-missing-jdk", action="store_true")
    ap.add_argument("--workdir", help="scratch directory (default: $DSA_WORKDIR, system temp, then ./.dsa-scratch)")
    ap.add_argument("--stamp", help="write a JSON validation stamp to this path")
    a = ap.parse_args()
    files = []
    for p in map(Path, a.paths):
        files += sorted(p.rglob("*.md")) if p.is_dir() else [p]
    results, info = check_files(files, a.release, a.workdir)
    bad = [r for r in results if r["status"] == "fail"]
    for r in bad:
        print(f"FAIL {r['file']}:{r['line']}  {r['msg']}")
    n = lambda s: sum(1 for r in results if r["status"] == s)
    if info.get("jdk"):
        j = info["jdk"]
        print(f"jdk: {j['version']} ({j['vendor']}); release flag: {info['release_effective']}")
    print(f"java blocks: {len(results)}  ok={n('ok')}  fail={len(bad)}  skipped(nocompile)={n('skipped')}  not-validated={n('not-validated')}")
    if a.stamp:
        dirs = [Path(p) for p in a.paths if Path(p).is_dir()]
        write_stamp(a.stamp, results, info, dirs[0] if len(dirs) == 1 and len(a.paths) == 1 else None)
    if info["status"] == "not-validated":
        print("NOT VALIDATED: no JDK compiler was available. Label Java as unvalidated in the manuscript and report it.")
        sys.exit(0 if a.allow_missing_jdk else 2)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
