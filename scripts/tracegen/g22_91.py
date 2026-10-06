from common import *
from collections import deque
CH = '22-bfs-variations'; F = '91-model-the-state.md'
# Trace 1: layered multi-source rotting on a 3 x 4 table; the pointer cur is the cell leaving the queue.
grid = [[2, 1, 1, 0], [1, 0, 1, 1], [0, 1, 1, 2]]
R, C = 3, 4
cells = [grid[i // C][i % C] for i in range(R * C)]
visited = [False] * (R * C); q = deque(); fresh = 0
for i, v in enumerate(cells):
    if v == 2: visited[i] = True; q.append(i)
    elif v == 1: fresh += 1
dist = [-1] * (R * C); q = deque()
for i, v in enumerate(cells):
    if v == 2: dist[i] = 0; q.append(i)
st = [{"at": {"key": -1}, "vars": {"layer": "0", "queue": str(list(q))},
       "note": f"Both rotten cells, {list(q)}, enter the queue before any removal. They form layer 0."}]
layer = 0; last = -1
while q:
    size = len(q); first_new = -1
    for _ in range(size):
        key = q.popleft(); found = []
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = key // C + dr, key % C + dc
            nid = nr * C + nc
            if 0 <= nr < R and 0 <= nc < C and cells[nid] == 1 and dist[nid] == -1:
                dist[nid] = layer + 1; q.append(nid); found.append(nid)
                if first_new == -1 or nid < first_new: first_new = nid
        msg = f"Cell {key} rots {found}." if found else f"Cell {key} finds no fresh neighbor."
        st.append({"at": {"key": key}, "vars": {"layer": str(layer), "queue": str(list(q))}, "note": msg})
    if first_new != -1:
        last = first_new
        st.append({"at": {"key": -1}, "vars": {"layer": str(layer), "queue": str(list(q))},
                   "note": f"Layer {layer} is fully expanded. The cells it rotted form layer {layer + 1} in minute {layer + 1}, and the smallest is {first_new}."})
        layer += 1
fresh = sum(1 for i, v in enumerate(cells) if v == 1 and dist[i] == -1)
top = max(dist)
st.append({"at": {"key": -1}, "vars": {"layer": str(top), "queue": "[]"},
           "note": f"The queue is empty. The largest layer number is {top}, so the answer is {top} minutes, and the last cell is row {last // C}, column {last % C}."})
assert fresh == 0 and (top, last // C, last % C) == (2, 0, 2)
fill(CH, F, block(cells, ["key"], st), "@@TRACE1@@")
# Trace 2: generated word states with parents; cells are word ids and cur is the word leaving the queue.
words = ["lead", "load", "goad", "gold", "lend", "mend", "loan"]; begin, end = "lead", "gold"
idx = {w: i for i, w in enumerate(words)}
parent = {idx[begin]: idx[begin]}; q = deque([idx[begin]])
st = [{"at": {"key": -1}, "vars": {"queue": "[lead]", "parent": "{}"},
       "note": "The begin word lead has id 0. It is marked as reached and enters the queue."}]
def show(ids): return "[" + ", ".join(words[i] for i in ids) + "]"
done = False
while q:
    cur = q.popleft(); found = []
    for p in range(len(words[cur])):
        for ch in "abcdefghijklmnopqrstuvwxyz":
            if ch == words[cur][p]: continue
            w = words[cur][:p] + ch + words[cur][p + 1:]
            if w not in idx or idx[w] in parent: continue
            j = idx[w]; parent[j] = cur; q.append(j); found.append(j)
    note = (f"{words[cur]} leaves the queue and generates {show(found)}, each with parent {words[cur]}." if found
            else f"{words[cur]} leaves the queue and generates no new word.")
    st.append({"at": {"key": cur}, "vars": {"queue": show(q), "parent": "{" + ", ".join(f"{words[k]}:{words[v]}" for k, v in parent.items() if k != v) + "}"}, "note": note})
path = []; i = idx[end]
while True:
    path.append(words[i])
    if i == idx[begin]: break
    i = parent[i]
path.reverse()
st.append({"at": {"key": idx[end]}, "vars": {"queue": show(q), "parent": "followed"},
           "note": "The search ran until the queue emptied. The caller then follows the parents from gold back to lead, and the reversed list is " + ", ".join(path) + "."})
assert path == ["lead", "load", "goad", "gold"]
fill(CH, F, block(list(range(len(words))), ["key"], st), "@@TRACE2@@")
