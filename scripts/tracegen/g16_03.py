from common import *
from tr import *
CH = '16-trees-bfs-and-bsts'
F = '03-validate-search-and-insert.md'
# complete-tree positions: node i has children 2i+1 and 2i+2
heap = [8, 3, 10, 1, 6, None, 14, None, None, None, None]
def path(key):
    i = 0; st = []
    while i < len(heap) and heap[i] is not None:
        v = heap[i]
        if key == v:
            st.append((i, f"The rack {v} equals the stub {key}, so the coat is found."))
            return st, True
        side = 0 if key < v else 1
        word = "smaller" if key < v else "larger"
        drop = "right" if key < v else "left"
        st.append((i, f"The stub {key} is {word} than the rack {v}, so the {drop} side is dropped and the walk goes {'left' if key < v else 'right'}."))
        i = 2 * i + 1 + side
    st.append((i, f"The place at position {i} is empty, so the stub {key} would hang here."))
    return st, False
st, found = path(6)
assert found and [i for i, _ in st] == [0, 1, 4]
steps = [{"at": {"node": i}, "vars": {"stub": 6, "rack": heap[i]}, "note": n} for i, n in st]
fill(CH, F, block(cells(heap[:7]), ["node"], steps), "@@TRACE1@@")
st, found = path(5)
assert not found and [i for i, _ in st] == [0, 1, 4, 9]
steps = []
for i, n in st:
    if heap[i] is None:
        steps.append({"at": {"node": i}, "vars": {"stub": 5, "rack": "empty"}, "note": f"The place to the left of 6 is empty, so the new coat 5 is attached here and nothing else moves."})
    else:
        steps.append({"at": {"node": i}, "vars": {"stub": 5, "rack": heap[i]}, "note": n})
fill(CH, F, block(cells(heap), ["node"], steps), "@@TRACE2@@")
