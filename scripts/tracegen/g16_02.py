from common import *
from tr import *
CH = '16-trees-bfs-and-bsts'
F = '02-bst-invariant-and-bounds.md'
def fmt(x, neg): return ("-inf" if neg else "+inf") if x is None else str(x)
def run(arr):
    L, R = parse(arr)
    st = []; ok = [True]
    def go(i, lo, hi):
        if i is None or not ok[0]: return
        v = arr[i]
        iv = f"({fmt(lo, True)}, {fmt(hi, False)})"
        fits = (lo is None or v > lo) and (hi is None or v < hi)
        if fits:
            note = f"The shelf {v} arrives with the interval {iv} and fits strictly inside it, so its children get ({fmt(lo, True)}, {v}) and ({v}, {fmt(hi, False)})."
        else:
            note = f"The shelf {v} arrives with the interval {iv} and does not fit strictly inside it, so the plan is rejected here."
            ok[0] = False
        st.append({"at": {"node": i}, "vars": {"lo": fmt(lo, True), "hi": fmt(hi, False)}, "note": note})
        if fits:
            go(L[i], lo, v); go(R[i], v, hi)
    go(0, None, None)
    return st, ok[0]
arr = [5, 3, 8, 1, 4, 7, 9]
s, ok = run(arr); assert ok
fill(CH, F, block(cells(arr), ["node"], s), "@@TRACE1@@")
arr = [10, 5, 15, None, None, 6, 20]
s, ok = run(arr); assert not ok and len(s) == 4
fill(CH, F, block(cells(arr), ["node"], s), "@@TRACE2@@")
