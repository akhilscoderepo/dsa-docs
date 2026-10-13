import sys, pathlib, bisect
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from common import block, fill

CH = '31-range-query-structures-and-sweep-processing'
NAME = '92-compress-then-count.md'

def brute(vals):
    return [sum(1 for j in range(i) if vals[j] < vals[i]) for i in range(len(vals))]

def run(vals):
    keys = sorted(set(vals))
    m = len(keys)
    tree = [0] * (m + 1)
    counts = [0] * m
    def add(p):
        while p <= m:
            tree[p] += 1
            p += p & -p
    def prefix(p):
        s = 0
        while p > 0:
            s += tree[p]
            p -= p & -p
        return s
    steps = [{"at": {"i": -1}, "vars": {"keys": str(keys), "counts": str(counts), "total": 0},
              "note": f"Compression gives the keys {keys}. The tree starts empty, so every count is 0."}]
    out = []
    total = 0
    for i, v in enumerate(vals):
        rank = bisect.bisect_left(keys, v) + 1
        smaller = prefix(rank - 1)
        add(rank)
        counts[rank - 1] += 1
        out.append(smaller)
        total += smaller
        steps.append({"at": {"i": i},
                      "vars": {"value": v, "rank": rank, "smaller": smaller, "counts": str(counts), "total": total},
                      "note": f"Step {i + 1} reads {v}, which has rank {rank}. The query over ranks below {rank} returns {smaller}, so the running total becomes {total}. Rank {rank} then holds {counts[rank - 1]} reading(s)."})
    assert out == brute(vals), (vals, out)
    return out, steps

t = pathlib.Path(__file__).resolve().parents[2] / 'dsa-skills' / 'manuscripts' / CH / NAME
res = {}
for ph, vals in (("@@TRACE1@@", [30, -5, 30, 1000000, -5, 7]), ("@@TRACE2@@", [9, 2000000000, -3, 9, 2000000000, 0, -3])):
    out, steps = run(vals)
    res[ph] = out
    fill(CH, NAME, block(vals, ["i"], steps), ph)
assert res == {"@@TRACE1@@": [0, 0, 1, 3, 0, 2], "@@TRACE2@@": [0, 1, 0, 1, 3, 1, 0]}
print(res)
