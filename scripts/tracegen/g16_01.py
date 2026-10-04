from common import *
from tr import *
CH = '16-trees-bfs-and-bsts'
F = '01-levels-zigzag-and-views.md'

def run(arr, mode):
    L, R = parse(arr)
    q = [0]; steps = []; out = []
    ring_no = 0
    while q:
        size = len(q); ring = []
        for k in range(size):
            i = q.pop(0)
            ring.append(arr[i])
            for c in (L[i], R[i]):
                if c is not None: q.append(c)
            qs = " ".join(str(arr[j]) for j in q) or "empty"
            if mode == 'levels':
                note = f"The lantern {arr[i]} is removed; the card for ring {ring_no} now reads {' '.join(map(str, ring))} and the queue behind it holds {qs}."
                if k == size - 1: note += f" The snapshot of {size} is used up, so the card is closed."
                steps.append({"at": {"node": i}, "vars": {"size": size, "ring": " ".join(map(str, ring)), "queue": qs}, "note": note})
            else:
                last = k == size - 1
                note = f"The lantern {arr[i]} is removal {k + 1} of {size} in ring {ring_no}, " + ("the last of its ring, so it is recorded." if last else "not the last of its ring, so it is skipped.")
                if last: out.append(arr[i])
                steps.append({"at": {"node": i}, "vars": {"size": size, "seen": k + 1, "queue": qs}, "note": note})
        ring_no += 1
    return steps, out

arr = [3, 9, 20, None, None, 15, 7]
s, _ = run(arr, 'levels')
fill(CH, F, block(cells(arr), ["node"], s), "@@TRACE1@@")
arr = [1, 2, 3, None, 5, None, 4]
s, out = run(arr, 'view')
assert out == [1, 3, 4]
fill(CH, F, block(cells(arr), ["node"], s), "@@TRACE2@@")
