from common import *
from collections import deque
CH='24-shortest-paths-and-graph-state-modeling'
F='08-graph-and-deque.md'
# trace 1: five hamlets
n=5; lanes=[[0,1,1],[0,2,0],[2,1,0],[2,3,1],[3,2,0]]
adj=[[] for _ in range(n)]
for a,b,w in lanes: adj[a].append((b,w))
INF=10**9
dist=[INF]*n; dist[0]=0; dq=deque([0]); steps=[]
def fmt(q): return "["+",".join(map(str,q))+"]"
while dq:
    u=dq.popleft(); notes=[]
    for v,w in adj[u]:
        if dist[u]+w<dist[v]:
            old=dist[v]; dist[v]=dist[u]+w
            if w==0: dq.appendleft(v)
            else: dq.append(v)
            notes.append(f"lane to {v} gives {dist[v]}"+(f" (was {old})" if old<INF else "")+(", queued at the front" if w==0 else ", queued at the back"))
    d=dist[u]
    note=f"Hamlet {u} is taken from the front with count {d}; "+("; ".join(notes)+"." if notes else "no lane improves anything, so nothing is queued.")
    steps.append({"at":{"v":u},"vars":{"count":d,"deque":fmt(dq)},"note":note})
assert dist==[0,0,0,1,INF] and len(steps)==5, (dist,len(steps))
assert [s["at"]["v"] for s in steps]==[0,2,1,1,3]
fill(CH,F,block(["h0","h1","h2","h3","h4"],["v"],steps),"@@TRACE1@@")
# trace 2: arrows
g=[[1,1,3],[4,2,2],[3,3,1]]; rows=cols=3
D=[(0,1),(0,-1),(1,0),(-1,0)]; name={1:"R",2:"L",3:"D",4:"U"}
d=[INF]*9; d[0]=0; dq=deque([(0,0)]); steps=[]; zeros=0
while dq:
    cost,cell=dq.popleft()
    if cost>d[cell]: continue
    r,c=divmod(cell,cols); notes=[]
    for k,(dr,dc) in enumerate(D):
        nr,nc=r+dr,c+dc
        if not(0<=nr<rows and 0<=nc<cols): continue
        w=0 if g[r][c]==k+1 else 1; to=nr*cols+nc
        if cost+w<d[to]:
            d[to]=cost+w
            if w==0: dq.appendleft((d[to],to))
            else: dq.append((d[to],to))
            notes.append(f"cell {to} gets {d[to]}")
    if cost==0: zeros+=1
    steps.append({"at":{"cell":cell},"vars":{"count":cost,"zeros":zeros,"waiting":len(dq)},
      "note":f"Cell {cell} is taken with count {cost}; "+(", ".join(notes)+"." if notes else "it improves no neighbour.")})
assert d[8]==1 and sum(1 for x in d if x==0)==6 and zeros==6
fill(CH,F,block([name[x] for row in g for x in row],["cell"],steps),"@@TRACE2@@")
print([s["at"] for s in steps])
