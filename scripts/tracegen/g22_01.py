from common import *
from collections import deque
CH='22-bfs-variations'
F='01-multi-source-bfs.md'
# trace 1: graph, stations 0 and 5
n=8
edges=[(0,1),(1,2),(2,3),(3,4),(4,5),(1,6),(6,7),(7,5)]
adj=[[] for _ in range(n)]
for a,b in edges: adj[a].append(b); adj[b].append(a)
dist=[-1]*n; q=deque(); steps=[]
for s in (0,5): dist[s]=0; q.append(s)
while q:
    v=q.popleft(); added=[]
    for w in adj[v]:
        if dist[w]==-1: dist[w]=dist[v]+1; q.append(w); added.append(w)
    steps.append({"at":{"cur":v},"vars":{"dist":dist[v],"queue":",".join(map(str,q)) or "empty"},
      "note":f"Junction {v} is removed at distance {dist[v]}, and it "+(f"adds {len(added)} junction{'s' if len(added)!=1 else ''} ({','.join(map(str,added))}) at distance {dist[v]+1}." if added else "adds nothing, because every neighbor already has a distance.")})
assert dist==[0,1,2,2,1,0,2,1] , dist
fill(CH,F,block(list(range(n)),["cur"],steps),"@@TRACE1@@")
# trace 2: walled grid 3x4
rows,cols=3,4
g=["S.#.",".#..","..S#"]
flat=[ch for r in g for ch in r]
dist=[-1]*12; q=deque(); steps=[]; mx=0
for i,ch in enumerate(flat):
    if ch=='S': dist[i]=0; q.append(i)
while q:
    code=q.popleft(); r,c=divmod(code,cols); added=[]
    mx=max(mx,dist[code])
    for dr,dc in((-1,0),(1,0),(0,-1),(0,1)):
        nr,nc=r+dr,c+dc
        if 0<=nr<rows and 0<=nc<cols and flat[nr*cols+nc]!='#' and dist[nr*cols+nc]==-1:
            dist[nr*cols+nc]=dist[code]+1; q.append(nr*cols+nc); added.append(nr*cols+nc)
    steps.append({"at":{"cur":code},"vars":{"dist":dist[code],"max_dist":mx,"queue":",".join(map(str,q)) or "empty"},
      "note":f"Square {code} at row {r}, column {c} is removed at distance {dist[code]}, and "+(f"it adds {len(added)} square{'s' if len(added)!=1 else ''} ({','.join(map(str,added))})." if added else "it adds nothing, so no later round begins from here.")})
assert mx==3 and all((dist[i]==-1)==(flat[i]=='#') for i in range(12)), dist
fill(CH,F,block(flat,["cur"],steps),"@@TRACE2@@")
