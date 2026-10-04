from common import *
from tn import *
CH='18-tries'
F='06-trie-and-string-search.md'

# trace 1: shorten "battery" with roots bat, cat
t = Trie()
for r in ("bat", "cat"): t.insert(r)
word = "battery"; cur = 0; steps = []; answer = None
for i, ch in enumerate(word):
    cur = t.kids[cur][ch]
    pre = word[:i + 1]
    if t.term[cur]:
        steps.append({"at": {"i": i}, "vars": {"node": pre, "flag": "set"},
                      "note": f"The node for {pre} is flagged, so the stop rule fires: the shortest root is {pre}, and the letters after position {i} are never read."})
        answer = pre
        break
    steps.append({"at": {"i": i}, "vars": {"node": pre, "flag": "unset"},
                  "note": f"The node for {pre} exists but is not flagged, so the walk continues."})
assert answer == "bat" and len(steps) == 3
fill(CH, F, block(list(word), ["i"], steps), "@@TRACE1@@")

# trace 2: terminal-only descent on a sorted word list
words = sorted(["a", "ab", "abc", "abd", "b", "bd", "xy", "xyz"])
t = Trie()
for w in words: t.insert(w)
steps = []; best = [""]
def go(node, pre):
    for c in sorted(t.kids[node]):
        child = t.kids[node][c]
        if not t.term[child]: continue
        w = pre + c
        if len(w) > len(best[0]):
            best[0] = w; note = f"The node for {w} is flagged and entered, and {w} is longer than the best so far, so it becomes the best."
        else:
            note = f"The node for {w} is flagged and entered, but {w} is not longer than the best word {best[0]}, so the best stays."
        steps.append({"at": {"w": words.index(w)}, "vars": {"best": best[0], "len": len(best[0])}, "note": note})
        go(child, w)
go(0, "")
assert best[0] == "abc" and len(steps) == 6
fill(CH, F, block(words, ["w"], steps), "@@TRACE2@@")
