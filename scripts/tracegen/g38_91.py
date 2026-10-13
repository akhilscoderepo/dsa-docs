from common import *
CH = '38-streaming-and-temporal-state'
NAME = '91-queue-time-window.md'

def run(span, events, calls, expect):
    """events: arrival-ordered (time, weight) list shown as cells; calls: (kind, time, weight, note)."""
    cells = ["t%d w%d" % e for e in events]
    queue = []          # indexes into events, oldest first
    total = 0; last = None; tail = -1; nxt = 0
    steps = []
    def Q(): return "[" + ",".join("t%d" % events[i][0] for i in queue) + "]"
    def snap(call, res, note):
        steps.append({"at": {"head": queue[0] if queue else len(cells), "tail": tail},
                      "vars": {"call": call, "result": res, "queue": Q(), "sum": total}, "note": note})
    snap("new(span=%d)" % span, "none", "Start: the queue is empty, the sum is 0, and no event has arrived.")
    results = []
    for kind, t, w, note in calls:
        label = ("add(%d,%d)" % (t, w)) if kind == "add" else ("score(%d)" % t)
        if last is not None and t < last:
            snap(label, "throws", note); results.append("throws"); continue
        last = t
        while queue and events[queue[0]][0] <= t - span:
            total -= events[queue.pop(0)][1]
        if kind == "add":
            assert events[nxt] == (t, w)
            queue.append(nxt); tail = nxt; nxt += 1; total += w
            snap(label, "none", note); results.append("none")
        else:
            snap(label, total, note); results.append(total)
        # oracle on the live window
        live = [e for e in events[:nxt] if e[0] > t - span]
        assert total == sum(e[1] for e in live), (label, total)
    assert results == expect, results
    return block(cells, ["head", "tail"], steps)

ev1 = [(2, 5), (4, 3), (9, 2), (12, 4), (14, 1), (22, 6)]
c1 = [("add", 2, 5, "The first event joins the empty queue. The sum becomes 5."),
      ("add", 4, 3, "The cutoff is -6, so nothing leaves. The event joins the back and the sum becomes 8."),
      ("add", 9, 2, "The cutoff is -1, so the queue is unchanged. The sum becomes 10."),
      ("score", 11, 0, "The cutoff is 1. The oldest event has time 2, which is greater, so nothing leaves and the score is the stored sum."),
      ("add", 12, 4, "The cutoff is 2. The event at time 2 is at or before it and leaves first, so the sum drops by 5. Then the new event joins."),
      ("add", 14, 1, "The cutoff is 4. The event at time 4 is on the border and leaves. The new event joins."),
      ("score", 20, 0, "The cutoff is 10. The event at time 9 leaves, and the events at times 12 and 14 stay."),
      ("add", 22, 6, "The cutoff is 12. The event at time 12 is on the border and leaves, so the queue holds the events at times 14 and 22.")]
b1 = run(10, ev1, c1, ["none", "none", "none", 10, "none", "none", 5, "none"])
fill(CH, NAME, b1, "@@TRACE1@@")

ev2 = [(3, 4), (3, 6), (8, 1), (21, 7)]
c2 = [("add", 3, 4, "The first event at time 3 joins the queue."),
      ("add", 3, 6, "An equal time is allowed. The second event at time 3 joins the back, and the sum is 10."),
      ("score", 8, 0, "The cutoff is 3. Both events at time 3 are at or before it, so both leave and the sum is 0."),
      ("add", 8, 1, "The queue is empty, so nothing leaves. The event at time 8 joins and the sum is 1."),
      ("score", 20, 0, "The cutoff is 15. The event at time 8 leaves, the queue is empty and the score is 0."),
      ("add", 10, 9, "Time 10 is smaller than the latest time 20, so the call throws. The queue and the sum do not change."),
      ("add", 21, 7, "The queue is empty. The event at time 21 joins and the sum is 7.")]
b2 = run(5, ev2, c2, ["none", "none", 0, "none", 0, "throws", "none"])
fill(CH, NAME, b2, "@@TRACE2@@")
