from common import *
CH = '37-iterators-encodings-and-versioned-state'
NAME = '91-iterator-traversal-state.md'

class N:
    def __init__(s, v, l=None, r=None): s.v, s.l, s.r = v, l, r

def inorder(n):
    return inorder(n.l) + [n.v] + inorder(n.r) if n else []

def trace(root, calls, cells_expect):
    keys = inorder(root)
    assert keys == cells_expect
    pending = []; visited = []; pos = -1
    def spine(n):
        while n: pending.append(n); n = n.l
    spine(root)
    P = lambda: "[" + ",".join(str(x.v) for x in reversed(pending)) + "]"
    V = lambda: "[" + ",".join(map(str, visited)) + "]"
    st = [{"at": {"pos": -1}, "vars": {"call": "new", "result": "none", "visited": "[]", "pending": P()}, "note": "Start: the constructor pushed the left spine, so the smallest key is on top of pending, and pos is -1."}]
    def hasnext(): return pos + 1 < len(visited) or bool(pending)
    for c, note in calls:
        if c == "next":
            if not hasnext():
                st.append({"at": {"pos": pos}, "vars": {"call": "next()", "result": "throws", "visited": V(), "pending": P()}, "note": note}); continue
            if pos + 1 == len(visited):
                n = pending.pop(); spine(n.r); visited.append(n.v)
            pos += 1; r = visited[pos]
            st.append({"at": {"pos": pos}, "vars": {"call": "next()", "result": r, "visited": V(), "pending": P()}, "note": note})
        elif c == "prev":
            if pos <= 0:
                st.append({"at": {"pos": pos}, "vars": {"call": "prev()", "result": "throws", "visited": V(), "pending": P()}, "note": note}); continue
            pos -= 1; r = visited[pos]
            st.append({"at": {"pos": pos}, "vars": {"call": "prev()", "result": r, "visited": V(), "pending": P()}, "note": note})
        elif c == "hasNext":
            st.append({"at": {"pos": pos}, "vars": {"call": "hasNext()", "result": str(hasnext()).lower(), "visited": V(), "pending": P()}, "note": note})
        elif c == "hasPrev":
            st.append({"at": {"pos": pos}, "vars": {"call": "hasPrev()", "result": str(pos > 0).lower(), "visited": V(), "pending": P()}, "note": note})
    return block([str(k) for k in keys], ["pos"], st), st

t1 = N(7, N(3), N(15, N(9), N(20)))
c1 = [("next", "next pops 3, which has no right child, appends 3 and moves pos to 0."),
      ("next", "next pops 7 and pushes the left spine of 15, which is 15 and 9. It appends 7 and moves pos to 1."),
      ("next", "next pops 9, appends it and moves pos to 2."),
      ("prev", "prev moves pos from 2 to 1 and returns 7 from visited. The tree is not read."),
      ("prev", "prev moves pos to 0 and returns 3 from visited."),
      ("next", "next replays 7 from visited. pending is unchanged."),
      ("next", "next replays 9 from visited. pending is unchanged."),
      ("next", "pos is at the last visited key, so next extends the history. It pops 15, pushes the left spine of 20, appends 15 and moves pos to 3.")]
b1, s1 = trace(t1, c1, [3, 7, 9, 15, 20])
assert [s["vars"]["result"] for s in s1[1:]] == [3, 7, 9, 7, 3, 7, 9, 15]
fill(CH, NAME, b1, "@@TRACE1@@")

t2 = N(2, N(1), N(3))
c2 = [("next", "next pops 1 and appends it. pos is 0."),
      ("next", "next pops 2, pushes the left spine of 3 and appends 2. pos is 1."),
      ("next", "next pops 3 and appends it. pending is now empty and pos is 2."),
      ("hasNext", "No visited key lies after pos, and pending is empty, so hasNext returns false."),
      ("next", "next finds nothing to replay or extend, throws NoSuchElementException and changes no field."),
      ("prev", "prev moves pos to 1 and returns 2."),
      ("prev", "prev moves pos to 0 and returns 1."),
      ("hasPrev", "pos is 0, so no key lies before the current one and hasPrev returns false."),
      ("prev", "prev throws NoSuchElementException and leaves pos at 0."),
      ("next", "next replays 2 from visited and moves pos to 1.")]
b2, s2 = trace(t2, c2, [1, 2, 3])
assert [s["vars"]["result"] for s in s2[1:]] == [1, 2, 3, "false", "throws", 2, 1, "false", "throws", 2]
fill(CH, NAME, b2, "@@TRACE2@@")
