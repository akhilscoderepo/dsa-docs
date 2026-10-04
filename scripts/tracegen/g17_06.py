from common import *
from hp import *
CH = '17-heaps-and-priority-queues'
F = '06-lazy-deletion.md'


def run(ops):
    h = Heap()
    pending = {}
    out = []
    steps = []
    pend = lambda: "{" + ",".join(f"{k}:{v}" for k, v in sorted(pending.items()) if v) + "}"
    for i, op in enumerate(ops):
        if op > 0:
            h.offer(op)
            note = f"Add {op}. It is inserted into the heap and nothing else changes."
        elif op < 0:
            v = -op
            pending[v] = pending.get(v, 0) + 1
            note = f"Remove {v}. Only the pending count of {v} rises to {pending[v]}, and the heap is not touched."
        else:
            dropped = []
            while len(h) and pending.get(h.peek(), 0) > 0:
                t = h.peek()
                pending[t] -= 1
                h.poll()
                dropped.append(t)
            res = h.peek() if len(h) else -1
            out.append(res)
            if dropped:
                note = "Query. The cleanup discards the stale root " + ", ".join(map(str, dropped)) + f" and then finds a live root, so the minimum is {res}."
            else:
                note = f"Query. The root {res} is live, so no cleanup is needed and the minimum is {res}."
        steps.append({"at": {"i": i}, "vars": {"heap": fmt(sorted(h.a)), "pending": pend(), "output": fmt(out)}, "note": note})
    return steps, out


a = [5, 3, 8, -3, 0, -5, 0]
s, out = run(a)
assert out == [5, 8], out
fill(CH, F, block(a, ["i"], s), "@@TRACE1@@")
b = [4, 4, 6, -4, 0, -4, 0]
s, out = run(b)
assert out == [4, 6], out
fill(CH, F, block(b, ["i"], s), "@@TRACE2@@")
