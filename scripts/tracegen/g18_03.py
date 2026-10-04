from common import *
from tn import *
CH='18-tries'
F='03-wildcard-branching.md'

def dfs_steps(words, pattern):
    t = Trie()
    for w in words: t.insert(w)
    steps = []; calls = [0]
    def lab(pre): return pre if pre else "the root"
    def go(node, pre, pos):
        calls[0] += 1
        if pos == len(pattern):
            ok = t.term[node]
            steps.append({"at": {"i": pos}, "vars": {"prefix": pre, "calls": calls[0]},
                          "note": f"The pattern is used up at {lab(pre)}, and its flag is {'set' if ok else 'unset'}, so this call answers {'yes' if ok else 'no'}."})
            return ok
        c = pattern[pos]
        if c != '.':
            if c not in t.kids[node]:
                steps.append({"at": {"i": pos}, "vars": {"prefix": pre, "calls": calls[0]},
                              "note": f"The square is the letter {c}, and {lab(pre)} has no edge {c}, so this call answers no without looking at any sibling."})
                return False
            steps.append({"at": {"i": pos}, "vars": {"prefix": pre, "calls": calls[0]},
                          "note": f"The square is the letter {c}, so only the edge {c} is followed from {lab(pre)}."})
            return go(t.kids[node][c], pre + c, pos + 1)
        ks = sorted(t.kids[node])
        steps.append({"at": {"i": pos}, "vars": {"prefix": pre, "calls": calls[0]},
                      "note": f"The square is blank, so every child of {lab(pre)} is a candidate: {', '.join(ks)} in that order."})
        for k in ks:
            if go(t.kids[node][k], pre + k, pos + 1): return True
        return False
    return steps, go(0, "", 0)

s1, a1 = dfs_steps(["bad", "bed", "bid", "cod"], "b.d")
assert a1 is True and len(s1) == 4
fill(CH, F, block(list("b.d"), ["i"], s1), "@@TRACE1@@")
s2, a2 = dfs_steps(["bat", "cad", "dad", "cot"], ".ad")
assert a2 is True and len(s2) == 6
fill(CH, F, block(list(".ad"), ["i"], s2), "@@TRACE2@@")
