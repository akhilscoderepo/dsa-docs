import sys
from collections import deque
from common import *
CH='24-shortest-paths-and-graph-state-modeling'
INF=10**9
def run(cells, nbrs, ptr, ph, n):
    """nbrs(u) yields (v,w). Simulates the deque search and records steps."""
    dist=[INF]*n; dist[0]=0; dq=deque([(0,0)]); st=[]
    D=lambda: "-".join("x" if d==INF else str(d) for d in dist)
    Q=lambda: "-".join(f"{u}@{d}" for u,d in dq) if dq else "empty"
    def snap(cur,note): st.append({"at":{ptr:cur},"vars":{"dist":D(),"deque":Q()},"note":note})
    snap(0,"The search stores distance 0 for the source and puts the entry for vertex 0 in the deque.")
    pushes=1
    while dq:
        u,d=dq.popleft()
        if d>dist[u]:
            snap(u,f"The front entry for vertex {u} carries distance {d}, but the stored distance is {dist[u]}, so the search discards it.")
            continue
        snap(u,f"The search takes vertex {u} from the front with distance {d}.")
        for v,w in nbrs(u):
            if d+w<dist[v]:
                dist[v]=d+w; pushes+=1
                if w==0:
                    dq.appendleft((v,d+w)); snap(u,f"The edge from {u} to {v} costs 0 and improves vertex {v} to {d+w}, so its entry goes to the front.")
                else:
                    dq.append((v,d+w)); snap(u,f"The edge from {u} to {v} costs 1 and improves vertex {v} to {d+w}, so its entry goes to the back.")
    fill(CH,'92-shortest-paths-with-a-deque.md',block(cells,[ptr],st),ph)
    return dist,pushes
edges=[(0,3,1),(0,1,0),(1,3,0),(3,4,1),(1,2,1)]
adj=[[] for _ in range(5)]
for a,b,w in edges: adj[a].append((b,w))
dist,p=run(list(range(5)),lambda u:adj[u],"cur","@@TRACE1@@",5)
assert dist==[0,0,1,0,1] and p==6
g=[[2,1,1],[1,1,3]]
m,n=2,3
A={1:(0,1),2:(0,-1),3:(1,0),4:(-1,0)}
def nb(u):
    r,c=divmod(u,n)
    for k,(dr,dc) in A.items():
        R,C=r+dr,c+dc
        if 0<=R<m and 0<=C<n: yield R*n+C,(0 if g[r][c]==k else 1)
dist,p=run([x for row in g for x in row],nb,"cell","@@TRACE2@@",6)
print(dist)
assert dist[5]==1
