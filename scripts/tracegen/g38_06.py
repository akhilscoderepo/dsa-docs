from common import *
import bisect
CH = '38-streaming-and-temporal-state'
NAME = '06-temporal-indexes.md'

def lower_bound(a, x, log, label):
    lo, hi = 0, len(a)
    log(lo, hi, None, f"{label}: search the first index whose time is at least {x}. The window is [0, {len(a)}).")
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] < x:
            lo = mid + 1
            log(lo, hi, mid, f"a[{mid}] is {a[mid]}, below {x}, so lo moves to {lo}.")
        else:
            hi = mid
            log(lo, hi, mid, f"a[{mid}] is {a[mid]}, at least {x}, so hi moves to {hi}.")
    assert lo == bisect.bisect_left(a, x)
    return lo

def search_trace():
    a = [3, 3, 8, 14, 15, 15, 27, 40]
    st = []
    def log(lo, hi, mid, note, tag=None):
        st.append({"at": {"lo": lo, "hi": hi, "mid": -1 if mid is None else mid},
                   "vars": {"target": cur[0], "result": "open"}, "note": note})
    cur = [8]
    i = lower_bound(a, 8, log, "Start of query [8, 28)")
    st[-1]["vars"]["result"] = f"first = {i}"
    cur[0] = 28
    j = lower_bound(a, 28, log, "End of query [8, 28)")
    st[-1]["vars"]["result"] = f"stop = {j}"
    assert j - i == len([x for x in a if 8 <= x < 28]) == 5
    st.append({"at": {"lo": i, "hi": j, "mid": -1}, "vars": {"target": "none", "result": f"count = {j - i}"},
               "note": f"The events at indexes {i} through {j - 1} lie inside [8, 28), so the count is {j} minus {i}, which is {j - i}."})
    return block(a, ["lo", "hi", "mid"], st)

def bucket_trace():
    a = [2, 2, 9, 31, 33, 58]; frm, to, size = 0, 59, 10
    nb = (to - frm) // size + 1
    assert nb == 6
    st = []
    out = []
    first = bisect.bisect_left(a, frm)
    st.append({"at": {"i": first}, "vars": {"bucket": "none", "nonEmpty": "[]"},
               "note": "Binary search places i on the first event at or after time 0. The query has 6 buckets of width 10."})
    i = first
    while i < len(a) and a[i] <= to:
        b = (a[i] - frm) // size
        start = i
        while i < len(a) and a[i] <= to and (a[i] - frm) // size == b:
            i += 1
        out.append((frm + b * size, i - start))
        shown = "[" + ",".join(f"{s}:{c}" for s, c in out) + "]"
        st.append({"at": {"i": i}, "vars": {"bucket": b, "nonEmpty": shown},
                   "note": f"Events {start} through {i - 1} share bucket {b}, which starts at {frm + b * size}. The walk records {i - start} and jumps to index {i}."})
    ref = {}
    for x in a:
        ref[(x - frm) // size] = ref.get((x - frm) // size, 0) + 1
    assert [(s, c) for s, c in out] == [(frm + k * size, c) for k, c in sorted(ref.items())]
    full = [ref.get(k, 0) for k in range(nb)]
    assert full == [3, 0, 0, 2, 0, 1]
    st.append({"at": {"i": len(a)}, "vars": {"bucket": "none", "nonEmpty": "[0:3,30:2,50:1]"},
               "note": "The walk touched 3 buckets and no empty one. Buckets 1, 2 and 4 are absent from the list, so each of them has count 0."})
    return block(a, ["i"], st)

fill(CH, NAME, search_trace(), "@@TRACE1@@")
fill(CH, NAME, bucket_trace(), "@@TRACE2@@")
