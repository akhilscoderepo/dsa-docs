import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from common import block, fill

CH = '31-range-query-structures-and-sweep-processing'
NAME = '91-sweep-ordered-state.md'

def brute_overload(trips, cap):
    for x in range(0, 60):
        if sum(p for p, a, b in trips if a <= x < b) > cap:
            return x
    return -1

def run_load(trips, cap):
    delta = {}
    for p, a, b in trips:
        delta[a] = delta.get(a, 0) + p
        delta[b] = delta.get(b, 0) - p
    keys = sorted(delta)
    load = 0
    steps = [{"at": {"i": -1}, "vars": {"load": 0, "change": 0},
              "note": "Nothing is applied yet. The load is 0."}]
    ans = -1
    for i, k in enumerate(keys):
        load += delta[k]
        over = load > cap
        note = f"Coordinate {k} carries the merged change {delta[k]:+d}. The load becomes {load}."
        if over:
            note += f" That exceeds the capacity {cap}, so the sweep returns {k} and stops."
        steps.append({"at": {"i": i}, "vars": {"load": load, "change": delta[k]}, "note": note})
        if over:
            ans = k
            break
    assert ans == brute_overload(trips, cap), (ans,)
    return keys, steps, ans

def brute_sky(bs):
    h = [max([b[2] for b in bs if b[0] <= x < b[1]], default=0) for x in range(60)]
    m = max(h); s = h.index(m); e = s
    while h[e] == m:
        e += 1
    return [m, s, e]

def run_sky(bs):
    ev = {}
    for l, r, h in bs:
        ev.setdefault(l, []).append((h, 1))
        ev.setdefault(r, []).append((h, -1))
    keys = sorted(ev)
    active = {}
    bestH, bestX, endX, open_ = 0, -1, -1, False
    steps = [{"at": {"i": -1}, "vars": {"height": 0, "bestH": 0, "bestX": -1, "endX": -1},
              "note": "No event is applied yet. The active multiset is empty."}]
    for i, k in enumerate(keys):
        for h, d in ev[k]:
            active[h] = active.get(h, 0) + d
            if active[h] == 0:
                del active[h]
        cur = max(active) if active else 0
        note = f"After the events at {k}, the active heights are {dict(sorted(active.items()))} and the height is {cur}."
        if cur > bestH:
            bestH, bestX, endX, open_ = cur, k, -1, True
            note += f" This is a new best, so best x is {k}."
        elif open_ and cur < bestH:
            endX, open_ = k, False
            note += f" The height is below the best, so end x is {k}."
        steps.append({"at": {"i": i}, "vars": {"height": cur, "bestH": bestH, "bestX": bestX, "endX": endX}, "note": note})
    res = [bestH, bestX, endX]
    assert res == brute_sky(bs), (res, brute_sky(bs))
    return keys, steps, res

k1, s1, a1 = run_load([(2, 1, 4), (1, 2, 6), (2, 4, 8), (3, 6, 9)], 4)
k2, s2, a2 = run_sky([(1, 6, 3), (4, 9, 5), (6, 8, 2), (8, 11, 5)])
assert a1 == 6 and a2 == [5, 4, 11], (a1, a2)
fill(CH, NAME, block(k1, ["i"], s1), "@@TRACE1@@")
fill(CH, NAME, block(k2, ["i"], s2), "@@TRACE2@@")
print(a1, a2)
