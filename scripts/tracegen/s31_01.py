import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from common import block, fill

CH = '31-range-query-structures-and-sweep-processing'
VALS = [3, 1, 4, 1, 5, 9, 2, 6]

def build(vals):
    n = len(vals)
    t = [0] * (n + 1)
    for p, v in enumerate(vals):
        i = p + 1
        while i <= n:
            t[i] += v
            i += i & -i
    return t

def run_update(vals, pos, delta):
    t = build(vals)
    n = len(vals)
    cells = list(t)
    steps = [{"at": {"i": -1}, "vars": {"pos": pos, "delta": delta},
              "note": f"The call converts position {pos} to internal index {pos + 1}. No entry has changed yet."}]
    i = pos + 1
    while i <= n:
        low = i & -i
        t[i] += delta
        steps.append({"at": {"i": i}, "vars": {"lowBit": low, "newValue": t[i]},
                      "note": f"Index {i} has low bit {low}, so its block covers positions {i - low + 1} to {i}. The entry becomes {t[i]}."})
        i += low
    steps.append({"at": {"i": n + 1}, "vars": {"lowBit": i & -i, "newValue": 0},
                  "note": f"The next index is {i}, which is past the last slot {n}, so the pointer rests beyond the array. The loop stops."})
    nv = list(vals); nv[pos] += delta
    assert t == build(nv), (t, build(nv))
    return cells, steps, nv, t

def run_prefix(t, k, vals):
    cells = list(t)
    steps = [{"at": {"i": k}, "vars": {"sum": 0},
              "note": f"The query starts at index {k} with a running sum of 0."}]
    s = 0; i = k
    while i > 0:
        low = i & -i
        s += t[i]
        steps.append({"at": {"i": i}, "vars": {"lowBit": low, "sum": s},
                      "note": f"The entry at index {i} covers positions {i - low + 1} to {i} and adds {t[i]}. The running sum is {s}."})
        i -= low
    steps.append({"at": {"i": 0}, "vars": {"lowBit": 0, "sum": s},
                  "note": f"The index reaches 0, so the loop stops with the answer {s}."})
    assert s == sum(vals[:k]), (s, sum(vals[:k]))
    return cells, steps, s

cells1, steps1, nv, t2 = run_update(VALS, 2, 10)
cells2, steps2, ans = run_prefix(t2, 6, nv)
assert build(VALS) == [0, 3, 4, 4, 9, 5, 14, 2, 31]
assert ans == 33
t = pathlib.Path(__file__).resolve().parents[2] / 'dsa-skills' / 'manuscripts' / CH / '01-fenwick-trees.md'
fill(CH, '01-fenwick-trees.md', block(cells1, ["i"], steps1), "@@TRACE1@@")
fill(CH, '01-fenwick-trees.md', block(cells2, ["i"], steps2), "@@TRACE2@@")
print(ans)
