from common import *
from hp import *
CH = '17-heaps-and-priority-queues'
F = '04-k-way-merge.md'


def merge(sources):
    off = []
    t = 0
    for s in sources:
        off.append(t)
        t += len(s)
    flat = [x for s in sources for x in s]
    h = Heap(key=lambda e: (e[0], e[1]))
    for s, src in enumerate(sources):
        if src:
            h.offer((src[0], s, 0))
    out = []
    steps = []
    fr = lambda: "[" + ",".join(f"({v},s{s})" for v, s, p in sorted(h.a)) + "]"
    while len(h):
        v, s, p = h.poll()[0]
        out.append(v)
        note = f"The front {v} of source {s} is polled and written."
        if p + 1 < len(sources[s]):
            h.offer((sources[s][p + 1], s, p + 1))
            note += f" Its successor {sources[s][p + 1]} enters the frontier."
        else:
            note += f" Source {s} is exhausted, so nothing is offered."
        steps.append({"at": {"polled": off[s] + p}, "vars": {"frontier": fr(), "output": fmt(out)}, "note": note})
    return flat, steps, out


flat, steps, out = merge([[1, 4, 7], [2, 4, 9], [3, 8]])
assert out == [1, 2, 3, 4, 4, 7, 8, 9]
fill(CH, F, block(flat, ["polled"], steps), "@@TRACE1@@")
flat, steps, out = merge([[1, 2, 3, 4], [10], [5, 6]])
assert out == [1, 2, 3, 4, 5, 6, 10]
fill(CH, F, block(flat, ["polled"], steps), "@@TRACE2@@")
