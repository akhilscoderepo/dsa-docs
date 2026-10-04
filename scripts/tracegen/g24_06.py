from common import *
from collections import deque
CH='24-shortest-paths-and-graph-state-modeling'
F='06-zero-one-bfs.md'
# trace 1: 3x3 wind grid, steps in pop order (stale pops included)
g=[[3,1,3],[3,1,3],[1,3,3]]
R=C=3; HEAD={1:(0,1),2:(0,-1),3:(1,0),4:(-1,0)}
letter={1:'R',2:'L',3:'D',4:'U'}
INF=10**9
dist=[INF]*9; dist[0]=0; dq=deque([(0,0)]); steps=[]; stale_seen=0
while dq:
    pad,d=dq.popleft(); r,c=divmod(pad,C)
    if d>dist[pad]:
        stale_seen+=1
        steps.append({"at":{"cur":pad},"vars":{"cost":d,"stale":1,"front":0,"back":0,"waiting":len(dq)},
          "note":f"The entry for pad {pad} carries cost {d}, but the table already holds {dist[pad]}, so it is skipped."})
        continue
    fr=bk=0
    for k,(dr,dc) in HEAD.items():
        nr,nc=r+dr,c+dc
        if not(0<=nr<R and 0<=nc<C): continue
        t=0 if g[r][c]==k else 1; nx=nr*C+nc
        if d+t<dist[nx]:
            dist[nx]=d+t
            if t==0: dq.appendleft((nx,d+t)); fr+=1
            else: dq.append((nx,d+t)); bk+=1
    steps.append({"at":{"cur":pad},"vars":{"cost":d,"stale":0,"front":fr,"back":bk,"waiting":len(dq)},
      "note":f"Pad {pad} is expanded at cost {d}; {fr} entr{'y' if fr==1 else 'ies'} went to the front and {bk} to the back."})
assert dist[8]==1, dist
# independent check by Bellman-Ford fixpoint
bf=[INF]*9; bf[0]=0; ch=True
while ch:
    ch=False
    for p in range(9):
        r,c=divmod(p,C)
        for k,(dr,dc) in HEAD.items():
            nr,nc=r+dr,c+dc
            if 0<=nr<R and 0<=nc<C and bf[p]+(g[r][c]!=k)<bf[nr*C+nc]: bf[nr*C+nc]=bf[p]+(g[r][c]!=k); ch=True
assert bf==dist
cells=[letter[x] for row in g for x in row]
fill(CH,F,block(cells,["cur"],steps),"@@TRACE1@@")
# trace 2: explicit graph with zero cycles and a stale duplicate
edges=[(0,3,1),(0,1,0),(1,3,0),(3,1,0),(1,2,1),(2,4,0),(4,2,0)]
n=5; adj=[[] for _ in range(n)]
for a,b,w in edges: adj[a].append((b,w))
dist=[INF]*n; dist[0]=0; dq=deque([(0,0)]); steps=[]; stale_hit=0
def span(): return (dq[-1][1]-dq[0][1]) if dq else 0
while dq:
    v,d=dq.popleft()
    if d>dist[v]:
        stale_hit+=1
        steps.append({"at":{"cur":v},"vars":{"cost":d,"stale":1,"span":span(),"waiting":len(dq)},
          "note":f"The entry for junction {v} carries cost {d} but the table holds {dist[v]}, so it is skipped."})
        continue
    msgs=[]
    for b,w in adj[v]:
        if d+w<dist[b]:
            dist[b]=d+w
            (dq.appendleft if w==0 else dq.append)((b,d+w))
            msgs.append(f"{b} at {d+w} to the {'front' if w==0 else 'back'}")
        assert not dq or dq[-1][1]-dq[0][1]<=1
        assert all(dq[i][1]<=dq[i+1][1] for i in range(len(dq)-1))
    note=f"Junction {v} is expanded at cost {d}; "+("it queues "+", ".join(msgs)+"." if msgs else "no edge lowers a stored cost.")
    steps.append({"at":{"cur":v},"vars":{"cost":d,"stale":0,"span":span(),"waiting":len(dq)},"note":note})
assert stale_hit==1 and dist==[0,0,1,0,1], dist
fill(CH,F,block([0,1,2,3,4],["cur"],steps),"@@TRACE2@@")
print(dist)
