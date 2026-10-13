from common import *
import itertools, collections
from math import factorial
CH = '38-streaming-and-temporal-state'
NAME = '07-randomized-evolution.md'

# Facts quoted in the lesson text, recomputed here.
def biased_counts(n):
    c = collections.Counter()
    for js in itertools.product(range(n), repeat=n):
        a = list(range(n))
        for i, j in enumerate(js):
            a[i], a[j] = a[j], a[i]
        c[tuple(a)] += 1
    return c
c3 = biased_counts(3)
assert sum(c3.values()) == 27 and len(c3) == 6
assert sorted(c3.values()) == [4, 4, 4, 5, 5, 5]
assert c3[(0, 1, 2)] == 4 and c3[(1, 2, 0)] == 5          # orders 1,2,3 and 2,3,1
c4 = biased_counts(4)
assert sum(c4.values()) == 256 and min(c4.values()) == 8 and max(c4.values()) == 15
assert round(256 / 24, 2) == 10.67
for n in range(3, 14):
    assert (n ** n) % factorial(n) != 0 and factorial(n) % (n - 1) == 0

def fy(a, draws):
    a = list(a); n = len(a); k = 0
    for i in range(n - 1):
        j = i + draws[k]; assert 0 <= draws[k] < n - i; k += 1
        a[i], a[j] = a[j], a[i]
    assert k == len(draws)
    return a
# Exercise examples.
assert fy([3, 1, 2], [2, 0]) == [2, 1, 3]
assert fy([8, 8, 5, 0], [1, 2, 0]) == [8, 0, 5, 8]
assert fy([1, 2, 3], [1, 1]) == [2, 3, 1] and fy([1, 2, 3], [2, 1]) == [3, 1, 2]
a = [4, 7, 9]; a[1], a[2] = a[2], a[1]; assert a == [4, 9, 7]
a = [5, 5, 2]; a[0], a[2] = a[2], a[0]; assert a == [2, 5, 5]
# Every draw sequence gives a distinct order, so n! orders each appear once.
for n in range(1, 7):
    outs = set()
    for ds in itertools.product(*[range(n - i) for i in range(n - 1)]):
        outs.add(tuple(fy(range(n), list(ds))))
    assert len(outs) == factorial(n)
# Reservoir example.
held = None
for t, (v, d) in enumerate(zip([5, 8, 3], [0, 1, 0]), 1):
    if d == 0: held = v
assert held == 3

def shuffle_steps(work, draws, snap, label):
    st = []; n = len(work); k = 0
    for i in range(n - 1):
        d = draws[k]; k += 1
        j = i + d; assert 0 <= d < n - i
        work[i], work[j] = work[j], work[i]
        if j == i:
            note = f"Bound {n - i}, draw {d}, so j equals i and {work[i]} stays at position {i}."
        else:
            note = f"Bound {n - i}, draw {d}, so j is {j} and positions {i} and {j} swap."
        st.append({"at": {"i": i, "j": j}, "vars": {"snapshot": snap, "bound": n - i, "draw": d}, "note": note})
    return st

def trace1():
    letters = ["K", "L", "M", "N"]
    w = list(letters)
    st = [{"at": {"i": -1, "j": -1}, "vars": {"bound": "none", "draw": "none"}, "note": "Start: the array is K L M N and no step has run."}]
    # The cells change per step, so describe the array in vars.
    draws = [2, 0, 1]
    for s in shuffle_steps(w, draws, "-", ""):
        s["vars"].pop("snapshot"); s["vars"]["array"] = " ".join(w) if False else ""
        st.append(s)
    # Recompute array text per step.
    w = list(letters); n = 4
    for idx, i in enumerate(range(n - 1)):
        j = i + draws[idx]; w[i], w[j] = w[j], w[i]
        st[idx + 1]["vars"]["array"] = " ".join(w)
    st[0]["vars"]["array"] = "K L M N"
    assert w == ["M", "L", "N", "K"] == fy(letters, draws)
    st.append({"at": {"i": 3, "j": 3}, "vars": {"bound": 1, "draw": "none", "array": " ".join(w)}, "note": "The frontier reaches position 3. One value is left, so no draw is needed and the result is M L N K."})
    return block(letters, ["i", "j"], st)

def trace2():
    base = [7, 2, 9, 2]; snap = " ".join(map(str, base))
    work = list(base)
    st = [{"at": {"i": -1, "j": -1}, "vars": {"snapshot": snap, "array": snap, "call": "new"}, "note": "The constructor copies the input twice. Snapshot and working array both read 7 2 9 2."}]
    def run(draws, first):
        n = len(work)
        for idx in range(n - 1):
            i = idx; d = draws[idx]; j = i + d
            assert 0 <= d < n - i
            work[i], work[j] = work[j], work[i]
            same = "Draw %d from bound %d gives j = %d" % (d, n - i, j)
            note = same + (", so the value stays at position %d." % i if j == i else ", so positions %d and %d swap." % (i, j))
            st.append({"at": {"i": i, "j": j}, "vars": {"snapshot": snap, "array": " ".join(map(str, work)), "call": "shuffle()"}, "note": note})
    run([2, 0, 1], True)
    assert work == fy(base, [2, 0, 1]) == [9, 2, 2, 7]
    work[:] = base
    st.append({"at": {"i": -1, "j": -1}, "vars": {"snapshot": snap, "array": snap, "call": "reset()"}, "note": "reset copies the snapshot into the working array. The snapshot never changed, so the array reads 7 2 9 2 again."})
    run([3, 2, 0], False)
    assert work == fy(base, [3, 2, 0]) == [2, 7, 9, 2]
    return block([str(x) for x in base], ["i", "j"], st)

fill(CH, NAME, trace1(), "@@TRACE1@@")
fill(CH, NAME, trace2(), "@@TRACE2@@")
