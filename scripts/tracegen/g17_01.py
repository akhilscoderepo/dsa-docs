import sys
from common import *
from hp import *
CH = '17-heaps-and-priority-queues'
F = '01-priorityqueue-mechanics.md'


def offers(vals):
    h = Heap()
    steps = []
    for i, v in enumerate(vals):
        swaps, k = h.offer(v)
        parts = [f"Value {v} is appended at index {len(h) - 1}."]
        if swaps:
            parts.append(f"Sift-up moves it up {len(swaps)} level{'s' if len(swaps) > 1 else ''}, to index {k}.")
        else:
            parts.append("Its parent is not larger, so it stays.")
        parts.append(f"The root is {h.a[0]}.")
        steps.append({"at": {"i": i}, "vars": {"heap": fmt(h.a), "root": h.a[0]}, "note": " ".join(parts)})
    return h, steps


vals = [7, 3, 9, 1, 5, 2]
h, s1 = offers(vals)
assert h.a == [1, 3, 2, 7, 5, 9], h.a
fill(CH, F, block(vals, ["i"], s1), "@@TRACE1@@")

# second trace: one poll, sift-down
h2 = Heap()
for v in [4, 8, 6, 9, 12, 7, 10]:
    h2.offer(v)
before = list(h2.a)
a = list(h2.a)
last = a.pop()
start = [last] + a[1:]
# simulate steps by hand with the same rule
n = len(start)
k = 0
cells = list(start)
cur = list(start)
steps = []
steps.append({"at": {"node": 0}, "vars": {"heap": fmt(cur), "removed": before[0]},
              "note": f"The root {before[0]} is polled and the last item {last} is moved to index 0. The array is shown after that move, and the value {last} must now sink to its place."})
while True:
    c = 2 * k + 1
    if c >= n:
        steps.append({"at": {"node": k}, "vars": {"heap": fmt(cur), "removed": before[0]},
                      "note": f"Index {k} has no children, so the sink stops. The heap order is restored."})
        break
    kids = [c] + ([c + 1] if c + 1 < n else [])
    small = c + 1 if c + 1 < n and cur[c + 1] < cur[c] else c
    if cur[small] < last:
        desc = " and ".join(str(cur[x]) for x in kids)
        cur[k] = cur[small]
        cur[small] = last
        steps.append({"at": {"node": small}, "vars": {"heap": fmt(cur), "removed": before[0]},
                      "note": f"The children of index {k} hold {desc}. The smaller child {cur[k]} is less than {last}, so it moves up and {last} sinks to index {small}."})
        k = small
    else:
        desc = " and ".join(str(cur[x]) for x in kids)
        steps.append({"at": {"node": k}, "vars": {"heap": fmt(cur), "removed": before[0]},
                      "note": f"The children of index {k} hold {desc}. Neither is smaller than {last}, so the sink stops here."})
        break
h3 = Heap()
for v in [4, 8, 6, 9, 12, 7, 10]:
    h3.offer(v)
h3.poll()
assert cur == h3.a, (cur, h3.a)
fill(CH, F, block(cells, ["node"], steps), "@@TRACE2@@")
print(before, cells, cur, file=sys.stderr)
