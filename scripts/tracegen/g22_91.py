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
st = [{"at": {"cur": -1}, "vars": {"minute": "0", "queue": str(list(q))},
       "note": f"Both rotten cells, {list(q)}, enter the queue before any removal. They form layer 0."}]
minute = 0; last = -1
while q:
    size = len(q); first_new = -1
    for _ in range(size):
        cur = q.popleft(); found = []
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = cur // C + dr, cur % C + dc
            if 0 <= nr < R and 0 <= nc < C and cells[nr * C + nc] == 1 and not visited[nr * C + nc]:
                visited[nr * C + nc] = True; fresh -= 1; q.append(nr * C + nc); found.append(nr * C + nc)
                if first_new == -1 or nr * C + nc < first_new: first_new = nr * C + nc
        shown = minute + 1 if found else minute
        msg = f"cell {cur} rots {found}." if found else f"cell {cur} finds no fresh neighbor."
        st.append({"at": {"cur": cur}, "vars": {"minute": str(shown), "queue": str(list(q))},
                   "note": f"{msg[0].upper()}{msg[1:]}"})
    if first_new != -1:
        minute += 1; last = first_new
        st.append({"at": {"cur": -1}, "vars": {"minute": str(minute), "queue": str(list(q))},
                   "note": f"The layer ends. Minute {minute} is complete, and its smallest new cell is {last}."})
st.append({"at": {"cur": -1}, "vars": {"minute": str(minute), "queue": "[]"},
           "note": f"The queue is empty and fresh = {fresh}, so the answer is {minute} minutes and the last cell is row {last // C}, column {last % C}."})
assert fresh == 0 and (minute, last // C, last % C) == (2, 0, 2)
fill(CH, F, block(cells, ["cur"], st), "@@TRACE1@@")
# Trace 2: generated word states with parents; cells are word ids and cur is the word leaving the queue.
words = ["lead", "load", "goad", "gold", "lend", "mend", "loan"]; begin, end = "lead", "gold"
idx = {w: i for i, w in enumerate(words)}
parent = {idx[begin]: idx[begin]}; q = deque([idx[begin]])
st = [{"at": {"cur": -1}, "vars": {"queue": "[lead]", "parent": "{}"},
       "note": "The begin word lead has id 0. It is marked as reached and enters the queue."}]
def show(ids): return "[" + ", ".join(words[i] for i in ids) + "]"
done = False
while q and not done:
    cur = q.popleft(); found = []
    for w in words:
        j = idx[w]
        if j in parent: continue
        if sum(a != b for a, b in zip(words[cur], w)) == 1:
            parent[j] = cur; q.append(j); found.append(j)
            if w == end: done = True
    note = (f"{words[cur]} leaves the queue and generates {show(found)}, each with parent {words[cur]}." if found
            else f"{words[cur]} leaves the queue and generates no new word.")
    if done: note += " The end word is reached, so the search stops."
    st.append({"at": {"cur": cur}, "vars": {"queue": show(q), "parent": "{" + ", ".join(f"{words[k]}:{words[v]}" for k, v in parent.items() if k != v) + "}"}, "note": note})
path = []; i = idx[end]
while True:
    path.append(words[i])
    if i == idx[begin]: break
    i = parent[i]
path.reverse()
st.append({"at": {"cur": idx[end]}, "vars": {"queue": show(q), "parent": "followed"},
           "note": "Following the parents from gold back to lead and reversing gives " + ", ".join(path) + "."})
assert path == ["lead", "load", "goad", "gold"]
fill(CH, F, block(list(range(len(words))), ["cur"], st), "@@TRACE2@@")
