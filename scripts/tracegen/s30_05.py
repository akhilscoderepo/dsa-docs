import sys, pathlib, random
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from common import block, fill as _fill, ROOT
def fill(ch, name, text, ph):
    if ph in (ROOT / ch / name).read_text():
        _fill(ch, name, text, ph)

CH = '30-bits-number-theory-and-interview-numerics'
NAME = '05-subset-masks.md'

# ---------- algorithms and brute force oracles ----------
def count_mask(w, t):
    n = len(w)
    return sum(1 for m in range(1 << n) if sum(w[i] for i in range(n) if (m >> i) & 1) == t)

def count_brute(w, t):
    from itertools import combinations
    return sum(1 for r in range(len(w) + 1) for c in combinations(range(len(w)), r) if sum(w[i] for i in c) == t)

def submasks(m):
    out, s = [], m
    while True:
        out.append(s)
        if s == 0:
            break
        s = (s - 1) & m
    return out

def submasks_brute(m):
    return sorted((s for s in range(m + 1) if s & m == s), reverse=True)

def budget(b):
    n = 0
    while (n + 1) * (1 << (n + 1)) <= b:
        n += 1
    return n

def budget_brute(b):
    best = 0
    for n in range(0, 70):
        if n * 2 ** n <= b:
            best = n
    return best

def walk_bfs(adj, s):
    from collections import deque
    n = len(adj); full = (1 << n) - 1
    seen = {(s, 1 << s)}; dq = deque([(s, 1 << s, 0)])
    while dq:
        u, m, d = dq.popleft()
        if m == full:
            return d
        for v in adj[u]:
            st = (v, m | (1 << v))
            if st not in seen:
                seen.add(st); dq.append((st[0], st[1], d + 1))

def walk_brute(adj, s):
    n = len(adj)
    for L in range(0, 40):
        # iterate over all walks of length L by set of (node, visited-set) reachable states
        cur = {(s, frozenset([s]))}
        for _ in range(L):
            cur = {(v, vs | {v}) for u, vs in cur for v in adj[u]}
        if any(len(vs) == n for _, vs in cur):
            return L

def vary_lists(nums, m):
    return [[nums[i] for i in range(len(nums)) if (sub >> i) & 1] for sub in submasks(m)]

def vary_brute(nums, m):
    out = []
    for sub in range(m, -1, -1):
        if sub & m == sub:
            out.append([nums[i] for i in range(len(nums)) if (sub >> i) & 1])
    return out

def rand_graph(rng, n):
    edges = set()
    for v in range(1, n):
        edges.add((rng.randrange(v), v))
    for _ in range(rng.randint(0, n)):
        a, b = rng.randrange(n), rng.randrange(n)
        if a != b:
            edges.add((min(a, b), max(a, b)))
    adj = [[] for _ in range(n)]
    for a, b in sorted(edges):
        adj[a].append(b); adj[b].append(a)
    return adj

rng = random.Random(3005)
for _ in range(300):
    w = [rng.randint(-5, 5) for _ in range(rng.randint(0, 8))]
    t = rng.randint(-8, 8)
    assert count_mask(w, t) == count_brute(w, t)
    m = rng.randint(0, 255)
    assert submasks(m) == submasks_brute(m)
    b = rng.randint(1, 10 ** 6)
    assert budget(b) == budget_brute(b)
    nn = rng.randint(1, 6)
    nums = rng.sample(range(-20, 21), nn); mm = rng.randrange(1 << nn)
    assert vary_lists(nums, mm) == vary_brute(nums, mm)
for _ in range(150):
    nn = rng.randint(1, 6); adj = rand_graph(rng, nn); ss = rng.randrange(nn)
    assert walk_bfs(adj, ss) == walk_brute(adj, ss), (adj, ss)
assert budget(10 ** 18) == budget_brute(10 ** 18) == 54

