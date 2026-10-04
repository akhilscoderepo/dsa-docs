from common import *
from tn import *
CH='18-tries'
F='04-word-break-trie-search.md'

# trace 1: one walk from start 0
s = "catsanddog"; words = ["cat", "cats", "and", "sand", "dog"]
t = Trie()
for w in words: t.insert(w)
steps = []; cur = 0; ends = []
for j in range(0, len(s)):
    ch = s[j]
    if ch not in t.kids[cur]:
        steps.append({"at": {"i": 0, "j": j}, "vars": {"node": s[:j], "ends": " ".join(map(str, ends))},
                      "note": f"The letter {ch} has no edge below the node for {s[0:j]}, so this is the dead end and the walk stops with the ends found so far."})
        break
    cur = t.kids[cur][ch]
    if t.term[cur]:
        ends.append(j + 1)
        note = f"The node for {s[:j+1]} is flagged, so {j+1} is recorded as an end and the walk continues."
    else:
        note = f"The node for {s[:j+1]} is not flagged, so only the cursor moves."
    steps.append({"at": {"i": 0, "j": j}, "vars": {"node": s[:j+1], "ends": " ".join(map(str, ends))}, "note": note})
assert ends == [3, 4]
fill(CH, F, block(list(s), ["i", "j"], steps), "@@TRACE1@@")

# trace 2: plain recursion on aaab, words a and aa
s = "aaab"; ws = {"a", "aa"}
steps = []; calls = [0]
def go(st):
    calls[0] += 1
    n = len(s)
    if st == n:
        steps.append({"at": {"start": st}, "vars": {"calls": calls[0]}, "note": "The whole banner is used up, so this call answers yes."})
        return True
    ends = [e for e in range(st + 1, n + 1) if s[st:e] in ws]
    if ends:
        steps.append({"at": {"start": st}, "vars": {"calls": calls[0]}, "note": f"The call for start {st} finds the ends {', '.join(map(str, ends))} and tries them in order."})
    else:
        steps.append({"at": {"start": st}, "vars": {"calls": calls[0]}, "note": f"The call for start {st} finds no approved word beginning here, so it answers no."})
    for e in ends:
        if go(e): return True
    return False
assert go(0) is False
print(calls[0])
fill(CH, F, block(list(s), ["start"], steps), "@@TRACE2@@")
