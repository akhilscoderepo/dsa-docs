import sys, pathlib, random, json, itertools
from collections import deque, Counter
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from common import block, fill

CH = '30-bits-number-theory-and-interview-numerics'
NAME = '91-bits-with-search-state.md'

def subsets_by_size(nums):
    n = len(nums)
    ms = sorted(range(1 << n), key=lambda m: (bin(m).count("1"), m))
    return [[nums[i] for i in range(n) if m >> i & 1] for m in ms]

def subsets_brute(nums):
    out = []
    def rec(i, chosen):
        if i == len(nums):
            out.append(list(chosen)); return
        rec(i + 1, chosen)
        chosen.append(i); rec(i + 1, chosen); chosen.pop()
    rec(0, [])
    key = lambda c: (len(c), sum(1 << i for i in c))
    out.sort(key=key)
    return [[nums[i] for i in c] for c in out]

def repeated(s, k):
    code = {"A": 0, "C": 1, "G": 2, "T": 3}
    full = (1 << (2 * k)) - 1
    w = 0; cnt = {}; first = {}
    for i, ch in enumerate(s):
        w = ((w << 2) | code[ch]) & full
        if i >= k - 1:
            cnt[w] = cnt.get(w, 0) + 1
            first.setdefault(w, i - k + 1)
    return sorted({s[first[w]:first[w] + k] for w, c in cnt.items() if c >= 2})

def repeated_brute(s, k):
    c = Counter(s[i:i + k] for i in range(len(s) - k + 1))
    return sorted(w for w, v in c.items() if v >= 2)

def pair(words):
    ms = [sum(1 << (ord(c) - 97) for c in set(w)) for w in words]
    best, bi, bj = 0, -1, -1
    for i in range(len(words)):
        for j in range(i + 1, len(words)):
            if ms[i] & ms[j] == 0 and len(words[i]) * len(words[j]) > best:
                best, bi, bj = len(words[i]) * len(words[j]), i, j
    return [best, bi, bj]

def pair_brute(words):
    cand = [(len(a) * len(b), -i, -j) for i, a in enumerate(words) for j, b in enumerate(words)
            if i < j and not (set(a) & set(b))]
    if not cand: return [0, -1, -1]
    p, i, j = max(cand)
    return [p, -i, -j]

def bfs_levels(g, target=None):
    n = len(g); full = (1 << n) - 1
    dist = {}; q = deque()
    for s in range(n):
        dist[(s, 1 << s)] = 0; q.append((s, 1 << s))
    while q:
        node, mask = q.popleft()
        d = dist[(node, mask)]
        if mask == full and (target is None or node == target): return d, dist
        for nx in g[node]:
            ns = (nx, mask | 1 << nx)
            if ns not in dist: dist[ns] = d + 1; q.append(ns)
    return -1, dist

def walk_brute(g, t):
    n = len(g); INF = 10**9
    d = [[INF] * n for _ in range(n)]
    for i in range(n):
        d[i][i] = 0
        for j in g[i]: d[i][j] = 1
    for k in range(n):
        for i in range(n):
            for j in range(n):
                d[i][j] = min(d[i][j], d[i][k] + d[k][j])
    others = [x for x in range(n) if x != t]
    if not others: return 0
    best = INF
    for perm in itertools.permutations(others):
        order = list(perm) + [t]
        best = min(best, sum(d[order[i]][order[i + 1]] for i in range(len(order) - 1)))
    return best

def rand_graph(rng, n):
    adj = [set() for _ in range(n)]
    for v in range(1, n):
        u = rng.randrange(v); adj[u].add(v); adj[v].add(u)
    for _ in range(rng.randint(0, n)):
        u, v = rng.randrange(n), rng.randrange(n)
        if u != v: adj[u].add(v); adj[v].add(u)
    return [sorted(a) for a in adj]

rng = random.Random(3091)
for _ in range(300):
    nums = rng.sample(range(-20, 20), rng.randint(0, 6))
    assert subsets_by_size(nums) == subsets_brute(nums)
    s = "".join(rng.choice("ACGT") for _ in range(rng.randint(0, 25))); k = rng.randint(1, 5)
    assert repeated(s, k) == repeated_brute(s, k)
    words = ["".join(rng.choice("abcdef") for _ in range(rng.randint(1, 5))) for _ in range(rng.randint(0, 6))]
    assert pair(words) == pair_brute(words)
    n = rng.randint(1, 6); g = rand_graph(rng, n); t = rng.randrange(n)
    assert bfs_levels(g, t)[0] == walk_brute(g, t), (g, t)

