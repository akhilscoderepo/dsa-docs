from common import *
from collections import deque
CH='22-bfs-variations'
F='02-layer-meaning.md'
# trace 1: graph
n=7
edges=[(0,1),(0,2),(1,3),(2,3),(2,4),(3,5),(4,5),(5,6)]
adj=[[] for _ in range(n)]
for a,b in edges: adj[a].append(b); adj[b].append(a)
for l in adj: l.sort()
rang=[-1]*n; rang[0]=0; q=deque([0]); steps=[]; clock=0; layers=[]
while q:
    size=len(q); layer=[]
    for i in range(size):
        u=q.popleft(); layer.append(u); added=[]
        for v in adj[u]:
            if rang[v]==-1: rang[v]=clock+1; q.append(v); added.append(v)
        steps.append({"at":{"cur":u},"vars":{"layer":clock,"left":size-i-1,"queue":",".join(map(str,q)) or "empty"},
          "note":f"Room {u} is removed in pass {clock}"+(f" and rings the new room{'s' if len(added)>1 else ''} {','.join(map(str,added))}." if added else " and finds no new room.")})
    layers.append(layer); clock+=1
assert layers==[[0],[1,2],[3,4],[5],[6]] and rang==[0,1,1,2,2,3,4] and clock==5
if "@@TRACE1@@" in (ROOT/CH/F).read_text(): fill(CH,F,block(list(range(n)),["cur"],steps),"@@TRACE1@@")
# trace 2: oranges
R,C=3,4
g=[2,1,0,1, 1,1,1,2, 0,1,1,0]
cells=g[:]
state=g[:]
q=deque(i for i in range(12) if state[i]==2); steps=[]; minutes=0; per=0; lastnew=0
while q:
    size=len(q); new=0
    for i in range(size):
        u=q.popleft(); per+=1; r,c=divmod(u,C); added=[]
        for dr,dc in((1,0),(-1,0),(0,1),(0,-1)):
            a,b=r+dr,c+dc
            if 0<=a<R and 0<=b<C and state[a*C+b]==1:
                state[a*C+b]=2; q.append(a*C+b); added.append(a*C+b)
        new+=len(added)
        steps.append({"at":{"cur":u},"vars":{"minutes":minutes+(1 if new else 0),"per_orange":per,"queue":",".join(map(str,q)) or "empty"},
          "note":f"Orange {u} is removed during minute {minutes+1}"+(f" and spoils {','.join(map(str,added))}." if added else " and spoils nothing new.")})
    if new: minutes+=1; lastnew=new
assert minutes==3 and lastnew==1 and per==9 and 1 not in state
fill(CH,F,block(cells,["cur"],steps),"@@TRACE2@@")
print(len(steps))
