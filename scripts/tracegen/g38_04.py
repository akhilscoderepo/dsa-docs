from common import *
import heapq
CH = '38-streaming-and-temporal-state'
NAME = '04-stream-order-statistics.md'

def halves_trace():
    stream = [12, 4, 9, 20, 1, 7]
    lo, up = [], []          # lo is a max-heap through negation
    seen = []
    st = [{"at": {"i": -1}, "vars": {"lower": "[]", "upper": "[]", "median": "none"}, "note": "Start: both halves are empty."}]
    for i, x in enumerate(stream):
        seen.append(x)
        moved = ""
        if not lo or x <= -lo[0]:
            heapq.heappush(lo, -x); side = "lower"
        else:
            heapq.heappush(up, x); side = "upper"
        if len(lo) > len(up) + 1:
            v = -heapq.heappop(lo); heapq.heappush(up, v); moved = f" The lower half is too large, so its root {v} moves to the upper half."
        elif len(up) > len(lo):
            v = heapq.heappop(up); heapq.heappush(lo, -v); moved = f" The upper half is larger, so its root {v} moves to the lower half."
        assert len(lo) - len(up) in (0, 1)
        srt = sorted(seen)
        med = -lo[0]
        assert med == srt[(len(srt) - 1) // 2]
        assert not up or med <= up[0]
        lows = sorted((-v for v in lo), reverse=True)
        st.append({"at": {"i": i}, "vars": {"lower": str(lows).replace(" ", ""), "upper": str(sorted(up)).replace(" ", ""), "median": med},
                   "note": f"{x} enters the {side} half.{moved} The lower middle value is {med}."})
    assert -lo[0] == 7
    return block([str(v) for v in stream], ["i"], st)

def peak_trace():
    ev = [("A", 7), ("B", 9), ("A", 12), ("B", 4), ("A", 3)]
    ver = {}; heap = []
    st = [{"at": {"i": -1}, "vars": {"peak": "none", "heap": 0, "popped": 0}, "note": "Start: the heap and the version map are empty."}]
    cur = {}
    for i, (s, r) in enumerate(ev):
        ver[s] = ver.get(s, 0) + 1; cur[s] = r
        heapq.heappush(heap, (-r, s, ver[s]))
        popped = 0
        while ver[heap[0][1]] != heap[0][2]:
            heapq.heappop(heap); popped += 1
        pk = -heap[0][0]
        assert pk == max(cur.values())
        note = f"{s} records {r} as version {ver[s]}."
        note += (f" The query removed {popped} stale root{'s' if popped != 1 else ''}." if popped else " The root is current, so nothing is removed.")
        note += f" The peak is {pk}."
        st.append({"at": {"i": i}, "vars": {"peak": pk, "heap": len(heap), "popped": popped}, "note": note})
    return block([f"{s}={r}" for s, r in ev], ["i"], st)

t1, t2 = halves_trace(), peak_trace()
fill(CH, NAME, t1, "@@TRACE1@@")
fill(CH, NAME, t2, "@@TRACE2@@")
print(t2)
