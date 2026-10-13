from common import *
import heapq
CH = '38-streaming-and-temporal-state'
NAME = '92-ordered-stream-state.md'

# Trace 1: keep the three largest values of an append-only stream with a min-heap.
stream = [12, 4, 9, 20, 1, 7, 15]
k = 3
heap = []
steps = [{"at": {"i": -1}, "vars": {"top": "[]", "boundary": "none"}, "note": "Start: the heap is empty and no boundary exists."}]
seen = []
for i, v in enumerate(stream):
    seen.append(v)
    if len(heap) < k:
        heapq.heappush(heap, v)
        why = f"The heap holds fewer than {k} values, so {v} is admitted."
    elif v > heap[0]:
        old = heapq.heapreplace(heap, v)
        why = f"The value {v} beats the boundary {old}, so it replaces the root {old}."
    else:
        why = f"The value {v} does not beat the boundary {heap[0]}, so the heap stays unchanged."
    assert sorted(heap) == sorted(seen)[-k:]
    bnd = str(heap[0]) if len(heap) == k else "none"
    steps.append({"at": {"i": i}, "vars": {"top": "[" + ",".join(map(str, sorted(heap))) + "]", "boundary": bnd}, "note": why})
assert heap[0] == 12
fill(CH, NAME, block([str(x) for x in stream], ["i"], steps), "@@TRACE1@@")

# Trace 2: lazy max-heap over a correctable stream.
ops = [("set", "a", 30), ("set", "b", 50), ("set", "b", 20), ("max",), ("erase", "a"), ("max",), ("set", "a", 25), ("max",)]
truth = {}
h = []
def fmt(d): return "{" + ",".join(f"{k}={v}" for k, v in sorted(d.items())) + "}"
def hs(): return "[" + ",".join(f"{-v}{k}" for v, k in sorted(h)) + "]"
steps = [{"at": {"op": -1}, "vars": {"truth": "{}", "heap": "[]"}, "note": "Start: no key has a value and the heap is empty."}]
cells = []
for j, op in enumerate(ops):
    if op[0] == "set":
        truth[op[1]] = op[2]
        heapq.heappush(h, (-op[2], op[1]))
        cells.append(f"set {op[1]} {op[2]}")
        note = f"The truth for {op[1]} becomes {op[2]}, and one new entry is pushed. Any older entry for {op[1]} is now stale."
        st = {"truth": fmt(truth), "heap": hs()}
    elif op[0] == "erase":
        del truth[op[1]]
        cells.append(f"erase {op[1]}")
        note = f"The key {op[1]} leaves the truth. Its entries stay in the heap and are now stale."
        st = {"truth": fmt(truth), "heap": hs()}
    else:
        cells.append("max")
        dropped = []
        while h and truth.get(h[0][1]) != -h[0][0]:
            dropped.append(f"{-h[0][0]}{h[0][1]}")
            heapq.heappop(h)
        ans = -h[0][0]
        assert ans == max(truth.values())
        if dropped:
            note = f"The query discards the stale root {', '.join(dropped)} and finds the live root {ans}, which agrees with the truth."
        else:
            note = f"The root {ans} agrees with the truth, so nothing is discarded."
        st = {"truth": fmt(truth), "heap": hs(), "answer": str(ans)}
    steps.append({"at": {"op": j}, "vars": st, "note": note})
fill(CH, NAME, block(cells, ["op"], steps), "@@TRACE2@@")