# ---------- traces ----------
def trace_masks():
    items = ['a', 'b', 'c']
    cells = list(range(8))
    steps = [{"at": {"mask": -1}, "vars": {"size": 0},
              "note": "The counter has not started. The loop will visit the 8 masks from 0 to 7."}]
    for m in cells:
        inside = [items[i] for i in range(3) if (m >> i) & 1]
        bits = format(m, '03b')
        if inside:
            txt = f"Mask {m} is {bits} in binary. Its set bits select " + " and ".join(inside) + "."
        else:
            txt = f"Mask {m} is {bits} in binary. No bit is set, so this is the empty subset."
        if m == 7:
            txt += " This is the full mask, and the loop ends after it."
        steps.append({"at": {"mask": m}, "vars": {"size": len(inside)}, "note": txt})
    assert len({tuple(s["note"] for s in steps)}) == 1 and len(cells) == 2 ** 3
    return block(cells, ["mask"], steps)

def trace_sub():
    m = 11
    seq = submasks(m)
    assert seq == [11, 10, 9, 8, 3, 2, 1, 0] == submasks_brute(m)
    steps = [{"at": {"k": -1}, "vars": {"m": m}, "note": "The mask is 11, which is 1011 in binary. The loop starts with sub equal to 11."}]
    for k, s in enumerate(seq):
        if s == 0:
            txt = "The submask is 0, the empty subset. The loop processes it. The update (0 - 1) & 11 gives 11, which wraps back to the start, so the loop stops here."
            nxt = (s - 1) & m
            assert nxt == 11
        else:
            nxt = (s - 1) & m
            txt = f"The submask is {s}, which is {format(s, '04b')} in binary. The update (sub - 1) & 11 computes ({s} - 1) & 11 and gives {nxt}."
            if s - 1 != nxt:
                txt += f" The subtraction gives {s - 1}, and the AND clears the bits that 11 does not allow."
        steps.append({"at": {"k": k}, "vars": {"sub": s, "next": nxt}, "note": txt})
    return block(seq, ["k"], steps)

def fmt(v):
    import json
    return json.dumps(v, separators=(",", ":"))

ex = {}
w1 = [3, 1, 4, 2]; assert count_mask(w1, 5) == count_brute(w1, 5) == 2
w2 = [0, 2, -2]; assert count_mask(w2, 0) == count_brute(w2, 0) == 4
ex["@@EX_B1@@"] = f"Input `w = {fmt(w1)}` and `target = 5`, output 2, from the subsets at positions 0 and 3 (3 + 2) and at positions 1 and 2 (1 + 4)."
ex["@@EX_B2@@"] = f"Input `w = {fmt(w2)}` and `target = 0`, output 4, because the empty subset, the zero, the pair 2 and -2, and all three positions each sum to 0."

nv1 = [7, -2, 5]; assert vary_lists(nv1, 5) == vary_brute(nv1, 5) == [[7, 5], [5], [7], []]
ex["@@EX_V1@@"] = f"Input `nums = {fmt(nv1)}` and `m = 5`, which is 101 in binary, output {fmt(vary_lists(nv1, 5))}, from the submasks 5, 4, 1 and 0."
ex["@@EX_V2@@"] = "Input `nums = [4]` and `m = 0`, output `[[]]`, because the only submask is 0 and it selects no element."

assert budget(1000) == 7 and budget(10 ** 18) == 54 and (54 * 2 ** 54 <= 10 ** 18 < 55 * 2 ** 55)
ex["@@EX_O1@@"] = "Input `budget = 1000`, output 7, since 7 * 128 = 896 fits and 8 * 256 = 2,048 does not."
ex["@@EX_O2@@"] = "Input `budget = 1000000000000000000`, output 54. Here 55 * 2^55 is about 1.98 * 10^18, so the answer stops at 54, and a naive long product for larger `n` would overflow."

g1 = [[1, 2, 3], [0], [0], [0]]; assert walk_bfs(g1, 1) == walk_brute(g1, 1) == 4
g2 = [[]]; assert walk_bfs(g2, 0) == 0
ex["@@EX_R1@@"] = f"Input `graph = {fmt(g1)}` and `s = 1`, output 4, from the walk 1, 0, 2, 0, 3."
ex["@@EX_R2@@"] = "Input `graph = [[]]` and `s = 0`, output 0, because the start node is the only node and counts as visited."

fill(CH, NAME, trace_masks(), "@@TRACE1@@")
fill(CH, NAME, trace_sub(), "@@TRACE2@@")
for k, v in ex.items():
    fill(CH, NAME, v, k)
print("ok")
