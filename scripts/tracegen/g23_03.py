from common import *
CH = '23-directed-graphs-and-union-find'; F = '03-undirected-parent-state.md'

def run(n, edges):
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b); adj[b].append(a)
    visited = [False] * n; steps = []; found = [False]
    def dfs(v, parent):
        visited[v] = True
        for nx in adj[v]:
            ps = "none" if parent == -1 else str(parent)
            vars_ = {"neighbor": nx, "parent": parent}
            if nx == parent:
                note = f"Vertex {v} reads neighbor {nx}, which is its parent ({ps}), so the search skips it."
            elif visited[nx]:
                note = f"Vertex {v} reads neighbor {nx}. It is visited and is not the parent, so the search reports a cycle."
                steps.append({"at": {"v": v}, "vars": vars_, "note": note})
                found[0] = True
                return True
            else:
                note = f"Vertex {v} reads neighbor {nx}, which is unvisited, so the search enters it with parent {v}."
                steps.append({"at": {"v": v}, "vars": vars_, "note": note})
                if dfs(nx, v):
                    return True
                continue
            steps.append({"at": {"v": v}, "vars": vars_, "note": note})
        return False
    for s in range(n):
        if not visited[s] and dfs(s, -1):
            break
    return found[0], steps

c1, s1 = run(4, [[0,1],[0,2],[1,3]])
assert not c1
fill(CH, F, block(list(range(4)), ["v"], s1), "@@TRACE1@@")
c2, s2 = run(4, [[0,1],[1,2],[2,0],[2,3]])
assert c2
fill(CH, F, block(list(range(4)), ["v"], s2), "@@TRACE2@@")
