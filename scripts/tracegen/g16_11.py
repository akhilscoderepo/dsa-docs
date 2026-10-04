from common import *
from tr import *
CH = '16-trees-bfs-and-bsts'
F = '11-bst-and-bounds.md'
def show(x, neg): return ("-inf" if neg else "+inf") if x is None else str(x)
# trace 1: stopping interval of a missing key
arr = [8, 3, 10, 1, 6, None, 14]
L, R = parse(arr)
key = 7; lo = hi = None; i = 0; st = []
while i is not None:
    v = arr[i]
    if key < v:
        hi = v; nxt = L[i]; side = "left"; what = f"the upper end becomes {v}"
    else:
        lo = v; nxt = R[i]; side = "right"; what = f"the lower end becomes {v}"
    st.append({"at": {"node": i}, "vars": {"lo": show(lo, True), "hi": show(hi, False)}, "note": f"The key {key} is {'smaller' if side == 'left' else 'larger'} than the stack {v}, so the walk goes {side} and {what}."})
    i = nxt
st.append({"at": {"node": -1}, "vars": {"lo": show(lo, True), "hi": show(hi, False)}, "note": f"The walk leaves the tree here, so nothing can lie between {lo} and {hi}; these are the neighbours of the missing key {key}."})
assert (lo, hi) == (6, 8)
fill(CH, F, block(cells(arr), ["node"], st), "@@TRACE1@@")
# trace 2: first violation in preorder
arr = [5, 4, 6, None, None, 3, 7]
L, R = parse(arr)
st = []; done = [False]
def go(i, lo, hi):
    if i is None or done[0]: return
    v = arr[i]
    iv = f"({show(lo, True)}, {show(hi, False)})"
    fits = (lo is None or v > lo) and (hi is None or v < hi)
    if fits:
        note = f"The stack {v} arrives with the interval {iv} and fits, so its left side gets ({show(lo, True)}, {v}) and its right side gets ({v}, {show(hi, False)})."
    else:
        note = f"The stack {v} arrives with the interval {iv} and does not fit, so the first violation is at position {i} and the walk stops."
        done[0] = True
    st.append({"at": {"node": i}, "vars": {"lo": show(lo, True), "hi": show(hi, False)}, "note": note})
    if fits:
        go(L[i], lo, v); go(R[i], v, hi)
go(0, None, None)
assert [s["at"]["node"] for s in st] == [0, 1, 2, 5]
fill(CH, F, block(cells(arr), ["node"], st), "@@TRACE2@@")
# trace 3: kth key inside a band
arr = [8, 4, 12, 2, 6, 10, 14, 1, 3, 5, 7, 9, 11, 13, 15]
L, R = parse(arr)
low, high, k = 5, 12, 3
stack = []; node = 0; st = []; ans = None
while node is not None or stack:
    while node is not None:
        if arr[node] < low: node = R[node]
        else:
            stack.append(node); node = L[node]
    if not stack: break
    node = stack.pop()
    if arr[node] > high: break
    k -= 1
    waiting = " ".join(str(arr[j]) for j in reversed(stack)) or "empty"
    note = f"The box {arr[node]} is popped inside the band, so the countdown becomes {k}."
    if k == 0:
        note += f" The countdown is zero, so {arr[node]} is the answer."; ans = arr[node]
    st.append({"at": {"node": node}, "vars": {"countdown": k, "stack": waiting}, "note": note})
    if k == 0: break
    node = R[node]
assert ans == 7 and len(st) == 3
fill(CH, F, block(cells(arr), ["node"], st), "@@TRACE3@@")
