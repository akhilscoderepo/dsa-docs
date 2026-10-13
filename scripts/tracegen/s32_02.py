import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from common import block, fill

CH = '32-selection-and-ordered-data-techniques'
F = '02-partition-invariants.md'

def lomuto(a):
    a = list(a); hi = len(a) - 1; p = a[hi]; i = 0
    steps = [{"at": {"i": 0, "j": 0}, "vars": {"pivot": p, "arr": str(a)},
              "note": f"The pivot is {p}, the last value. The pointers i and j both start at slot 0."}]
    for j in range(hi):
        if a[j] < p:
            a[i], a[j] = a[j], a[i]; i += 1
            note = f"The value {a[i-1]} is below {p}, so it swaps with the slot at the old i and i moves to {i}."
        else:
            note = f"The value {a[j]} is not below {p}, so it stays in the large range."
        steps.append({"at": {"i": i, "j": j + 1}, "vars": {"pivot": p, "arr": str(a)}, "note": note})
    a[i], a[hi] = a[hi], a[i]
    steps.append({"at": {"i": i, "j": len(a)}, "vars": {"pivot": p, "arr": str(a)},
                  "note": f"The scan is done. The pivot swaps into slot {i}, which is its final index."})
    assert a[:i] == [x for x in a[:i] if x < p] and all(x >= p for x in a[i+1:]) and a[i] == p
    return list(range(1)), steps, a, i

def three(a, p):
    a = list(a); lt = i = 0; gt = len(a) - 1
    steps = [{"at": {"lt": 0, "i": 0, "gt": gt}, "vars": {"pivot": p, "arr": str(a)},
              "note": f"The pivot value is {p}. The unresolved region is the whole array."}]
    while i <= gt:
        v = a[i]
        if v < p:
            a[lt], a[i] = a[i], a[lt]; lt += 1; i += 1
            note = f"The value {v} is below {p}, so it swaps with slot lt. Both lt and i advance."
        elif v > p:
            a[i], a[gt] = a[gt], a[i]; gt -= 1
            note = f"The value {v} is above {p}, so it swaps with slot gt. Only gt moves, and i stays to examine the arrival."
        else:
            i += 1
            note = f"The value {v} equals {p}, so only i advances."
        steps.append({"at": {"lt": lt, "i": i, "gt": gt}, "vars": {"pivot": p, "arr": str(a)}, "note": note})
    assert all(x < p for x in a[:lt]) and all(x == p for x in a[lt:gt+1]) and all(x > p for x in a[gt+1:])
    assert sorted(a) == sorted([4, 7, 1, 4, 9, 2, 4, 0])
    return steps, a, lt, gt

A1 = [7, 2, 9, 4, 1, 8, 5]
_, s1, r1, idx = lomuto(A1)
assert idx == 3 and r1 == [2, 4, 1, 5, 9, 8, 7], r1
s2, r2, lt, gt = three([4, 7, 1, 4, 9, 2, 4, 0], 4)
assert (lt, gt) == (3, 5)
fill(CH, F, block(A1, ["i", "j"], s1), "@@TRACE1@@")
fill(CH, F, block([4, 7, 1, 4, 9, 2, 4, 0], ["lt", "i", "gt"], s2), "@@TRACE2@@")
print(r1, r2)
