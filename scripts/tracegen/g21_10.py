from common import *
CH = '21-graph-traversal-models-dfs-and-ordinary-bfs'
F = '10-grid-and-graph-traversal.md'

DR = [0, 1, 0, -1, 1, 1, -1, -1]
DC = [1, 0, -1, 0, 1, -1, -1, 1]

# trace 1: ring flood fill (columns wrap), DFS with a stack of ids
img = [[1, 0, 0, 1], [0, 0, 0, 1], [1, 1, 0, 1]]
rows, cols = 3, 4
cells = [v for row in img for v in row]
tone = 1
owned = [False] * (rows * cols)
stack = [0]; owned[0] = True
claimed = 0; steps = []; order = []
while stack:
    cid = stack.pop(); claimed += 1; order.append(cid)
    r, c = divmod(cid, cols); pushed = []
    for d in range(4):
        nr, nc = r + DR[d], (c + DC[d]) % cols
        if nr < 0 or nr >= rows: continue
        nxt = nr * cols + nc
        if owned[nxt] or cells[nxt] != tone: continue
        owned[nxt] = True; stack.append(nxt); pushed.append(nxt)
    wrapped = any(abs((p % cols) - c) > 1 for p in pushed)
    note = f"Cell {cid} at row {r}, column {c} is claimed and it pushes " + (f"{len(pushed)} new cells ({', '.join(map(str, pushed))})" if pushed else "nothing new")
    note += ", one of them through the wrap of the ring." if wrapped else "."
    steps.append({"at": {"cur": cid}, "vars": {"claimed": claimed, "waiting": len(stack)}, "note": note})
assert sorted(order) == [0, 3, 7, 8, 9, 11] and claimed == 6 and not owned[6]
assert any("wrap" in s["note"] for s in steps)
# independent oracle: label propagation on the ring
lab = {i: i for i in range(12) if cells[i] == tone}
ch = True
while ch:
    ch = False
    for i in list(lab):
        r, c = divmod(i, cols)
        for dr, dc in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            nr, nc = r + dr, (c + dc) % cols
            j = nr * cols + nc
            if 0 <= nr < rows and j in lab and lab[j] < lab[i]: lab[i] = lab[j]; ch = True
assert sorted(i for i in lab if lab[i] == lab[0]) == sorted(order)
fill(CH, F, block(cells, ["cur"], steps), "@@TRACE1@@")

# trace 2: outer scan with the diagonal flag
grid = ["1001", "0100", "0010"]
rows, cols = 3, 4
cells = [ch for row in grid for ch in row]

def scan(diag, record):
    owned = [False] * 12; count = 0; last = 0; steps = []
    moves = 8 if diag else 4
    for sid in range(12):
        if cells[sid] == '1' and not owned[sid]:
            count += 1
            st = [sid]; owned[sid] = True; last = 0
            while st:
                cid = st.pop(); last += 1
                r, c = divmod(cid, cols)
                for d in range(moves):
                    nr, nc = r + DR[d], c + DC[d]
                    if not (0 <= nr < rows and 0 <= nc < cols): continue
                    nx = nr * cols + nc
                    if owned[nx] or cells[nx] != '1': continue
                    owned[nx] = True; st.append(nx)
            if record: steps.append({"at": {"scan": sid}, "vars": {"islands": count, "last_size": last},
                "note": f"Id {sid} is unowned land, so search {count} starts and claims {last} cell" + ("s." if last != 1 else ".")})
        elif cells[sid] == '1' and record:
            steps.append({"at": {"scan": sid}, "vars": {"islands": count, "last_size": last},
                "note": f"Id {sid} is land that is already owned, so no new search starts."})
    return count, steps
n8, steps = scan(True, True)
n4, _ = scan(False, False)
assert (n8, n4) == (2, 4)
steps.append({"at": {"scan": 12}, "vars": {"islands": n8, "last_size": steps[-1]["vars"]["last_size"]},
    "note": f"The scan has passed all twelve ids and the diagonal contract gives {n8} islands, where the four-way contract would give {n4}."})
# oracle: union-find over land cells
par = list(range(12))
def f(x):
    while par[x] != x: par[x] = par[par[x]]; x = par[x]
    return x
for i in range(12):
    for j in range(12):
        if cells[i] == '1' == cells[j]:
            (r1, c1), (r2, c2) = divmod(i, cols), divmod(j, cols)
            if max(abs(r1 - r2), abs(c1 - c2)) == 1: par[f(i)] = f(j)
assert len({f(i) for i in range(12) if cells[i] == '1'}) == n8
fill(CH, F, block(cells, ["scan"], steps), "@@TRACE2@@")
