import sys, pathlib, bisect
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from common import block, fill

CH = '31-range-query-structures-and-sweep-processing'
F = '04-coordinate-compression.md'

def run1(vals):
    table = sorted(set(vals))
    steps = [{"at": {"i": -1}, "vars": {"m": len(table)},
              "note": f"Sorting and removing duplicates gives the table {table} with {len(table)} distinct values."}]
    out = []
    for i, v in enumerate(vals):
        pos = bisect.bisect_left(table, v)
        assert table[pos] == v
        r = pos + 1
        out.append(r)
        steps.append({"at": {"i": i}, "vars": {"value": v, "position": pos, "rank": r},
                      "note": f"The value {v} sits at table position {pos}, so its rank is {r}."})
    assert out == [sorted(set(vals)).index(v) + 1 for v in vals]
    return steps, out

def run2(ins):
    table = sorted(set(ins))
    m = len(table)
    tree = [0] * (m + 1)
    def add(pos):
        i = pos + 1
        while i <= m:
            tree[i] += 1
            i += i & -i
    def prefix(p):
        s = 0
        while p > 0:
            s += tree[p]
            p -= p & -p
        return s
    steps = [{"at": {"i": -1}, "vars": {"m": m, "total": 0},
              "note": f"The table is {table}, so the tree has {m} positions and starts empty."}]
    total = 0
    for i, v in enumerate(ins):
        r = bisect.bisect_left(table, v) + 1
        less = prefix(r - 1)
        greater = i - prefix(r)
        c = min(less, greater)
        total += c
        add(r - 1)
        steps.append({"at": {"i": i}, "vars": {"rank": r, "less": less, "greater": greater, "cost": c, "total": total},
                      "note": f"The value {v} has rank {r}. {less} earlier values are below it and {greater} are above it, so the cost is {c} and the total is {total}."})
    brute = 0
    for i, v in enumerate(ins):
        brute += min(sum(1 for y in ins[:i] if y < v), sum(1 for y in ins[:i] if y > v))
    assert brute == total, (brute, total)
    return steps, total

s1, r1 = run1([900, -5, 1000000000, 900, 42, -5, 7])
assert r1 == [4, 1, 5, 4, 3, 1, 2]
s2, t2 = run2([8, 2, 5, 5, 9, 1, 5])
assert t2 == 4
assert run2([4, 9, 4, 1, 7, 7])[1] == 2 and run2([3, 3, 3, 3])[1] == 0
fill(CH, F, block([900, -5, 1000000000, 900, 42, -5, 7], ["i"], s1), "@@TRACE1@@")
fill(CH, F, block([8, 2, 5, 5, 9, 1, 5], ["i"], s2), "@@TRACE2@@")
print(r1, t2)
