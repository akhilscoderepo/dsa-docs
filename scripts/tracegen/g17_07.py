from common import *
from hp import *
CH = '17-heaps-and-priority-queues'
F = '07-running-median.md'


def run(vals):
    lo = Heap(key=lambda x: -x)
    hi = Heap()
    steps = []
    meds = []
    for i, v in enumerate(vals):
        lo.offer(v)
        c = lo.poll()[0]
        hi.offer(c)
        parts = [f"Reading {v} is offered to the lower half, and its root {c} crosses to the upper half."]
        if len(hi) > len(lo):
            b = hi.poll()[0]
            lo.offer(b)
            parts.append(f"The upper half is now larger, so its root {b} moves back to the lower half.")
        else:
            parts.append("The sizes already satisfy the rule, so nothing moves back.")
        if len(lo) > len(hi):
            m = lo.peek()
            parts.append(f"The count is odd, so the median is the lower root {m}.")
        else:
            m = (lo.peek() + hi.peek()) / 2
            parts.append(f"The count is even, so the median is the average of {lo.peek()} and {hi.peek()}, which is {m}.")
        meds.append(m)
        steps.append({"at": {"i": i}, "vars": {"lower": fmt(sorted(lo.a, reverse=True)), "upper": fmt(sorted(hi.a)), "median": m}, "note": " ".join(parts)})
    return steps, meds, lo, hi


a = [5, 15, 1, 3, 8, 7]
s, meds, lo, hi = run(a)
assert meds == [5, 10.0, 5, 4.0, 5, 6.0], meds
assert sorted(lo.a) == [1, 3, 5] and sorted(hi.a) == [7, 8, 15]
fill(CH, F, block(a, ["i"], s), "@@TRACE1@@")
b = [9, 7, 5, 3, 1]
s, meds, lo, hi = run(b)
assert meds == [9, 8.0, 7, 6.0, 5], meds
fill(CH, F, block(b, ["i"], s), "@@TRACE2@@")
