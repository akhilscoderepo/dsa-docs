from common import *
CH = '01-arrays-core-operations'
F = '08-cyclic-placement.md'

def place(nums):
    a = list(nums)
    n = len(a)
    i, steps = 0, []
    while i < n:
        t = a[i] - 1
        has = 0 <= t < n
        before = ",".join(map(str, a))
        if has and a[t] != a[i]:
            v = a[i]
            a[i], a[t] = a[t], a[i]
            note = f"Swap: {v} goes to index {t} and {a[i]} comes back to index {i}. The new value at {i} is unexamined, so i stays."
            steps.append({"at": {"i": i}, "vars": {"target": t, "array": ",".join(map(str, a))}, "note": note})
        else:
            if not has:
                note = f"{a[i]} lies outside 1..{n}, so it has no target slot and the loop passes it."
            elif t == i:
                note = f"{a[i]} sits at its own target slot, index {t}, so it is settled."
            else:
                note = f"{a[i]} would go to index {t}, yet that cell holds {a[t]} already. The duplicate guard refuses the swap."
            steps.append({"at": {"i": i}, "vars": {"target": t, "array": before}, "note": note})
            i += 1
    steps.append({"at": {"i": n}, "vars": {"array": ",".join(map(str, a))}, "note": f"Done: i has passed the end and the array reads [{','.join(map(str, a))}]."})
    return a, steps

t1 = [3, 1, 4, 2]
a, s = place(t1)
assert a == [1, 2, 3, 4]
fill(CH, F, block(t1, ["i"], s), "@@TRACE1@@")
t2 = [2, 2, 7, 1]
a, s = place(t2)
assert a == [1, 2, 7, 2]
assert next(i for i in range(4) if a[i] != i + 1) + 1 == 3
fill(CH, F, block(t2, ["i"], s), "@@TRACE2@@")
