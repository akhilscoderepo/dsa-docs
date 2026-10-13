from common import *
import itertools
CH = '29-dynamic-programming-intervals-and-advanced-states'

def brute(v):
    best = -1
    for perm in itertools.permutations(range(len(v))):
        alive = list(range(len(v) + 2)); cur = [1] + list(v) + [1]; s = 0
        for p in perm:
            pos = p + 1
            L = max(q for q in alive if q < pos); R = min(q for q in alive if q > pos)
            s += cur[L] * cur[R]; alive.remove(pos)
        best = max(best, s)
    return best

def run(v, ph, expect):
    a = [1] + list(v) + [1]; m = len(a)
    dp = [[0] * m for _ in range(m)]
    cells = []; order = []
    for gap in range(2, m):
        for l in range(0, m - gap):
            order.append((l, gap + l)); cells.append(f"({l},{gap + l})")
    steps = [{"at": {"cell": -1}, "vars": {"values": str(a)}, "note": "Positions 0 and %d hold the outside value 1. Every interval with no item strictly inside starts at 0." % (m - 1)}]
    for idx, (l, r) in enumerate(order):
        best = None
        for k in range(l + 1, r):
            val = a[l] * a[r] + dp[l][k] + dp[k][r]
            if best is None or val > best[0]: best = (val, k)
        dp[l][r] = best[0]; k = best[1]
        pair = a[l] * a[r]
        steps.append({"at": {"cell": idx}, "vars": {"l": l, "r": r, "last": k, "pair": pair, "left": dp[l][k], "right": dp[k][r], "dp": best[0]},
                      "note": f"Interval ({l},{r}) keeps the values {a[l]} and {a[r]} until the end. The best last removal is position {k}, so the entry is {pair} plus {dp[l][k]} plus {dp[k][r]}, which is {best[0]}."})
    assert dp[0][m - 1] == expect == brute(v)
    fill(CH, '91-dp-advanced-state.md', block(cells, ["cell"], steps), ph)

run([4, 9, 3, 1], "@@TRACE1@@", 28)
run([6, 2, 5], "@@TRACE2@@", None if False else brute([6, 2, 5]))
