from common import *
from collections import deque
CH = '23-directed-graphs-and-union-find'; F = '91-merge-groups-as-edges-arrive.md'

class G:
    def __init__(s, n): s.p = list(range(n)); s.sz = [1] * n; s.count = n; s.largest = 1
    def find(s, x):
        while s.p[x] != x:
            s.p[x] = s.p[s.p[x]]; x = s.p[x]
        return x
    def union(s, a, b):
        ra, rb = s.find(a), s.find(b)
        if ra == rb: return False
        if s.sz[ra] < s.sz[rb]: ra, rb = rb, ra
        s.p[rb] = ra; s.sz[ra] += s.sz[rb]; s.largest = max(s.largest, s.sz[ra]); s.count -= 1
        return True

# Trace 1: six events on six vertices.
n = 6; events = [(0, 1), (2, 3), (1, 3), (0, 2), (4, 5), (5, 4)]
g = G(n); closing = []
st = [{"at": {"u": -1, "v": -1}, "vars": {"count": "6", "largest": "1", "closing": "[]", "parent": str(g.p)},
       "note": "Start: six groups of one vertex, so count = 6 and largest = 1."}]
for i, (u, v) in enumerate(events):
    ru, rv = g.find(u), g.find(v)
    ok = g.union(u, v)
    if ok:
        note = f"Event {i} pairs {u} and {v}. The representatives {ru} and {rv} differ, so the groups merge and count becomes {g.count}."
    else:
        closing.append(i)
        note = f"Event {i} pairs {u} and {v}. Both have representative {ru}, so the event is a closing edge and nothing changes."
    st.append({"at": {"u": u, "v": v}, "vars": {"count": str(g.count), "largest": str(g.largest), "closing": str(closing), "parent": str(g.p)}, "note": note})
assert (g.count, g.largest, closing) == (2, 4, [3, 5])
# brute-force check: component sizes by search over all events
adj = {i: [] for i in range(n)}
for u, v in events: adj[u].append(v); adj[v].append(u)
seen = set(); sizes = []
for s0 in range(n):
    if s0 in seen: continue
    q = deque([s0]); seen.add(s0); c = 0
    while q:
        x = q.popleft(); c += 1
        for y in adj[x]:
            if y not in seen: seen.add(y); q.append(y)
    sizes.append(c)
assert (len(sizes), max(sizes)) == (2, 4)
fill(CH, F, block(list(range(n)), ["u", "v"], st), "@@TRACE1@@")

# Trace 2: four accounts merged by lowercase email.
accts = [["Ana", "A@x.io", "b@x.io"], ["Bo", "B@X.io", "c@x.io"], ["Cy", "d@x.io"], ["Dee", "C@X.IO", "e@x.io"]]
g = G(4); owner = {}
def show(o): return "{" + ", ".join(f"{k}:{v}" for k, v in o.items()) + "}"
st = [{"at": {"acct": -1}, "vars": {"owner": "{}", "parent": str(g.p)}, "note": "Start: four accounts, each its own group, and no address has an owner."}]
for i, a in enumerate(accts):
    msgs = []
    for e in a[1:]:
        k = e.lower()
        if k in owner:
            ro = owner[k]; was = g.find(i) != g.find(ro); g.union(i, ro)
            msgs.append(f"{k} is owned by account {ro}, so accounts {i} and {ro} merge" if was else f"{k} is owned by account {ro}, which already shares its group")
        else:
            owner[k] = i; msgs.append(f"{k} gets owner {i}")
    st.append({"at": {"acct": i}, "vars": {"owner": show(owner), "parent": str(g.p)}, "note": f"Account {i}: " + "; ".join(msgs) + "."})
groups = {}
for i in range(4): groups.setdefault(g.find(i), []).append(i)
final = sorted(groups.values())
assert final == [[0, 1, 3], [2]], final
st.append({"at": {"acct": 3}, "vars": {"owner": show(owner), "parent": str(g.p)}, "note": "Grouping by final root gives {0, 1, 3} and {2}. The name of each group comes from its smallest account position, so the groups are named Ana and Cy."})
fill(CH, F, block([0, 1, 2, 3], ["acct"], st), "@@TRACE2@@")
print("ok")
