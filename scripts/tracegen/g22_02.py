from common import *
from collections import deque
CH = '22-bfs-variations'; F = '02-layer-meaning.md'

def run(n, edges, source):
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b); adj[b].append(a)
    visited = [False] * n; visited[source] = True
    q = deque([source]); layers = 0; steps = []
    while q:
        size = len(q); found = False
        for i in range(size):
            cur = q.popleft(); new = []
            for nx in adj[cur]:
                if not visited[nx]:
                    visited[nx] = True; q.append(nx); found = True; new.append(nx)
            if i == size - 1 and found:
                layers += 1
            qs = "-".join(map(str, q)) if q else "empty"
            if new:
                note = f"The search takes vertex {cur} from a pass of size {size} and appends {' and '.join(map(str, new))}."
            else:
                note = f"The search takes vertex {cur} from a pass of size {size} and finds no unvisited neighbor."
            if i == size - 1 and found:
                note += f" The pass appended vertices, so layers becomes {layers}."
            elif i == size - 1:
                note += " The pass appended nothing, so layers keeps its value."
            steps.append({"at": {"cur": cur}, "vars": {"size": size, "layers": layers, "queue": qs}, "note": note})
    return layers, steps

l1, s1 = run(7, [[0,1],[0,2],[1,3],[2,3],[3,4],[5,6]], 0)
assert l1 == 3
fill(CH, F, block(list(range(7)), ["cur"], s1), "@@TRACE1@@")
l2, s2 = run(4, [[0,1],[0,2],[1,2],[2,3]], 0)
assert l2 == 2
fill(CH, F, block(list(range(4)), ["cur"], s2), "@@TRACE2@@")
