import sys
from common import *
from hp import *
CH = '17-heaps-and-priority-queues'
F = '08-heap-and-intervals.md'


def run(acts, closed):
    acts = sorted(acts, key=lambda a: a[0])
    h = Heap()
    steps = []
    for i, (s, e) in enumerate(acts):
        free = len(h) and ((h.peek() < s) if closed else (h.peek() <= s))
        if free:
            old = h.poll()[0]
            op = "<" if closed else "at most"
            note = f"Act [{s},{e}] starts at {s}. The root {old} is {'strictly below' if closed else 'not above'} the start, so that stage is reused and its end {old} is replaced by {e}."
        else:
            if len(h):
                note = f"Act [{s},{e}] starts at {s}. The root {h.peek()} is {'not below' if closed else 'above'} the start, so every stage is busy and a new stage is opened with end {e}."
            else:
                note = f"Act [{s},{e}] starts at {s}. No stage exists yet, so one is opened with end {e}."
        h.offer(e)
        steps.append({"at": {"i": i}, "vars": {"ends": fmt(sorted(h.a)), "stages": len(h)}, "note": note})
    return [a[0] for a in acts], steps, len(h)


cells, steps, n = run([[1, 4], [2, 6], [4, 7], [5, 9], [8, 10]], False)
assert n == 3
fill(CH, F, block(cells, ["i"], steps), "@@TRACE1@@")
cells, steps, n = run([[1, 3], [3, 6], [4, 8], [6, 9]], True)
assert n == 3 and run([[1, 3], [3, 6], [4, 8], [6, 9]], False)[2] == 2
fill(CH, F, block(cells, ["i"], steps), "@@TRACE2@@")


def minint(intervals, queries):
    out = []
    for q in queries:
        best = -1
        for l, r in intervals:
            if l <= q <= r and (best < 0 or r - l + 1 < best):
                best = r - l + 1
        out.append(best)
    return out


print(minint([[2, 5], [1, 3], [6, 9], [3, 3]], [3, 1, 6, 10, 4]), minint([[4, 4]], [4, 5]), file=sys.stderr)
