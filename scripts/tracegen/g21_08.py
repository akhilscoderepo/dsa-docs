from common import *
from collections import deque
CH='21-graph-traversal-models-dfs-and-ordinary-bfs'; F='08-bipartite-coloring.md'
def run(n,edges,ph):
    adj=[[] for _ in range(n)]
    for a,b in edges: adj[a].append(b); adj[b].append(a)
    color=[-1]*n; st=[]; ok=True
    def cs(): return "".join('.' if c<0 else str(c) for c in color)
    for s in range(n):
        if color[s]!=-1: continue
        color[s]=0; q=deque([s])
        st.append({"at":{"cur":s},"vars":{"colors":cs(),"queue":str(list(q))},"note":f"Vertex {s} is uncolored, so it becomes a new source and receives color 0."})
        while q and ok:
            u=q.popleft(); new=[]; bad=None
            for v in adj[u]:
                if color[v]==color[u]: bad=v; break
                if color[v]==-1: color[v]=1-color[u]; q.append(v); new.append(v)
            if bad is not None:
                ok=False
                note=f"Vertex {u} meets neighbor {bad}, and both hold color {color[u]}. The edge is a conflict, so the answer is false."
            elif new:
                note=f"Vertex {u} leaves the queue and gives color {1-color[u]} to neighbors {new}."
            else:
                note=f"Vertex {u} leaves the queue, and every neighbor already holds the opposite color."
            st.append({"at":{"cur":u},"vars":{"colors":cs(),"queue":str(list(q))},"note":note})
        if not ok: break
    if ok: st.append({"at":{"cur":-1},"vars":{"colors":cs(),"queue":"[]"},"note":"The loop passes vertex 5 and finds every vertex colored, so the graph passes." if n==6 else "Every vertex is colored."})
    fill(CH,F,block(list(range(n)),["cur"],st),ph); return ok
assert run(6,[(0,1),(0,2),(1,3),(2,3),(3,4)],"@@TRACE1@@")==True
assert run(6,[(0,1),(2,3),(3,4),(4,2),(4,5)],"@@TRACE2@@")==False
