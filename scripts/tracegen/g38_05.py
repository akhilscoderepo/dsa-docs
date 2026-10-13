from common import *
CH = '38-streaming-and-temporal-state'
NAME = '05-frequency-streams.md'

def fmt(d):
    return " ".join(f"{k}:{v}" for k, v in sorted(d.items())) or "empty"

def book_trace():
    ops = [("add", 4), ("add", 7), ("add", 4), ("has", 2), ("del", 4), ("has", 2), ("del", 7), ("del", 7), ("has", 1)]
    counts = {}; tally = {}
    def shift(v, a, b):
        if a > 0:
            tally[a] -= 1
            if tally[a] == 0: del tally[a]
        if b > 0: tally[b] = tally.get(b, 0) + 1
        if b == 0: del counts[v]
        else: counts[v] = b
    st = [{"at": {"op": -1}, "vars": {"counts": "empty", "tally": "empty", "answer": "none"}, "note": "Start: both maps are empty."}]
    expect = {3: True, 5: False, 8: True}
    for i, (o, a) in enumerate(ops):
        ans = "none"; note = ""
        c = counts.get(a, 0)
        if o == "add":
            shift(a, c, c + 1); note = f"add {a} moves its count from {c} to {c+1} in both maps."
        elif o == "del":
            if c > 0:
                shift(a, c, c - 1)
                note = f"del {a} moves its count from {c} to {c-1}" + (" and removes the key, with no tally entry for 0." if c == 1 else " in both maps.")
            else:
                note = f"del {a} finds no key, so nothing changes."
        else:
            r = tally.get(a, 0) > 0; ans = str(r).lower()
            assert r == (a in counts.values())
            note = f"has {a} reads tally[{a}], which is {tally.get(a, 0)}, so the answer is {ans}."
            if i in expect: assert r == expect[i]
        # tally always equals recount
        rec = {}
        for v in counts.values(): rec[v] = rec.get(v, 0) + 1
        assert rec == tally and 0 not in tally and all(x > 0 for x in counts.values())
        st.append({"at": {"op": i}, "vars": {"counts": fmt(counts), "tally": fmt(tally), "answer": ans}, "note": note})
    assert counts == {4: 1} and st[-1]["vars"]["answer"] == "true"
    return block([f"{o} {a}" for o, a in ops], ["op"], st)

def first_trace():
    ops = [("add", 5), ("add", 3), ("add", 5), ("first", 0), ("add", 2), ("add", 3), ("first", 0), ("add", 2), ("first", 0), ("add", 7), ("first", 0)]
    counts = {}; order = []; seq = []
    st = [{"at": {"op": -1}, "vars": {"order": "empty", "answer": "none"}, "note": "Start: the queue is empty."}]
    for i, (o, a) in enumerate(ops):
        ans = "none"
        if o == "add":
            seq.append(a); counts[a] = counts.get(a, 0) + 1
            if counts[a] == 1:
                order.append(a); note = f"add {a} gives count 1, so {a} enters the queue."
            else:
                note = f"add {a} raises its count to {counts[a]} and pushes nothing, so {a} in the queue is now stale."
        else:
            pops = []
            while order and counts[order[0]] != 1: pops.append(order.pop(0))
            res = order[0] if order else -1
            oracle = next((v for v in seq if seq.count(v) == 1), -1)
            assert res == oracle
            ans = str(res)
            note = ("first pops stale " + ", ".join(map(str, pops)) + f" and returns {res}." if pops else f"first finds the front {res} with count 1 and returns it.") if res != -1 else "first pops stale " + ", ".join(map(str, pops)) + ", finds an empty queue and returns -1."
        st.append({"at": {"op": i}, "vars": {"order": " ".join(map(str, order)) or "empty", "answer": ans}, "note": note})
    return block([f"{o} {a}" if o == "add" else "first" for o, a in ops], ["op"], st)

fill(CH, NAME, book_trace(), "@@TRACE1@@")
fill(CH, NAME, first_trace(), "@@TRACE2@@")
