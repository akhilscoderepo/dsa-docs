from common import *
from tr import *
CH = '16-trees-bfs-and-bsts'
F = '08-serialization-and-deserialization.md'
arr = [1, 2, 3, None, None, 4, 5]
# cells that sit below each present node (a null cell is an explicit empty hanging)
CHILD_CELLS = {}
q = [0]; nxt = 1; qi = 0
while qi < len(q):
    i = q[qi]; qi += 1
    if arr[i] is None: continue
    cs = []
    for _ in range(2):
        if nxt < len(arr):
            cs.append(nxt)
            if arr[nxt] is not None: q.append(nxt)
            nxt += 1
    if cs: CHILD_CELLS[i] = cs
card = []; steps = []
def walk(i):
    v = arr[i]
    if v is None:
        card.append("#")
        steps.append({"at": {"node": i}, "vars": {"card": ",".join(card)}, "note": "This hanging spot is empty, so one marker # is written for it."})
        return
    card.append(str(v))
    kids = CHILD_CELLS.get(i)
    if kids is None:
        card.append("#"); card.append("#")
        steps.append({"at": {"node": i}, "vars": {"card": ",".join(card)}, "note": f"The weight {v} is a leaf with no cells below it, so it is written and then two markers # for its empty hangings."})
        return
    steps.append({"at": {"node": i}, "vars": {"card": ",".join(card)}, "note": f"The weight {v} is written first, and its left hanging and then its right hanging follow."})
    for c in kids: walk(c)
walk(0)
text = ",".join(card)
assert text == "1,2,#,#,3,4,#,#,5,#,#", text
fill(CH, F, block(cells(arr), ["node"], steps), "@@TRACE1@@")
# trace 2: read the card back with one shared cursor
tokens = text.split(",")
evs = []; cur = [0]
def read(parent, side):
    k = cur[0]; cur[0] += 1
    t = tokens[k]
    where = "as the root" if parent is None else f"as the {side} child of {parent}"
    if t == "#":
        evs.append((k, parent, f"The marker # closes an empty {side} hanging of {parent}."))
        return
    evs.append((k, t, f"The token {t} creates the weight {t} {where}, and its left hanging is read next."))
    read(t, "left"); read(t, "right")
read(None, "left")
assert cur[0] == len(tokens)
steps = [{"at": {"cursor": k}, "vars": {"building": b}, "note": n} for k, b, n in evs]
fill(CH, F, block(tokens, ["cursor"], steps), "@@TRACE2@@")
