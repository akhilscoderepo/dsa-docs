from common import *
CH = '37-iterators-encodings-and-versioned-state'
NAME = '92-codec-structural-traversal.md'

# Trace 1: decode the level-order text with a queue of nodes.
text = "1,2,3,null,null,4,5"
tok = text.split(",")
idx = 1
queue = ["1"]
steps = [{"at": {"idx": 1}, "vars": {"queue": "[1]", "built": "root 1"}, "note": "The first token creates the root 1, and the queue holds the root. The index moves to the next unread token."}]
built = {"1": []}
tree = {}
while queue:
    n = queue.pop(0)
    kids = {}
    for side in ("left", "right"):
        if idx >= len(tok):
            steps.append({"at": {"idx": idx}, "vars": {"queue": "[" + ",".join(queue) + "]", "owner": n, "slot": side}, "note": f"No token is left, so the {side} slot of node {n} counts as empty."})
            continue
        t = tok[idx]
        idx += 1
        if t == "null":
            steps.append({"at": {"idx": idx}, "vars": {"queue": "[" + ",".join(queue) + "]", "owner": n, "slot": side}, "note": f"The token null leaves the {side} slot of node {n} empty."})
        else:
            queue.append(t)
            kids[side] = t
            steps.append({"at": {"idx": idx}, "vars": {"queue": "[" + ",".join(queue) + "]", "owner": n, "slot": side}, "note": f"The token {t} fills the {side} slot of node {n}, and the new node joins the back of the queue."})
    tree[n] = kids
assert idx == len(tok)
assert tree == {"1": {"left": "2", "right": "3"}, "2": {}, "3": {"left": "4", "right": "5"}, "4": {}, "5": {}}
fill(CH, NAME, block(tok, ["idx"], steps), "@@TRACE1@@")

# Trace 2: encode the forest [1[2,3],4] as one binary tree, then walk it in preorder.
class N:
    def __init__(s, v): s.v = v; s.kids = []
class B:
    def __init__(s, v): s.v = v; s.l = None; s.r = None
def chain(nodes):
    head = prev = None
    for n in nodes:
        t = B(n.v)
        t.l = chain(n.kids)
        if prev is None: head = t
        else: prev.r = t
        prev = t
    return head
r1 = N(1); r1.kids = [N(2), N(3)]
forest = [r1, N(4)]
root = chain(forest)
out = []
steps = [{"at": {"out": 0}, "vars": {"written": "[]"}, "note": "Start: the encoder has linked the roots 1 and 4 in a right chain and put 2 and 3 in a chain on the left link of 1. Nothing is written yet."}]
def walk(t, why):
    if t is None:
        out.append("N")
        steps.append({"at": {"out": len(out)}, "vars": {"written": " ".join(out)}, "note": f"The {why} is missing, so the walk writes N."})
        return
    out.append(str(t.v))
    steps.append({"at": {"out": len(out)}, "vars": {"written": " ".join(out)}, "note": f"The walk writes the value {t.v} for the {why}."})
    walk(t.l, f"left link of {t.v}")
    walk(t.r, f"right link of {t.v}")
walk(root, "root of the binary tree")
assert out == "1 2 N 3 N N 4 N N".split() and len(out) == 2 * 4 + 1
fill(CH, NAME, block(out, ["out"], steps), "@@TRACE2@@")
