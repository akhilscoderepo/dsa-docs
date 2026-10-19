from common import *
CH = '39-dynamic-query-structures'
F = '92-preprocessed-query-apis.md'

# Trace 1: jump table queries on a 12-node tree.
PAR = [-1, 0, 1, 2, 3, 4, 5, 6, 2, 8, 9, 10]
N = len(PAR)
ROWS = 4
up = [PAR[:]]
for j in range(1, ROWS):
    up.append([-1 if up[j-1][v] == -1 else up[j-1][up[j-1][v]] for v in range(N)])

def walk(node, k):
    for _ in range(k):
        if node == -1:
            break
        node = PAR[node]
    return node

def query(node, k, st):
    start, cur = node, node
    st.append({"at": {"node": cur}, "vars": {"query": f"kth({start},{k})", "bit": "-", "left": k, "result": "start"},
               "note": f"Query kth({start}, {k}). The binary form of {k} is {k:b}, so the loop reads {bin(k).count('1')} set bits."})
    j = 0
    while k >> j and cur != -1:
        if k >> j & 1:
            nxt = up[j][cur]
            rest = k >> (j + 1) << (j + 1)
            where = f"node {nxt}" if nxt != -1 else "outside the tree"
            st.append({"at": {"node": nxt}, "vars": {"query": f"kth({start},{k})", "bit": j, "left": rest, "result": "pending"},
                       "note": f"Bit {j} is set, so one read of the table row {j} moves the node {2**j} steps up, to {where}."})
            cur = nxt
        else:
            pass
        j += 1
    assert cur == walk(start, k), (start, k, cur)
    st[-1]["vars"]["result"] = cur
    st[-1]["note"] += f" No bits remain, so the answer is {cur}."
    return cur

st = []
assert query(11, 5, st) == 1
assert query(6, 9, st) == -1
# make the miss explicit
fill(CH, F, block([str(i) for i in range(N)], ["node"], st), "@@TRACE1@@")

# Trace 2: growing graph with stale flag; tiny model with brute force path max.
n = 4
edges = [(0, 1, 5)]
def msf_summary(es):
    d = list(range(n))
    def f(x):
        while d[x] != x:
            d[x] = d[d[x]]; x = d[x]
        return x
    comps, tot = n, 0
    for u, v, w in sorted(es, key=lambda e: e[2]):
        a, b = f(u), f(v)
        if a != b:
            d[a] = b; comps -= 1; tot += w
    return comps, tot
def reach(es, p, q, lim):
    d = list(range(n))
    def f(x):
        while d[x] != x:
            d[x] = d[d[x]]; x = d[x]
        return x
    for u, v, w in es:
        if w < lim:
            d[f(u)] = f(v)
    return f(p) == f(q)
stale = False; rb = 0
st = [{"at": {"p": 0, "q": 1}, "vars": {"call": "new(4,[0-1:5])", "result": "none", "stale": "false", "rebuilds": 0},
       "note": "The constructor builds the index once. That build is not counted, so rebuilds starts at 0."}]
ops = [('a', 2, 3, 7), ('q', 0, 1, 6), ('a', 0, 1, 9), ('a', 1, 2, 2), ('a', 0, 1, 3), ('q', 0, 2, 4), ('q', 2, 3, 7), ('q', 2, 3, 8)]
res = []
for o in ops:
    if o[0] == 'a':
        _, u, v, w = o
        before = msf_summary(edges); edges.append((u, v, w)); after = msf_summary(edges)
        if stale:
            note = f"addEdge({u},{v},{w}) only stores the edge, because the index is already stale and the next query rebuilds."
        elif before != after:
            stale = True
            note = f"addEdge({u},{v},{w}) joins two trees or beats the heaviest edge on the tree path, so the index becomes stale."
        else:
            note = f"addEdge({u},{v},{w}) is not lighter than the tree path between its ends, so the index stays fresh."
        st.append({"at": {"p": u, "q": v}, "vars": {"call": f"add({u},{v},{w})", "result": "none", "stale": str(stale).lower(), "rebuilds": rb}, "note": note})
    else:
        _, p, q, lim = o
        pre = ""
        if stale:
            stale = False; rb += 1
            pre = "The index is stale, so this query rebuilds it first. "
        r = reach(edges, p, q, lim); res.append(r)
        st.append({"at": {"p": p, "q": q}, "vars": {"call": f"query({p},{q},{lim})", "result": str(r).lower(), "stale": "false", "rebuilds": rb},
                   "note": pre + f"query({p},{q},{lim}) asks for a path with every edge below {lim} and returns {str(r).lower()}."})
assert res == [True, True, False, True]
print(res, rb)
fill(CH, F, block([str(i) for i in range(n)], ["p", "q"], st), "@@TRACE2@@")
