from common import *
CH = '36-stateful-containers-and-histories'
FILE = '91-containers-and-api-state.md'


class Q:
    # Simulates the ring plus index; safe=False adds the id to the index before the full check.
    def __init__(self, cap, safe):
        self.cap, self.safe = cap, safe
        self.slots = [None] * cap
        self.head = self.size = 0
        self.index = set()

    def offer(self, v):
        if self.safe:
            if v in self.index:
                return 2
            if self.size == self.cap:
                return 1
        else:
            if v in self.index:
                return 2
            self.index.add(v)
            if self.size == self.cap:
                return 1
        self.slots[(self.head + self.size) % self.cap] = v
        self.size += 1
        self.index.add(v)
        return 0

    def poll(self):
        if self.size == 0:
            return -1
        v = self.slots[self.head]
        self.head = (self.head + 1) % self.cap
        self.size -= 1
        self.index.discard(v)
        return v

    def live(self):
        return [self.slots[(self.head + i) % self.cap] for i in range(self.size)]


def run(cap, calls, safe, expect):
    q = Q(cap, safe)
    nxt = lambda: (q.head + q.size) % cap
    show = lambda: "[" + ",".join("-" if x is None else str(x) for x in q.slots) + "]"
    st = [{"at": {"head": 0, "next": 0}, "vars": {"slots": show(), "size": 0, "index": "{}", "result": "start"},
           "note": "Start: every slot is empty, and the index is empty."}]
    got = []
    for op, v in calls:
        if op == "offer":
            r = q.offer(v)
            code = {0: "accepted", 1: "full", 2: "duplicate"}[r]
            note = f"offer({v}) returns {r}, {code}."
            if r == 0:
                note += f" The id enters slot {(q.head + q.size - 1) % cap}, size becomes {q.size}, and the index gains {v}."
            elif not safe and r == 1:
                note += f" The set already gained {v} before the full check, so the index no longer matches the live window."
            elif r == 2 and not safe and v not in q.live():
                note += f" The id {v} is not queued, so this answer is wrong: a correct queue accepts it."
            else:
                note += " No field changed."
        else:
            r = q.poll()
            note = f"poll() returns {r}. The head moves to slot {q.head}, size becomes {q.size}, and the index drops {r}."
        got.append(r)
        idx = "{" + ",".join(map(str, sorted(q.index))) + "}"
        st.append({"at": {"head": q.head, "next": nxt()},
                   "vars": {"slots": show(), "size": q.size, "index": idx, "result": r}, "note": note})
        assert q.size <= cap and all(0 <= p["at"]["head"] <= cap and 0 <= p["at"]["next"] <= cap for p in st)
    assert got == expect, got
    return q, st


def correct_oracle(cap, calls):
    from collections import deque
    d, out = deque(), []
    for op, v in calls:
        if op == "offer":
            out.append(2 if v in d else 1 if len(d) == cap else (d.append(v), 0)[1])
        else:
            out.append(d.popleft() if d else -1)
    return out


calls1 = [("offer", 7), ("offer", 9), ("offer", 7), ("offer", 4), ("offer", 5), ("poll", 0),
          ("offer", 5), ("poll", 0), ("offer", 7)]
exp1 = [0, 0, 2, 0, 1, 7, 0, 9, 0]
assert correct_oracle(3, calls1) == exp1
q1, st1 = run(3, calls1, True, exp1)
assert q1.live() == [4, 5, 7] and q1.slots == [5, 7, 4] and q1.index == {4, 5, 7}
assert st1[4]["at"] == {"head": 0, "next": 0} and st1[0]["at"] == {"head": 0, "next": 0}

calls2 = [("offer", 5), ("offer", 6), ("offer", 7), ("offer", 8), ("poll", 0), ("offer", 8)]
good = correct_oracle(3, calls2)
assert good == [0, 0, 0, 1, 5, 0]
q2, st2 = run(3, calls2, False, [0, 0, 0, 1, 5, 2])
assert 8 in q2.index and 8 not in q2.live()

fill(CH, FILE, block(["0", "1", "2"], ["head", "next"], st1), "@@TRACE1@@")
fill(CH, FILE, block(["0", "1", "2"], ["head", "next"], st2), "@@TRACE2@@")
