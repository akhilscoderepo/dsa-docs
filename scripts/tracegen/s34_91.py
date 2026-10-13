from common import *
CH = '34-advanced-strings'
FILE = '91-prefix-automata-state.md'


def fail_array(p):
    f = [0] * len(p)
    k = 0
    for i in range(1, len(p)):
        while k and p[i] != p[k]:
            k = f[k - 1]
        if p[i] == p[k]:
            k += 1
        f[i] = k
    return f


def trace_one(text, pat, expect):
    # Simulates the one-pattern machine with a match state that falls back.
    m = len(pat)
    fail = fail_array(pat)
    k = 0
    starts = []
    st = [{"at": {"i": -1, "k": 0}, "vars": {"starts": "[]"},
           "note": "Start: the match state is 0 and nothing is read yet."}]
    V = lambda: "[" + ",".join(map(str, starts)) + "]"
    for i, c in enumerate(text):
        while k > 0 and pat[k] != c:
            nk = fail[k - 1]
            st.append({"at": {"i": i, "k": nk}, "vars": {"starts": V()},
                       "note": f"i = {i}: p[{k}] is '{pat[k]}' and rejects '{c}'. The fallback moves the state from {k} to fail[{k - 1}] = {nk} and the same text index is tried again."})
            k = nk
        if pat[k] == c:
            k += 1
            note = f"i = {i}: '{c}' equals p[{k - 1}], so the state rises to {k}."
        else:
            note = f"i = {i}: '{c}' does not start the pattern, so the state stays 0."
        if k == m:
            starts.append(i - m + 1)
            st.append({"at": {"i": i, "k": k}, "vars": {"starts": V()},
                       "note": note + f" The state equals the pattern length, so a match starts at {i - m + 1}."})
            nk = fail[m - 1]
            st.append({"at": {"i": i, "k": nk}, "vars": {"starts": V()},
                       "note": f"i = {i}: the match state has no next pattern character, so it falls back to fail[{m - 1}] = {nk} and keeps scanning."})
            k = nk
        else:
            st.append({"at": {"i": i, "k": k}, "vars": {"starts": V()}, "note": note})
    assert starts == expect, starts
    assert starts == [s for s in range(len(text) - m + 1) if text[s:s + m] == pat]
    return block(list(text), ["i", "k"], st)


def trace_two(words, stream, expect):
    # Builds the trie in insertion order and simulates the stream with counts.
    go = [{}]
    cnt = [0]
    for w in words:
        v = 0
        for ch in w:
            if ch not in go[v]:
                go.append({})
                cnt.append(0)
                go[v][ch] = len(go) - 1
            v = go[v][ch]
        cnt[v] += 1
    fail = [0] * len(go)
    order = list(go[0].values())
    q = list(order)
    qi = 0
    while qi < len(q):
        v = q[qi]
        qi += 1
        cnt[v] += cnt[fail[v]]
        for ch, u in go[v].items():
            f = fail[v]
            while f and ch not in go[f]:
                f = fail[f]
            fail[u] = go[f][ch] if ch in go[f] and go[f][ch] != u else 0
            q.append(u)
    def step(v, ch):
        while v and ch not in go[v]:
            v = fail[v]
        return go[v].get(ch, 0)
    v = 0
    got = []
    st = [{"at": {"v": 0}, "vars": {"count": 0}, "note": "Start: the state is the root, node 0."}]
    for i, ch in enumerate(stream):
        nv = step(v, ch)
        got.append(cnt[nv])
        direct = ch in go[v]
        how = "the node has a child for this letter" if direct else "the transition follows the failure chain"
        st.append({"at": {"v": nv}, "vars": {"letter": ch, "count": cnt[nv]},
                   "note": f"Letter '{ch}': {how}, so the state moves from node {v} to node {nv}. Exactly {cnt[nv]} stored word(s) end here."})
        v = nv
    assert got == expect, got
    assert got == [sum(1 for w in words if stream[:i + 1].endswith(w)) for i in range(len(stream))]
    assert max(max(s["at"].values()) for s in st) <= len(stream)
    return block(list(stream), ["v"], st)


fill(CH, FILE, trace_one("aabaaabaa", "aabaa", [0, 4]), "@@TRACE1@@")
fill(CH, FILE, trace_two(["ab", "bab", "b"], "ababbab", [0, 2, 0, 3, 1, 0, 3]), "@@TRACE2@@")
