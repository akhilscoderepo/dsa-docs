from common import *
from collections import deque
CH='21-graph-traversal-models-dfs-and-ordinary-bfs'
F='07-unweighted-shortest-paths.md'
n=7
E=[(0,1),(1,2),(2,3),(3,4),(0,5),(5,4),(5,6)]
adj=[[] for _ in range(n)]
for u,v in E: adj[u].append(v); adj[v].append(u)
for a in adj: a.sort()
dist=[-1]*n; parent=[-1]*n; dist[0]=0; q=deque([0]); steps=[]; order=[]
def tab(): return " ".join(str(x) if x>=0 else "-" for x in dist)
while q:
    cur=q.popleft(); order.append(cur); found=[]
    for nx in adj[cur]:
        if dist[nx]!=-1: continue
        dist[nx]=dist[cur]+1; parent[nx]=cur; q.append(nx); found.append(nx)
    steps.append({"at":{"cur":cur},"vars":{"dist":tab(),"queue":",".join(map(str,q)) or "empty"},
      "note":f"Station {cur} is taken from the queue at distance {dist[cur]}, and "+(f"it discovers {len(found)} new station"+("s" if len(found)!=1 else "")+f" ({','.join(map(str,found))}) at distance {dist[cur]+1}." if found else "it discovers nothing new, since every neighbour already has a distance.")})
assert order==[0,1,5,2,4,6,3] and dist==[0,1,2,3,2,1,2]
assert all(dist[order[i]]<=dist[order[i+1]] for i in range(n-1))
fill(CH,F,block(list(range(n)),["cur"],steps),"@@TRACE1@@")
# trace 2: restore to 3
steps=[]; route=[]; v=3
while v!=-1:
    route.append(v)
    steps.append({"at":{"v":v},"vars":{"route":",".join(map(str,route))},
      "note":f"Station {v} joins the route"+(f" and its predecessor is {parent[v]}, so the walk moves there." if parent[v]!=-1 else ", and it has no predecessor, so it is the depot and the walk ends.")})
    v=parent[v]
assert route==[3,2,1,0] and len(route)-1==dist[3]
fill(CH,F,block(list(range(n)),["v"],steps),"@@TRACE2@@")
