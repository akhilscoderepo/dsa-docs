import sys, pathlib, random, heapq
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from common import block, fill

CH = '31-range-query-structures-and-sweep-processing'
NAME = '05-sweep-events.md'

# ---------- algorithms and brute force oracles ----------
def car_sweep(trips, cap):
    ev = []
    for p, a, b in trips:
        ev.append((a, p)); ev.append((b, -p))
    ev.sort()
    load = 0
    for _, d in ev:
        load += d
        if load > cap:
            return False
    return True

def car_brute(trips, cap):
    load = {}
    for p, a, b in trips:
        for x in range(a, b):
            load[x] = load.get(x, 0) + p
    return all(v <= cap for v in load.values())

def merge_sweep(iv):
    ev = {}
    for a, b in iv:
        ev[a] = ev.get(a, 0) + 1
        ev[b] = ev.get(b, 0) - 1
    out, cnt, start = [], 0, None
    for x in sorted(ev):
        was = cnt
        cnt += ev[x]
        if was == 0 and cnt > 0:
            start = x
        elif was > 0 and cnt == 0:
            out.append([start, x])
    return out

def merge_brute(iv):
    cov = sorted({x for a, b in iv for x in range(a, b)})
    out = []
    for x in cov:
        if out and out[-1][1] == x:
            out[-1][1] = x + 1
        else:
            out.append([x, x + 1])
    return out

def tie_sweep(iv, closed):
    ev = sorted((a, 1 if closed else 1) for a, b in iv)
    ev = []
    for a, b in iv:
        ev.append((a, 1)); ev.append((b, -1))
    ev.sort(key=lambda e: (e[0], -e[1] if closed else e[1]))
    best = cur = 0
    for _, d in ev:
        cur += d
        best = max(best, cur)
    return best

def tie_brute(iv, closed):
    lo = min(a for a, b in iv); hi = max(b for a, b in iv)
    best = 0
    for x in range(lo, hi + 1):
        c = sum(1 for a, b in iv if a <= x and (x <= b if closed else x < b))
        best = max(best, c)
    return best

def sky_sweep(bs):
    ev = []
    for l, r, h in bs:
        ev.append((l, h)); ev.append((r, -h))
    ev.sort(key=lambda e: e[0])
    heap = [0]; pending = {}
    prev = 0; i = 0; out = []
    while i < len(ev):
        x = ev[i][0]
        while i < len(ev) and ev[i][0] == x:
            h = ev[i][1]; i += 1
            if h > 0: heapq.heappush(heap, -h)
            else: pending[-h] = pending.get(-h, 0) + 1
        while pending.get(-heap[0], 0) > 0:
            v = -heapq.heappop(heap); pending[v] -= 1
        top = -heap[0]
        if top != prev:
            out.append([x, top]); prev = top
    return out

def sky_brute(bs):
    if not bs: return []
    out = []; prev = 0
    for x in range(0, max(r for _, r, _ in bs) + 1):
        h = max([hh for l, r, hh in bs if l <= x < r], default=0)
        if h != prev:
            out.append([x, h]); prev = h
    return out

rng = random.Random(3105)
for _ in range(400):
    n = rng.randint(1, 6)
    trips = []
    for _ in range(n):
        a = rng.randint(0, 9); b = rng.randint(a + 1, 10)
        trips.append((rng.randint(1, 4), a, b))
    cap = rng.randint(1, 9)
    assert car_sweep(trips, cap) == car_brute(trips, cap)
    iv = []
    for _ in range(rng.randint(0, 6)):
        a = rng.randint(-5, 8); iv.append((a, rng.randint(a + 1, 9)))
    assert merge_sweep(iv) == merge_brute(iv), iv
    if iv:
        for c in (True, False):
            assert tie_sweep(iv, c) == tie_brute(iv, c), (iv, c)
    bs = []
    for _ in range(rng.randint(0, 6)):
        l = rng.randint(0, 9); bs.append((l, rng.randint(l + 1, 10), rng.randint(1, 5)))
    assert sky_sweep(bs) == sky_brute(bs), bs

# ---------- traces ----------
def trace_car():
    trips, cap = [(2, 1, 5), (1, 3, 6), (3, 5, 8)], 4
    ev = []
    for p, a, b in trips:
        ev.append((a, p)); ev.append((b, -p))
    ev.sort()
    cells = [e[0] for e in ev]
    steps = [{"at": {"e": -1}, "vars": {"load": 0, "capacity": cap},
              "note": "No event is applied yet, so the load is 0 and the capacity is 4."}]
    load = 0
    for i, (x, d) in enumerate(ev):
        load += d
        assert load <= cap
        kind = "pickup" if d > 0 else "drop-off"
        extra = ""
        if i > 0 and ev[i - 1][0] == x:
            extra = " This event shares its coordinate with the previous one, and the decrease ran first."
        elif i + 1 < len(ev) and ev[i + 1][0] == x:
            extra = " Another event waits at the same coordinate, and this decrease runs first."
        steps.append({"at": {"e": i}, "vars": {"load": load, "capacity": cap},
                      "note": f"Coordinate {x} applies a {kind} of {abs(d)}. The load is now {load}, which is at most {cap}.{extra}"})
    assert car_sweep(trips, cap) is True and car_brute(trips, cap) is True
    assert max(1, 0) and not car_sweep([(2, 1, 5), (1, 3, 6), (3, 5, 8)], 3)
    return block(cells, ["e"], steps)

