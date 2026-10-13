import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from common import block, fill

CH = '32-selection-and-ordered-data-techniques'
NAME = '91-partition-and-selection.md'

def run(vals, r):
    a = list(vals)
    lo, hi = 0, len(a) - 1
    steps = [{"at": {"lo": lo, "hi": hi}, "vars": {"r": r, "array": str(a)},
              "note": f"The range is the whole array and the target rank is r = {r}."}]
    rnd = 0
    while True:
        rnd += 1
        pivot = a[lo + (hi - lo) // 2]
        lt, i, gt = lo, lo, hi
        while i <= gt:
            if a[i] < pivot:
                a[lt], a[i] = a[i], a[lt]; lt += 1; i += 1
            elif a[i] > pivot:
                a[i], a[gt] = a[gt], a[i]; gt -= 1
            else:
                i += 1
        if r < lt:
            move, nlo, nhi = "keep the smaller side", lo, lt - 1
        elif r > gt:
            move, nlo, nhi = "keep the larger side", gt + 1, hi
        else:
            move, nlo, nhi = "stop, the answer is the pivot", lo, hi
        steps.append({"at": {"lo": lo, "hi": hi},
                      "vars": {"pivot": pivot, "lt": lt, "gt": gt, "array": str(a), "move": move},
                      "note": f"Round {rnd} on indices {lo} to {hi} uses pivot {pivot}. The equal block covers indices {lt} to {gt}, and r = {r}, so the search will {move}."})
        if nlo == lo and nhi == hi:
            res = [pivot, lt, gt - lt + 1]
            steps.append({"at": {"lo": lo, "hi": hi},
                          "vars": {"value": pivot, "below": res[1], "equal": res[2]},
                          "note": f"The loop stops. The answer is {pivot}, with {res[1]} smaller entries and {res[2]} equal entries."})
            return res, steps
        lo, hi = nlo, nhi

def brute(vals, r):
    s = sorted(vals); v = s[r]
    return [v, sum(x < v for x in s), sum(x == v for x in s)]

t = pathlib.Path(__file__).resolve().parents[2] / 'dsa-skills' / 'manuscripts' / CH / NAME
res = {}
for ph, vals, r in (("@@TRACE1@@", [7, 2, 9, 2, 5, 7, 7, 1, 8], 6), ("@@TRACE2@@", [4, 4, 4, 3, 10, -6, 4, 8], 1)):
    out, steps = run(vals, r)
    assert out == brute(vals, r), (out, brute(vals, r))
    res[ph] = out
    print(ph, out, [s["vars"].get("array") for s in steps])
    fill(CH, NAME, block(vals, ["lo", "hi"], steps), ph)
assert res == {"@@TRACE1@@": [7, 4, 3], "@@TRACE2@@": [3, 1, 1]}
