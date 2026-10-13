from common import *
CH = '37-iterators-encodings-and-versioned-state'
F = '05-query-objects.md'


def merge_trace(text, wa, wb):
    pa = [i for i, w in enumerate(text) if w == wa]
    pb = [i for i, w in enumerate(text) if w == wb]
    i = j = 0; best = None
    st = [{"at": {"a": pa[0], "b": pb[0]}, "vars": {"best": "none"},
           "note": f"Start: the cursors point to position {pa[0]} of {wa} and position {pb[0]} of {wb}."}]
    while i < len(pa) and j < len(pb):
        gap = abs(pa[i] - pb[j])
        best = gap if best is None else min(best, gap)
        mover = "a" if pa[i] < pb[j] else "b"
        if mover == "a": i += 1
        else: j += 1
        na = pa[i] if i < len(pa) else len(text)
        nb = pb[j] if j < len(pb) else len(text)
        done = i >= len(pa) or j >= len(pb)
        st.append({"at": {"a": na, "b": nb}, "vars": {"gap": gap, "best": best},
                   "note": f"The gap is {gap}, so best is {best}. The cursor of {wa if mover == 'a' else wb} has the smaller position and moves forward." + (" A list is now exhausted, so the walk ends." if done else "")})
    return block(text, ["a", "b"], st), best


def lb_trace(plist, left, right):
    st = []
    def lb(x, label):
        lo, hi = 0, len(plist)
        st.append({"at": {"lo": lo, "hi": hi, "mid": -1}, "vars": {"target": x}, "note": f"Search {label}: find the first position at least {x}."})
        while lo < hi:
            mid = (lo + hi) // 2
            if plist[mid] < x:
                st.append({"at": {"lo": lo, "hi": hi, "mid": mid}, "vars": {"target": x, "entry": plist[mid]}, "note": f"Entry {plist[mid]} is below {x}, so lo becomes {mid + 1}."}); lo = mid + 1
            else:
                st.append({"at": {"lo": lo, "hi": hi, "mid": mid}, "vars": {"target": x, "entry": plist[mid]}, "note": f"Entry {plist[mid]} is at least {x}, so hi becomes {mid}."}); hi = mid
        st.append({"at": {"lo": lo, "hi": hi, "mid": lo}, "vars": {"target": x, "index": lo}, "note": f"The window closes at index {lo}."})
        return lo
    a = lb(left, "one"); b = lb(right + 1, "two")
    st.append({"at": {"lo": a, "hi": b, "mid": a}, "vars": {"count": b - a}, "note": f"The count is {b} minus {a}, which is {b - a}."})
    return block([str(p) for p in plist], ["lo", "hi", "mid"], st), b - a


arr = [1, 3, 2, 3, 3, 1, 3, 2, 3]
plist = [i for i, x in enumerate(arr) if x == 3]
assert plist == [1, 3, 4, 6, 8]
t2, c = lb_trace(plist, 2, 6)
assert c == sum(1 for i in range(2, 7) if arr[i] == 3) == 3
text = "a c b c a c b b c a".split()
t1, best = merge_trace(text, "a", "b")
assert best == min(abs(i - j) for i, w in enumerate(text) for j, v in enumerate(text) if w == "a" and v == "b") == 2
fill(CH, F, t1, "@@TRACE1@@")
fill(CH, F, t2, "@@TRACE2@@")
