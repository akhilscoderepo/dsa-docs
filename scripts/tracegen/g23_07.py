from common import *
CH = '23-directed-graphs-and-union-find'; F = '07-kruskal-foundations.md'

def find(p, x):
    while p[x] != x:
        p[x] = p[p[x]]; x = p[x]
    return x

def run(n, edges):
    order = sorted(range(len(edges)), key=lambda k: (edges[k][2], k))
    ws = [edges[k][2] for k in order]
    parent = list(range(n)); size = [1] * n; acc = 0; total = 0
    st = [{"at": {"i": -1}, "vars": {"accepted": "0", "total": "0", "parent": str(parent)},
           "note": f"Start: {n} separate groups. The edges are sorted by weight and the loop needs {n - 1} acceptances."}]
    for i, k in enumerate(order):
        if acc == n - 1:
            break
        u, v, w = edges[k]
        ru, rv = find(parent, u), find(parent, v)
        if ru == rv:
            note = f"Edge {u}-{v} with weight {w}: find returns {ru} for both ends, so the edge is skipped."
        else:
            if size[ru] < size[rv]: ru, rv = rv, ru
            parent[rv] = ru; size[ru] += size[rv]; acc += 1; total += w
            note = f"Edge {u}-{v} with weight {w}: the representatives {rv} and {ru} differ, so the edge is accepted and the groups merge."
        st.append({"at": {"i": i}, "vars": {"accepted": str(acc), "total": str(total), "parent": str(parent)}, "note": note})
    return ws, st, acc, total, i

# Trace 1: connected graph, loop stops after V - 1 acceptances before the list ends.
E1 = [(0, 1, 4), (0, 2, 3), (1, 2, 1), (1, 3, 2), (2, 3, 2), (3, 4, 3), (3, 5, 6), (4, 5, 3), (2, 4, 5)]
ws, st, acc, total, last = run(6, E1)
assert acc == 5 and last < len(E1) - 1
st.append({"at": {"i": last}, "vars": {"accepted": str(acc), "total": str(total), "parent": st[-1]["vars"]["parent"]},
           "note": f"accepted equals {acc}, which is V - 1, so the loop stops. The {len(E1) - last} later edges are never examined, and the total is {total}."})
# cross-check with a brute-force minimum over all 5-edge subsets
import itertools
def conn(n, sub):
    p = list(range(n))
    for k in sub:
        a, b = find(p, E1[k][0]), find(p, E1[k][1])
        if a == b: return False
        p[a] = b
    return True
best = min(sum(E1[k][2] for k in s) for s in itertools.combinations(range(len(E1)), 5) if conn(6, s))
assert best == total, (best, total)
fill(CH, F, block(ws, ["i"], st), "@@TRACE1@@")

# Trace 2: two triangles, so the loop examines every edge and ends below V - 1.
E2 = [(0, 1, 2), (1, 2, 1), (0, 2, 3), (3, 4, 4), (4, 5, 1), (3, 5, 2)]
ws, st, acc, total, last = run(6, E2)
assert acc == 4 and last == len(E2) - 1
st.append({"at": {"i": len(E2)}, "vars": {"accepted": str(acc), "total": str(total), "parent": st[-1]["vars"]["parent"]},
           "note": f"The list is exhausted with accepted = {acc}, which is below V - 1 = 5, so the method returns -1."})
fill(CH, F, block(ws, ["i"], st), "@@TRACE2@@")
print("ok")
