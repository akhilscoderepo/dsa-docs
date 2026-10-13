import sys, pathlib, bisect
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from common import block, fill

CH = '32-selection-and-ordered-data-techniques'
FILE = '03-ordered-maps-and-sets.md'

def descend(keys, x, kind):
    """Midpoint-balanced tree over sorted keys; kind is 'floor' or 'ceiling'."""
    steps = [{"at": {"node": -1, "best": -1}, "vars": {"x": x},
              "note": f"The call {kind}({x}) starts at the root with no candidate."}]
    lo, hi, best = 0, len(keys) - 1, -1
    while lo <= hi:
        m = (lo + hi) // 2
        k = keys[m]
        ok = k <= x if kind == 'floor' else k >= x
        if ok:
            best = m
            side = "right" if kind == 'floor' else "left"
            why = f"{k} is {'at most' if kind == 'floor' else 'at least'} {x}, so it qualifies and becomes the candidate. The search goes {side} for a better key."
            if kind == 'floor': lo = m + 1
            else: hi = m - 1
        else:
            side = "left" if kind == 'floor' else "right"
            why = f"{k} is {'above' if kind == 'floor' else 'below'} {x}, so it does not qualify. The search goes {side}."
            if kind == 'floor': hi = m - 1
            else: lo = m + 1
        steps.append({"at": {"node": m, "best": best}, "vars": {"x": x, "key": k, "candidate": keys[best] if best >= 0 else None}, "note": why})
    steps.append({"at": {"node": -1, "best": best}, "vars": {"x": x, "result": keys[best] if best >= 0 else None},
                  "note": f"The search reaches a missing child, so it stops. The answer is {keys[best]}."})
    # oracle
    if kind == 'floor':
        i = bisect.bisect_right(keys, x) - 1
    else:
        i = bisect.bisect_left(keys, x)
        i = i if i < len(keys) else -1
    assert i == best, (i, best)
    return steps, keys[best]

k1 = [3, 8, 12, 17, 21, 25, 30]
k2 = [2, 7, 11, 16, 22, 27, 31, 40, 44]
s1, a1 = descend(k1, 14, 'ceiling')
s2, a2 = descend(k2, 25, 'floor')
assert a1 == 17 and a2 == 22
fill(CH, FILE, block(k1, ["node", "best"], s1), "@@TRACE1@@")
fill(CH, FILE, block(k2, ["node", "best"], s2), "@@TRACE2@@")
print(a1, a2)
