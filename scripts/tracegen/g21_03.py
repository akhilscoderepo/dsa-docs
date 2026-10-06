from common import *
from collections import deque
CH='21-graph-traversal-models-dfs-and-ordinary-bfs'; F='03-visited-state.md'
def fmt(xs): return "["+",".join(map(str,xs))+"]" if xs else "[]"
def run(n,edges,source,directed,ph,notes):
    adj=[[] for _ in range(n)]
    for a,b in edges:
        adj[a].append(b)
        if not directed: adj[b].append(a)
    visited=[False]*n; visited[source]=True; q=deque([source]); st=[]; k=0; pushes=1
    while q:
        v=q.popleft(); added=[]; skipped=[]
        for w in adj[v]:
            if visited[w]: skipped.append(w)
            else: visited[w]=True; q.append(w); added.append(w); pushes+=1
        st.append({"at":{"cur":v},"vars":{"frontier":fmt(list(q)),"marked":fmt([i for i in range(n) if visited[i]])},"note":notes[k](v,added,skipped)}); k+=1
    assert pushes==sum(visited)
    st.append({"at":{"cur":-1},"vars":{"frontier":"[]","marked":fmt([i for i in range(n) if visited[i]])},"note":notes[k]([i for i in range(n) if not visited[i]])})
    fill(CH,F,block(list(range(n)),["cur"],st),ph); return visited
n1=[
 lambda v,a,s:f"Vertex {v} leaves the frontier and marks its neighbors {a[0]} and {a[1]} as it adds them.",
 lambda v,a,s:f"Vertex {v} finds vertex {s[0]} already marked and adds only vertex {a[0]}.",
 lambda v,a,s:f"Vertex {v} sees that vertex {s[1]} is already marked, so it adds nothing and the repeated entry never forms." if False else f"Vertex {v} sees vertex {s[1]} already marked, so it adds nothing and no repeated entry forms.",
 lambda v,a,s:f"Vertex {v} skips the marked vertices {s[0]} and {s[1]} and adds vertex {a[0]}.",
 lambda v,a,s:f"Vertex {v} has no unmarked neighbor, so the frontier becomes empty.",
 lambda u:"The frontier is empty and every vertex is marked, so each vertex was scheduled once."]
r=run(5,[[0,1],[0,2],[1,3],[2,3],[3,4]],0,False,"@@TRACE1@@",n1); assert all(r)
# note step 2 (vertex 1): neighbors 0 (marked), 3 (added)
n2=[
 lambda v,a,s:f"Vertex {v} marks vertex {a[0]} and adds it to the frontier.",
 lambda v,a,s:f"Vertex {v} marks vertex {a[0]} and adds it to the frontier.".replace("marks","reaches and marks"),
 lambda v,a,s:f"Vertex {v} has an edge back to marked vertex {s[0]}, so the cycle stops there, and it adds vertex {a[0]}.",
 lambda v,a,s:f"Vertex {v} has no outgoing edge, so nothing joins the frontier.",
 lambda u:f"The frontier is empty. Vertex {u[0]} was never marked, because no edge leads to it from a marked vertex."]
r=run(5,[[0,1],[1,2],[2,0],[2,3]],0,True,"@@TRACE2@@",n2); assert r==[True,True,True,True,False]
