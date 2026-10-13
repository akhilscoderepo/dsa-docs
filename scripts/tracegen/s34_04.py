from common import *
CH = '34-advanced-strings'; F = '04-suffix-structures.md'

# Trace 1: prefix doubling on "banana".
s = "banana"; n = len(s)
rank = [ord(c) for c in s]; order = list(range(n)); k = 1; st = []
st.append({"at": {"first": -1, "last": -1}, "vars": {"k": 0, "rank": "[98,97,110,97,110,97]"},
           "note": "Before any round the rank of each suffix is the code of its first character."})
while True:
    key = lambda i: (rank[i], rank[i + k] if i + k < n else -1)
    order.sort(key=key)
    nr = [0] * n
    for t in range(1, n):
        nr[order[t]] = nr[order[t - 1]] + (1 if key(order[t - 1]) < key(order[t]) else 0)
    rank = nr
    done = rank[order[-1]] == n - 1
    st.append({"at": {"first": order[0], "last": order[-1]},
               "vars": {"k": k, "rank": json.dumps(rank, separators=(",", ":")), "order": json.dumps(order, separators=(",", ":"))},
               "note": f"Round with k = {k} sorts by pairs of ranks, so it orders by {2*k} characters." + (" All ranks are distinct, so the loop stops." if done else " Ties remain, so another round follows.")})
    if done: break
    k *= 2
assert order == [5, 3, 1, 0, 4, 2] and len(st) == 3
fill(CH, F, block(list(s), ["first", "last"], st), "@@TRACE1@@")

# Trace 2: Kasai pass on "banana".
sa = order; rk = [0] * n
for r, v in enumerate(sa): rk[v] = r
lcp = [0] * n; h = 0; st = []
for i in range(n):
    if rk[i] == 0:
        h = 0
        st.append({"at": {"i": i, "j": -1}, "vars": {"h": 0, "lcp": json.dumps(lcp, separators=(",", ":"))},
                   "note": f"i = {i}: the suffix is first in sorted order, so no predecessor exists and h resets to 0."})
        continue
    j = sa[rk[i] - 1]; h0 = h
    while i + h < n and j + h < n and s[i + h] == s[j + h]: h += 1
    lcp[rk[i]] = h
    st.append({"at": {"i": i, "j": j}, "vars": {"h": h, "lcp": json.dumps(lcp, separators=(",", ":"))},
               "note": f"i = {i}: predecessor starts at {j}. The match starts at h = {h0} and ends at {h}, so lcp[{rk[i]}] = {h}."})
    if h > 0: h -= 1
assert lcp == [0, 1, 3, 0, 0, 2] and len(st) == 6
fill(CH, F, block(list(s), ["i", "j"], st), "@@TRACE2@@")