def trace_sky():
    bs = [(2, 6, 3), (4, 6, 5), (6, 9, 2)]
    ev = []
    for l, r, h in bs:
        ev.append((l, h)); ev.append((r, -h))
    ev.sort(key=lambda e: e[0])
    xs = sorted({e[0] for e in ev})
    heap = [0]; pending = {}; prev = 0; out = []
    steps = [{"at": {"x": -1}, "vars": {"maxHeight": 0, "pendingRemovals": 0},
              "note": "The heap holds only the ground height 0, and no removal is pending."}]
    for xi, x in enumerate(xs):
        starts = [h for xx, h in ev if xx == x and h > 0]
        ends = [-h for xx, h in ev if xx == x and h < 0]
        for h in starts: heapq.heappush(heap, -h)
        for h in ends: pending[h] = pending.get(h, 0) + 1
        popped = []
        while pending.get(-heap[0], 0) > 0:
            v = -heapq.heappop(heap); pending[v] -= 1; popped.append(v)
        top = -heap[0]
        changed = top != prev
        if changed: out.append([x, top]); prev = top
        npend = sum(pending.values())
        txt = f"Coordinate {x} adds heights {starts or 'none'} and ends heights {ends or 'none'}."
        if popped: txt += f" The top values {popped} are pending removals, so they leave the heap."
        txt += f" The maximum is {top}, " + (f"so the outline gets the key point ({x},{top})." if changed else "which is unchanged.")
        steps.append({"at": {"x": xi}, "vars": {"maxHeight": top, "pendingRemovals": npend}, "note": txt})
    assert out == sky_brute(bs) == [[2, 3], [4, 5], [6, 2], [9, 0]], out
    return block(xs, ["x"], steps)

def fmt(v):
    import json
    return json.dumps(v, separators=(",", ":")).replace("true", "true").replace("false", "false")

ex = {}
t1 = [[2, 1, 5], [3, 3, 7]]; assert car_sweep(t1, 4) is False and car_brute(t1, 4) is False
t2 = [[2, 1, 5], [3, 5, 7]]; assert car_sweep(t2, 3) is True and car_brute(t2, 3) is True
ex["@@EX_B1@@"] = f"Input trips {fmt(t1)} and capacity 4, output `false`, because positions 3 and 4 carry 2 + 3 = 5 passengers."
ex["@@EX_B2@@"] = f"Input trips {fmt(t2)} and capacity 3, output `true`, because the 2 passengers leave at 5 as the 3 passengers board."

v1 = [[1, 3], [3, 5], [7, 9]]; assert merge_sweep(v1) == merge_brute(v1) == [[1, 5], [7, 9]]
v2 = [[4, 6], [1, 2], [3, 4]]; assert merge_sweep(v2) == merge_brute(v2) == [[1, 2], [3, 6]]
ex["@@EX_V1@@"] = f"Input {fmt(v1)}, output {fmt(merge_sweep(v1))}, because `[1,3)` and `[3,5)` touch at 3 and form one span."
ex["@@EX_V2@@"] = f"Input {fmt(v2)}, output {fmt(merge_sweep(v2))}, because position 2 is uncovered and separates the first two spans."

i1 = [[1, 3], [3, 5]]; assert (tie_sweep(i1, True), tie_sweep(i1, False)) == (2, 1) == (tie_brute(i1, True), tie_brute(i1, False))
i2 = [[1, 4], [2, 6], [4, 8]]; assert (tie_sweep(i2, True), tie_sweep(i2, False)) == (3, 2) == (tie_brute(i2, True), tie_brute(i2, False))
ex["@@EX_T1@@"] = f"Input {fmt(i1)}, output 2 when `closed` is true and 1 when `closed` is false, because position 3 belongs to both intervals only in the closed case."
ex["@@EX_T2@@"] = f"Input {fmt(i2)}, output 3 when `closed` is true and 2 when `closed` is false, because the first interval contains position 4 only in the closed case."

s1 = [[2, 6, 3], [4, 6, 5], [6, 9, 2]]; assert sky_sweep(s1) == sky_brute(s1) == [[2, 3], [4, 5], [6, 2], [9, 0]]
s2 = [[0, 3, 4], [2, 5, 4]]; assert sky_sweep(s2) == sky_brute(s2) == [[0, 4], [5, 0]]
ex["@@EX_R1@@"] = f"Input {fmt(s1)}, output {fmt(sky_sweep(s1))}, because the shared edge at 6 changes the maximum from 5 to 2."
ex["@@EX_R2@@"] = f"Input {fmt(s2)}, output {fmt(sky_sweep(s2))}, because the two buildings of height 4 overlap and produce no key point at 3."

fill(CH, NAME, trace_car(), "@@TRACE1@@")
fill(CH, NAME, trace_sky(), "@@TRACE2@@")
for k, v in ex.items():
    fill(CH, NAME, v, k)
print("ok")
