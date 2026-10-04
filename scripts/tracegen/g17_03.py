from common import *
from hp import *
CH = '17-heaps-and-priority-queues'
F = '03-top-k.md'


def run(vals, k):
    h = Heap()
    steps = []
    for i, v in enumerate(vals):
        if len(h) < k:
            h.offer(v)
            note = f"Score {v} arrives and the heap holds fewer than {k} items, so it is offered."
        elif v > h.peek():
            old = h.peek()
            h.poll()
            h.offer(v)
            note = f"Score {v} beats the boundary {old}, so the root is polled and {v} is offered."
        else:
            note = f"Score {v} does not beat the boundary {h.peek()}, so it is ignored."
        note += f" The boundary is now {h.peek()}."
        steps.append({"at": {"i": i}, "vars": {"kept": fmt(sorted(h.a)), "boundary": h.peek()}, "note": note})
    return h, steps


a = [5, 1, 9, 3, 7, 8, 2, 6]
h, s = run(a, 3)
assert sorted(h.a) == [7, 8, 9] and h.peek() == 7
fill(CH, F, block(a, ["i"], s), "@@TRACE1@@")
b = [9, 8, 7, 3, 2, 1]
h, s = run(b, 3)
assert sorted(h.a) == [7, 8, 9]
fill(CH, F, block(b, ["i"], s), "@@TRACE2@@")
