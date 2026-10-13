from common import *
from collections import deque
CH = '38-streaming-and-temporal-state'
NAME = '01-windowed-streams.md'

def count_trace():
    vals = [4, 1, 7, 2, 9, 5]; k = 3
    head, tail = 0, -1
    total = 0
    st = [{"at": {"head": 0, "tail": -1}, "vars": {"event": "start", "sum": 0, "size": 0, "average": "none"}, "note": "Start: the window is empty, so head is 0 and tail is -1."}]
    notes = [
        "4 enters; the window holds 1 value and the sum is 4.",
        "1 enters; the window holds 2 values and the sum is 5.",
        "7 enters; the window holds 3 values, which equals k, so nothing leaves.",
        "2 enters and the size 4 exceeds k, so 4 leaves; head moves to 1 and the sum is 10.",
        "9 enters and 1 leaves; head moves to 2 and the sum is 18.",
        "5 enters and 7 leaves; head moves to 3 and the sum is 16.",
    ]
    for i, v in enumerate(vals):
        tail = i; total += v
        if tail - head + 1 > k:
            total -= vals[head]; head += 1
        size = tail - head + 1
        assert total == sum(vals[head:tail + 1]) and size <= k
        avg = total / size
        st.append({"at": {"head": head, "tail": tail}, "vars": {"event": f"add {v}", "sum": total, "size": size, "average": f"{avg:.2f}"}, "note": notes[i]})
    assert total == 16 and (head, tail) == (3, 5)
    return block([str(v) for v in vals], ["head", "tail"], st)

def time_trace():
    times = [1, 3, 3, 8, 9, 13]; span = 5
    head, tail = 0, -1
    q = deque()
    st = [{"at": {"head": 0, "tail": -1}, "vars": {"event": "start", "cutoff": "none", "count": 0}, "note": "Start: no pings yet, so head is 0 and tail is -1."}]
    notes = [
        "The cutoff is -4, so nothing expires and the count is 1.",
        "The cutoff is -2, so nothing expires and the count is 2.",
        "A second ping at time 3 is a separate event; the cutoff is -2 and the count is 3.",
        "The cutoff is 3, so the pings at times 1, 3 and 3 expire; head moves to 3 and the count is 1.",
        "The cutoff is 4 and the oldest ping is 8, so nothing leaves and the count is 2.",
        "The cutoff is 8, so the ping at time 8 expires; head moves to 4 and the count is 2.",
    ]
    for i, t in enumerate(times):
        tail = i; q.append(t)
        cutoff = t - span
        while q and q[0] <= cutoff:
            q.popleft(); head += 1
        assert len(q) == sum(1 for u in times[:i + 1] if t - span < u <= t) == tail - head + 1
        st.append({"at": {"head": head, "tail": tail}, "vars": {"event": f"ping {t}", "cutoff": cutoff, "count": len(q)}, "note": notes[i]})
    assert (head, tail) == (4, 5)
    return block([str(t) for t in times], ["head", "tail"], st)

fill(CH, NAME, count_trace(), "@@TRACE1@@")
fill(CH, NAME, time_trace(), "@@TRACE2@@")
