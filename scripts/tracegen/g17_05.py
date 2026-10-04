import sys
from common import *
from hp import *
CH = '17-heaps-and-priority-queues'
F = '05-heap-scheduling.md'


def sched(jobs):
    n = len(jobs)
    srt = sorted(range(n), key=lambda i: (jobs[i][0], i))
    h = Heap(key=lambda e: (e[0], e[1]))
    clock = 0
    nxt = 0
    order = []
    steps = []
    for _ in range(n):
        parts = []
        if not len(h) and clock < jobs[srt[nxt]][0]:
            parts.append(f"The ready heap is empty, so the clock jumps from {clock} to {jobs[srt[nxt]][0]}.")
            clock = jobs[srt[nxt]][0]
        admitted = []
        while nxt < n and jobs[srt[nxt]][0] <= clock:
            i = srt[nxt]
            h.offer((jobs[i][1], i))
            admitted.append(i)
            nxt += 1
        if admitted:
            parts.append("Admitted: ticket" + ("s " if len(admitted) > 1 else " ") + ", ".join(map(str, admitted)) + ".")
        d, i = h.poll()[0]
        parts.append(f"Ticket {i} has the least minutes ({d}) among the ready rolls and starts at {clock}.")
        start = clock
        clock += d
        order.append(i)
        ready = "[" + ",".join(f"({m},t{t})" for m, t in sorted(h.a)) + "]"
        steps.append({"at": {"next": nxt}, "vars": {"clock": clock, "ready": ready, "order": fmt(order)}, "note": " ".join(parts) + f" The clock is now {clock}."})
    return steps, order


jobs = [(1, 3), (2, 2), (2, 1), (8, 2), (20, 1)]
steps, order = sched(jobs)
assert order == [0, 2, 1, 3, 4], order
cells = sorted(j[0] for j in jobs)
fill(CH, F, block(cells, ["next"], steps), "@@TRACE1@@")
jobs = [(5, 4), (5, 2), (5, 2), (5, 1)]
steps, order = sched(jobs)
assert order == [3, 1, 2, 0], order
fill(CH, F, block([5, 5, 5, 5], ["next"], steps), "@@TRACE2@@")


def servers_ref(servers, tasks):
    # second-by-second reference simulation
    busy = [0] * len(servers)
    q = []
    out = [None] * len(tasks)
    t = 0
    done = 0
    while done < len(tasks):
        if t < len(tasks):
            q.append(t)
        while q:
            free = [s for s in range(len(servers)) if busy[s] <= t]
            if not free:
                break
            s = min(free, key=lambda s: (servers[s], s))
            j = q.pop(0)
            out[j] = s
            busy[s] = t + tasks[j]
            done += 1
        t += 1
    return out


print(servers_ref([5, 1, 1, 4], [3, 1, 2, 2, 1, 4, 1]), servers_ref([2], [1, 1]), file=sys.stderr)
