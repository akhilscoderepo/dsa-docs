from common import *
from tr import *
CH = '16-trees-bfs-and-bsts'
F = '05-kth-and-range-queries.md'
# trace 1: countdown walk
arr = [5, 3, 6, 2, 4, None, None, 1]
L, R = parse(arr)
k = 3; stack = []; node = 0; steps = []; ans = None
while node is not None or stack:
    while node is not None:
        stack.append(node); node = L[node]
    node = stack.pop()
    k -= 1
    waiting = " ".join(str(arr[j]) for j in reversed(stack)) or "empty"
    note = f"The crate {arr[node]} is popped as the next heavier crate and the countdown drops to {k}."
    if k == 0:
        note += f" The countdown has reached zero, so {arr[node]} is the answer and the walk stops."
        ans = arr[node]
    steps.append({"at": {"node": node}, "vars": {"countdown": k, "stack": waiting}, "note": note})
    if k == 0: break
    node = R[node]
assert ans == 3
fill(CH, F, block(cells(arr), ["node"], steps), "@@TRACE1@@")
# trace 2: pruned band sum
arr = [8, 4, 12, 2, 6, 10, 14, 1, 3, 5, 7, 9, 11, 13, 15]
L, R = parse(arr)
low, high = 5, 9
steps = []; total = [0]
def go(i):
    if i is None: return
    v = arr[i]
    if v < low:
        note = f"The crate {v} is lighter than {low}, so it and its left side are out and only the right side is entered."
    elif v > high:
        note = f"The crate {v} is heavier than {high}, so it and its right side are out and only the left side is entered."
    else:
        total[0] += v
        note = f"The crate {v} lies inside the band and is added, so the total becomes {total[0]} and both sides are entered."
    steps.append({"at": {"node": i}, "vars": {"low": low, "high": high, "total": total[0]}, "note": note})
    if v < low: go(R[i])
    elif v > high: go(L[i])
    else: go(L[i]); go(R[i])
go(0)
assert total[0] == 35 and [s["at"]["node"] for s in steps] == [0, 1, 4, 9, 10, 2, 5, 11]
fill(CH, F, block(cells(arr), ["node"], steps), "@@TRACE2@@")
