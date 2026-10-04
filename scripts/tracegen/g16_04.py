from common import *
from tr import *
CH = '16-trees-bfs-and-bsts'
F = '04-successor-and-predecessor.md'
arr = [8, 3, 10, 1, 6, None, 14, None, None, 4, 7, 13]
L, R = parse(arr)
def run(target):
    i = 0; best = None; st = []
    while i is not None:
        v = arr[i]
        if v > target:
            best = v
            nxt = L[i]
            note = f"The bell {v} is higher than {target}, so it is saved as the candidate and the walk goes left."
        else:
            nxt = R[i]
            note = f"The bell {v} is not higher than {target}, so the candidate stays and the walk goes right."
        if nxt is None:
            note += f" There is nothing on that side, so the walk ends with {best if best is not None else 'no candidate'} as the answer."
        st.append({"at": {"node": i}, "vars": {"target": target, "best": "none" if best is None else best}, "note": note})
        i = nxt
    return st, best
st, best = run(7); assert best == 8 and [s["at"]["node"] for s in st] == [0, 1, 4, 10]
fill(CH, F, block(cells(arr), ["node"], st), "@@TRACE1@@")
st, best = run(3); assert best == 4 and [s["at"]["node"] for s in st] == [0, 1, 4, 9]
fill(CH, F, block(cells(arr), ["node"], st), "@@TRACE2@@")
