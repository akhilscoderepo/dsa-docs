from common import *
from tr import *
CH = '16-trees-bfs-and-bsts'
F = '10-tree-and-bfs.md'
arr = [4, -2, 6, 1, None, 5, 9]
L, R = parse(arr)
q = [0]; steps = []; wave_no = 1
while q:
    size = len(q); cnt = 0; tot = 0
    for k in range(size):
        i = q.pop(0); cnt += 1; tot += arr[i]
        for c in (L[i], R[i]):
            if c is not None: q.append(c)
        qs = " ".join(str(arr[j]) for j in q) or "empty"
        note = f"The person {arr[i]} is removed from wave {wave_no}, so the count is {cnt} and the sum is {tot}; the queue behind holds {qs}."
        if k == size - 1:
            note += f" The snapshot of {size} is used up, so the pair [{cnt}, {tot}] is written for this wave."
        steps.append({"at": {"node": i}, "vars": {"count": cnt, "sum": tot, "queue": qs}, "note": note})
    wave_no += 1
fill(CH, F, block(cells(arr), ["node"], steps), "@@TRACE1@@")
children = [[1, 2, 3], [4, 5], [], [6], [], [], []]
q = [0]; steps = []; wave_no = 1
while q:
    size = len(q)
    for k in range(size):
        i = q.pop(0)
        q.extend(children[i])
        qs = " ".join(map(str, q)) or "empty"
        added = f"it adds its {len(children[i])} children {' '.join(map(str, children[i]))} to the queue" if children[i] else "it has no children to add"
        note = f"The person {i} is removed from wave {wave_no} and {added}."
        if k == size - 1: note += f" This was removal {size} of {size}, so wave {wave_no} is complete."
        steps.append({"at": {"node": i}, "vars": {"wave": wave_no, "queue": qs}, "note": note})
    wave_no += 1
fill(CH, F, block([str(i) for i in range(7)], ["node"], steps), "@@TRACE2@@")
