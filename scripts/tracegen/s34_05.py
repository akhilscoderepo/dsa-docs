from collections import deque
from common import *
CH = '34-advanced-strings'; F = '05-aho-corasick.md'

def build(pats):
    # Trie in creation order, then BFS fill of fail, link and the full goto table.
    go = [dict()]; term = [-1]; label = ['']
    for k, p in enumerate(pats):
        v = 0
        for ch in p:
            if ch not in go[v]:
                go.append(dict()); term.append(-1); label.append(label[v] + ch)
                go[v][ch] = len(go) - 1
            v = go[v][ch]
        term[v] = k
    n = len(go); fail = [0] * n; link = [0] * n
    q = deque(go[0].values())
    while q:
        v = q.popleft(); f = fail[v]
        link[v] = f if term[f] >= 0 else link[f]
        for ch, u in go[v].items():
            w = f
            while w and ch not in go[w]: w = fail[w]
            t = go[w].get(ch, 0)
            fail[u] = t if t != u else 0
            q.append(u)
    return go, term, label, fail, link

def trace(pats, text):
    go, term, label, fail, link = build(pats)
    v = 0; st = [{"at": {"i": -1}, "vars": {"state": "(root)", "reported": "-"}, "note": "Before the first letter the state is the root."}]
    found = []
    for i, ch in enumerate(text):
        fell = []
        while v and ch not in go[v]:
            v = fail[v]; fell.append(label[v] or '(root)')
        old = label[v] or '(root)'
        v = go[v].get(ch, 0)
        rep = []
        m = v if term[v] >= 0 else link[v]
        while m:
            rep.append(pats[term[m]]); found.append((i, pats[term[m]])); m = link[m]
        # the walk above covers the goto fallback; the note names the fallback nodes visited
        note = f"i = {i}: letter {ch}. "
        if fell: note += f"The child is missing, so the table falls back through {', '.join(fell)} and moves to {label[v] or '(root)'}. "
        elif v == 0: note += "No pattern starts with this letter, so the state stays at the root. "
        else: note += f"The state moves from {old} to {label[v]}. "
        note += (f"It reports {', '.join(rep)}." if rep else "No pattern ends here.")
        st.append({"at": {"i": i}, "vars": {"state": label[v] or '(root)', "reported": ', '.join(rep) or '-'}, "note": note})
    return list(text), st, found, (go, term, label, fail, link)

P1 = ["he", "she", "his", "hers"]
c, st, found, aut = trace(P1, "ushers")
assert aut[3] == [0, 0, 0, 0, 1, 2, 0, 3, 0, 3]
assert found == [(3, "she"), (3, "he"), (5, "hers")]
assert len(st) == 7
fill(CH, F, block(c, ["i"], st), "@@TRACE1@@")

P2 = ["ab", "bab", "bc", "bca", "c", "caa"]
c, st, found, aut = trace(P2, "babcaa")
brute = sorted((i + len(p) - 1, p) for p in P2 for i in range(len("babcaa")) if "babcaa".startswith(p, i))
assert sorted(found) == brute, (found, brute)
assert len(st) == 7
fill(CH, F, block(c, ["i"], st), "@@TRACE2@@")
