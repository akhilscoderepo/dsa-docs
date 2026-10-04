from common import *
from tr import *
CH = '16-trees-bfs-and-bsts'
F = '06-general-and-bst-lca.md'
arr = [1, 2, 3, 4, 5, 6, 7, None, None, 8, 9]
L, R = parse(arr)
def run(p, q):
    steps = []
    def go(i):
        if i is None: return None
        v = arr[i]
        if v in (p, q):
            steps.append({"at": {"node": i}, "vars": {"report": v}, "note": f"The junction {v} is a camper, so it reports itself at once without looking further."})
            return v
        l = go(L[i]); r = go(R[i])
        if l is not None and r is not None:
            rep = v; note = f"The branches of the junction {v} reported {l} and {r}, one camper on each side, so {v} is the meeting junction and reports itself."
        elif l is not None or r is not None:
            rep = l if l is not None else r
            note = f"Only one branch of the junction {v} reported, so it passes the report {rep} upward unchanged."
        else:
            rep = None; note = f"Neither branch of the junction {v} holds a camper, so it reports nothing."
        steps.append({"at": {"node": i}, "vars": {"report": "none" if rep is None else rep}, "note": note})
        return rep
    return go(0), steps
ans, st = run(8, 7); assert ans == 1 and len(st) == 9
fill(CH, F, block(cells(arr), ["node"], st), "@@TRACE1@@")
ans, st = run(2, 9); assert ans == 2 and [s["at"]["node"] for s in st] == [1, 5, 6, 2, 0]
fill(CH, F, block(cells(arr), ["node"], st), "@@TRACE2@@")
arr = [20, 10, 30, 5, 15, 25, 35, None, None, 12, 18]
L, R = parse(arr)
p, q = 12, 18
i = 0; st = []
while True:
    v = arr[i]
    if p < v and q < v:
        st.append({"at": {"node": i}, "vars": {"p": p, "q": q}, "note": f"Both {p} and {q} are smaller than the junction {v}, so the walk goes left."}); i = L[i]
    elif p > v and q > v:
        st.append({"at": {"node": i}, "vars": {"p": p, "q": q}, "note": f"Both {p} and {q} are larger than the junction {v}, so the walk goes right."}); i = R[i]
    else:
        st.append({"at": {"node": i}, "vars": {"p": p, "q": q}, "note": f"The junction {v} is not above both numbers nor below both, so the routes separate here and {v} is the answer."}); break
assert arr[i] == 15 and len(st) == 3
fill(CH, F, block(cells(arr), ["node"], st), "@@TRACE3@@")
