from common import *
from hp import *
CH = '17-heaps-and-priority-queues'
F = '02-heap-orientation.md'

# trace 1: minutes then ticket
mins = [5, 2, 5, 1, 2]
h = Heap(key=lambda t: (t[0], t[1]))
for i, m in enumerate(mins):
    h.offer((m, i))
steps = []
order = []
tup = lambda items: "[" + ",".join(f"({m},{i})" for m, i in sorted(items)) + "]"
while len(h):
    top, _, _ = h.poll()
    order.append(top[1])
    note = f"Ticket {top[1]} needs {top[0]} minutes and leaves."
    ties = [x for x in h.a if x[0] == top[0]]
    if ties:
        note += f" Another ticket needs {top[0]} minutes as well, and the smaller ticket number decided."
    steps.append({"at": {"picked": top[1]}, "vars": {"left": tup(h.a) if h.a else "[]", "order": fmt(order)}, "note": note})
assert order == [3, 1, 4, 0, 2], order
fill(CH, F, block(mins, ["picked"], steps), "@@TRACE1@@")

# trace 2: max-first with extremes
w = [2147483647, -2147483648, 0, 7]
idx = sorted(range(len(w)), key=lambda i: -w[i])
steps = []
out = []
rest = list(range(len(w)))
for i in idx:
    out.append(w[i])
    rest.remove(i)
    extra = ""
    if w[i] == -2147483648:
        extra = " Under negation this weight would have looked like the lightest crate and left first."
    steps.append({"at": {"picked": i}, "vars": {"order": fmt(out), "left": len(rest)}, "note": f"Weight {w[i]} is the largest that remains, so it leaves.{extra}"})
assert idx == [0, 3, 2, 1]
fill(CH, F, block(w, ["picked"], steps), "@@TRACE2@@")

# examples for exercises (printed for the writer)
import sys
tasks = [[2, 3], [0, 6], [3, 1], [3, 1], [20, 2]]
def cpu(tasks):
    n = len(tasks)
    srt = sorted(range(n), key=lambda i: (tasks[i][0], i))
    t = 0; p = 0; out = []; hh = Heap(key=lambda x: x)
    while len(out) < n:
        if not len(hh) and p < n and tasks[srt[p]][0] > t:
            t = tasks[srt[p]][0]
        while p < n and tasks[srt[p]][0] <= t:
            i = srt[p]; hh.offer((tasks[i][1], i)); p += 1
        d, i = hh.poll()[0]
        t += d; out.append(i)
    return out
print(cpu(tasks), cpu([[1, 2], [1, 2], [1, 2]]), file=sys.stderr)
assert cpu(tasks) == [1, 2, 3, 0, 4]
