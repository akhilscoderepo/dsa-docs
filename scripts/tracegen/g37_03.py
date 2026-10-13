from common import *
CH = '37-iterators-encodings-and-versioned-state'
NAME = '03-structural-codecs.md'

# Trace 1: decode a framed string and assert the final list.
enc = "2#ab0#3#c#d"
cells = list(enc)
steps = [{"at": {"i": 0, "hash": -1}, "vars": {"items": "[]"}, "note": "Start: the pointer i stands on the first character of the first frame, and no item is decoded."}]
items = []
i = 0
while i < len(enc):
    h = enc.index('#', i)
    ln = int(enc[i:h])
    body = h + 1
    items.append(enc[body:body + ln])
    i = body + ln
    shown = "[" + ", ".join('"' + x + '"' for x in items) + "]"
    if ln == 0:
        note = "The header says 0, so the frame has an empty body. The decoder takes no characters and stores an empty item."
    elif items[-1] == "c#d":
        note = "The header says 3. The decoder takes the next 3 characters, including the # inside the body, because the length already fixed where the frame ends."
    else:
        note = f"The header says {ln}. The decoder takes the next {ln} characters and moves i past them."
    steps.append({"at": {"i": i, "hash": h}, "vars": {"len": ln, "items": shown}, "note": note})
assert items == ["ab", "", "c#d"] and i == len(enc)
fill(CH, NAME, block(cells, ["i", "hash"], steps), "@@TRACE1@@")

# Trace 2: bounded preorder decode of a BST with no markers.
vals = [5, 3, 1, 4, 8, 9]
pos = 0
st = [{"at": {"rest": 0}, "vars": {"range": "(-inf, inf)", "built": "[]"}, "note": "Start: the root call has no bounds, and every token is still unread."}]
built = []
def f(x):
    return "-inf" if x is None else ("inf" if x == "INF" else str(x))
def rng(lo, hi):
    return "(" + ("-inf" if lo is None else str(lo)) + ", " + ("inf" if hi is None else str(hi)) + ")"
def build(lo, hi):
    global pos
    r = rng(lo, hi)
    if pos == len(vals):
        st.append({"at": {"rest": pos}, "vars": {"range": r, "built": "[" + ", ".join(map(str, built)) + "]"}, "note": f"No token is left, so the call with range {r} returns null."})
        return None
    v = vals[pos]
    if (lo is not None and v <= lo) or (hi is not None and v >= hi):
        st.append({"at": {"rest": pos}, "vars": {"range": r, "built": "[" + ", ".join(map(str, built)) + "]"}, "note": f"The token {v} lies outside {r}, so the call returns null and leaves the token for an ancestor."})
        return None
    pos += 1
    built.append(v)
    st.append({"at": {"rest": pos}, "vars": {"range": r, "built": "[" + ", ".join(map(str, built)) + "]"}, "note": f"The token {v} lies inside {r}, so it becomes a node. Its left range is {rng(lo, v)} and its right range is {rng(v, hi)}."})
    build(lo, v)
    build(v, hi)
    return v
build(None, None)
assert pos == len(vals) and built == vals
fill(CH, NAME, block([str(v) for v in vals], ["rest"], st), "@@TRACE2@@")