def trace_bfs():
    g = [[1, 2], [0, 2], [0, 1, 3], [2]]
    n = 4; full = 15
    dist = {}; q = deque()
    for s in range(n): dist[(s, 1 << s)] = 0; q.append((s, 1 << s))
    levels = {0: 4}
    answer = None
    while q:
        node, mask = q.popleft(); d = dist[(node, mask)]
        if mask == full: answer = d; break
        for nx in g[node]:
            ns = (nx, mask | 1 << nx)
            if ns not in dist:
                dist[ns] = d + 1; q.append(ns); levels[d + 1] = levels.get(d + 1, 0) + 1
    assert answer == 3 == bfs_levels(g)[0]
    cells = [0, 1, 2, 3]
    steps = [{"at": {"d": -1}, "vars": {"seenStates": 0}, "note": "No state exists yet. There are 64 possible states in total."}]
    seen = 0
    for d in range(4):
        seen += levels[d] if d < 3 else sum(1 for v in dist.values() if v == 3)
        if d == 0:
            note = "Level 0 holds the 4 start states, one per node, each with only its own bit set."
        elif d < 3:
            note = f"Level {d} holds {levels[d]} new states, reached by one more corridor step. The distinct states seen so far number {seen}."
        else:
            note = f"Level 3 is reached after {seen} distinct states are queued. Popping a state with the full mask 15 ends the search, so the answer is 3."
        steps.append({"at": {"d": d}, "vars": {"levelSize": levels[d] if d < 3 else sum(1 for v in dist.values() if v == 3), "seenStates": seen}, "note": note})
    return block(cells, ["d"], steps)

def trace_dna():
    s, k = "ACGACGTACGT", 3
    code = {"A": 0, "C": 1, "G": 2, "T": 3}
    cells = [code[c] for c in s]
    full = 63; w = 0; cnt = {}
    steps = [{"at": {"i": -1}, "vars": {"window": 0}, "note": "No letter is read yet. The window mask is 0."}]
    for i, ch in enumerate(s):
        w = ((w << 2) | code[ch]) & full
        if i >= k - 1:
            text = s[i - k + 1:i + 1]
            cnt[w] = cnt.get(w, 0) + 1
            note = f"The window is {text} with mask {w}. " + (f"The mask has now occurred {cnt[w]} times, so {text} is a repeat." if cnt[w] >= 2 else "The mask is new.")
        else:
            note = f"The letter {ch} fills the window. Fewer than 3 letters are present, so no window is complete."
        steps.append({"at": {"i": i}, "vars": {"window": w}, "note": note})
    assert cnt[6] == 3 and repeated(s, k) == ["ACG", "CGT"] == repeated_brute(s, k)
    return block(cells, ["i"], steps)

def arr(v): return json.dumps(v, separators=(", ", ": "))
ex = {}
n1 = [5, 2, 9]; r = subsets_by_size(n1); assert r == subsets_brute(n1)
ex["@@EX_B1@@"] = f"Input `nums = {arr(n1)}`, output `{arr(r)}`, from the masks 0, 1, 2, 4, 3, 5, 6 and 7."
assert subsets_by_size([]) == [[]]
ex["@@EX_B2@@"] = "Input `nums = []`, output `[[]]`, because the only mask is 0, which is the empty subset."
s1, k1 = "CCGGTTCCGGTTCCGGA", 4
v1 = repeated(s1, k1); assert v1 == repeated_brute(s1, k1)
ex["@@EX_V1@@"] = f"Input `s = \"{s1}\"` and `k = 4`, output `{arr(v1)}`, where `CCGG` occurs three times with overlap."
s2 = "A" * 40; v2 = repeated(s2, 31); assert v2 == ["A" * 31] == repeated_brute(s2, 31)
ex["@@EX_V2@@"] = "Input `s` equal to 40 copies of `A` and `k = 31`, output a list with the single string of 31 copies of `A`. The window needs 62 bits, so an `int` mask fails."
w1 = ["abcd", "ab", "xyz", "mnopq", "cde"]; p1 = pair(w1); assert p1 == pair_brute(w1)
ex["@@EX_X1@@"] = f"Input `words = {arr(w1)}`, output `{arr(p1)}`, since `abcd` and `mnopq` share no letter."
w2 = ["a" * 100000, "b" * 100000]; assert pair(w2[:0] + ["aaa", "bbb"]) == [9, 0, 1]
ex["@@EX_X2@@"] = "Input two words, `a` repeated 100,000 times and `b` repeated 100,000 times, output `[10000000000, 0, 1]`. The product 10^10 exceeds the range of `int`."
w3 = ["ab", "ba", "ab"]; assert pair(w3) == [0, -1, -1]
g1 = [[1, 2], [0, 2], [0, 1, 3], [2]]
assert [bfs_levels(g1, t)[0] for t in range(4)] == [3, 3, 4, 3]
ex["@@EX_R1@@"] = "Input `graph = [[1,2],[0,2],[0,1,3],[2]]` and `t = 3`, output 3, from the walk 0, 1, 2, 3. The same graph with `t = 2` gives 4."
g2 = [[]]; assert bfs_levels(g2, 0)[0] == 0
g3 = [[1], [0, 2], [1, 3], [2]]; assert [bfs_levels(g3, t)[0] for t in range(4)] == [3, 4, 4, 3]
ex["@@EX_R2@@"] = "Input `graph = [[1],[0,2],[1,3],[2]]` and `t = 1`, output 4, from the walk 3, 2, 1, 0, 1. A one-node graph `[[]]` with `t = 0` gives 0."

fill(CH, NAME, trace_bfs(), "@@TRACE1@@")
fill(CH, NAME, trace_dna(), "@@TRACE2@@")
for k_, v in ex.items(): fill(CH, NAME, v, k_)
print("ok")
