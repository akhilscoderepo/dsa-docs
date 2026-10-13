from common import *
CH = '37-iterators-encodings-and-versioned-state'
F = '04-version-histories.md'


def floor_trace(versions, values, q):
    n = len(versions)
    lo, hi = 0, n
    st = [{"at": {"lo": 0, "hi": n, "mid": -1}, "vars": {"query": q},
           "note": f"Start: the window covers all {n} versions, and the query asks for version {q}."}]
    while lo < hi:
        mid = (lo + hi) // 2
        if versions[mid] <= q:
            st.append({"at": {"lo": lo, "hi": hi, "mid": mid}, "vars": {"query": q, "version": versions[mid]},
                       "note": f"Version {versions[mid]} at index {mid} is at most {q}, so the first greater version lies to the right and lo becomes {mid + 1}."})
            lo = mid + 1
        else:
            st.append({"at": {"lo": lo, "hi": hi, "mid": mid}, "vars": {"query": q, "version": versions[mid]},
                       "note": f"Version {versions[mid]} at index {mid} is above {q}, so the first greater version is at index {mid} or earlier and hi becomes {mid}."})
            hi = mid
    ans = values[lo - 1] if lo else -1
    st.append({"at": {"lo": lo, "hi": hi, "mid": lo}, "vars": {"query": q, "answer": ans},
               "note": f"The window is empty. The first greater version is at index {lo}, so the answer slot is index {lo - 1} and the value is {ans}."})
    return block([str(v) for v in versions], ["lo", "hi", "mid"], st), ans


def snap_trace():
    start = 0
    ops = ["set(0,5)", "set(0,6)", "snap", "set(1,4)", "snap", "get(1,0)", "get(1,1)", "get(2,1)"]
    pending = {}; hist = {0: [], 1: [], 2: []}; snaps = 0; out = []
    fmt = lambda d: "{" + ", ".join(f"{k}:{v}" for k, v in sorted(d.items())) + "}"
    H = lambda: "; ".join(f"c{i}={hist[i] if hist[i] else '[]'}" for i in range(3)).replace(" ", "")
    st = []
    def get(i, s):
        if s >= snaps: return -1
        best = start
        for v, x in hist[i]:
            if v <= s: best = x
        return best
    for k, op in enumerate(ops):
        if op.startswith("set"):
            i, v = map(int, op[4:-1].split(","))
            note = f"Write {v} to cell {i}. " + ("The pending table replaces the earlier entry for this cell." if i in pending else "The pending table gets a new entry.")
            pending[i] = v
        elif op == "snap":
            for i, v in sorted(pending.items()): hist[i].append((snaps, v))
            pending = {}
            note = f"Snapshot id {snaps}: each pending entry moves into the history of its cell with version {snaps}."
            snaps += 1
        else:
            i, s = map(int, op[4:-1].split(","))
            r = get(i, s); out.append(r)
            note = f"Query cell {i} at snapshot {s}: the floor search returns {r}" + (", the starting value, because no stored version is at most " + str(s) + "." if r == start else ".")
        st.append({"at": {"op": k}, "vars": {"pending": fmt(pending), "histories": H()}, "note": note})
    assert out == [0, 4, 0], out
    return block(ops, ["op"], st)


t1, ans = floor_trace([2, 5, 9, 14, 20], [30, 10, 40, 20, 50], 11)
assert ans == 40
fill(CH, F, t1, "@@TRACE1@@")
fill(CH, F, snap_trace(), "@@TRACE2@@")
