from common import *
CH = '01-arrays-core-operations'
F = '09-in-place-sign-marking.md'

def scan(nums, report_dups):
    a = list(nums)
    steps, dups = [], []
    for i in range(len(a)):
        v = abs(a[i])
        s = v - 1
        arr = lambda: ",".join(map(str, a))
        if a[s] > 0:
            a[s] = -a[s]
            note = f"Value {v} marks cell {s}, which turns negative."
        else:
            note = f"Cell {s} is already negative, so {v} has a second visit."
            if report_dups:
                dups.append(v)
                note += f" Report {v}."
        steps.append({"at": {"i": i}, "vars": {"value": v, "slot": s, "array": arr()}, "note": note})
    return a, steps, dups

t1 = [2, 4, 2, 6, 1, 1]
a, s, _ = scan(t1, False)
missing = [i + 1 for i in range(len(a)) if a[i] > 0]
assert missing == [3, 5] and missing == [v for v in range(1, 7) if v not in t1]
s.append({"at": {"i": len(t1)}, "vars": {"array": ",".join(map(str, a))}, "note": "Cells 2 and 4 are still positive, so 3 and 5 never appeared."})
fill(CH, F, block(t1, ["i"], s), "@@TRACE1@@")
t2 = [5, 3, 5, 1, 3]
a, s, d = scan(t2, True)
assert d == [5, 3]
s.append({"at": {"i": len(t2)}, "vars": {"array": ",".join(map(str, a))}, "note": "The scan ends with the repeated values 5 and 3 reported."})
fill(CH, F, block(t2, ["i"], s), "@@TRACE2@@")
