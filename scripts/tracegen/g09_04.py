from common import *
CH = '09-sliding-window'
F = '04-minimum-cover-and-deficit-windows.md'


def run(s, need):
    ledger = dict(need)
    missing = sum(need.values())
    left = 0
    best = None
    steps = []
    for right, c in enumerate(s):
        if ledger.get(c, 0) > 0:
            missing -= 1
        ledger[c] = ledger.get(c, 0) - 1
        removed = 0
        recorded = None
        while missing == 0:
            ln = right - left + 1
            if best is None or ln < best[1]:
                best = (left, ln)
                recorded = ln
            out = s[left]
            left += 1
            removed += 1
            ledger[out] += 1
            if ledger[out] > 0:
                missing += 1
        if recorded is not None:
            note = f"Position {right} ({c}) completes a cover. The shrink loop records length {recorded}, removes {removed} floats, and left becomes {left}. Missing is back to {missing}."
        elif removed:
            note = f"Position {right} ({c}) completes a cover, but length is no better than the best. {removed} floats leave and left becomes {left}."
        else:
            note = f"Position {right} ({c}) is added. Missing is {missing}, so the window is not a cover yet." if missing else f"Position {right} ({c}) is added."
        steps.append({"at": {"left": left, "right": right}, "vars": {"missing": missing, "best": best[1] if best else 0}, "note": note})
    return steps, best


s1 = "qabxxcbaqz"
st, best = run(s1, {"a": 1, "b": 1, "c": 1})
assert best == (1, 3) or best[1] == 3, best
assert st[5]["at"]["left"] == 2 and "records length 5" in st[5]["note"], st[5]
fill(CH, F, block(list(s1), ["left", "right"], st), "@@TRACE1@@")

s2 = "abaxbbaxa"
st, best = run(s2, {"a": 2, "b": 1})
assert best == (0, 3), best
assert "records length 3" in st[2]["note"] and st[2]["at"]["left"] == 1, st[2]
fill(CH, F, block(list(s2), ["left", "right"], st), "@@TRACE2@@")
