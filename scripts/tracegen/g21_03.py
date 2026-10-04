from common import *
from collections import deque
CH='21-graph-traversal-models-dfs-and-ordinary-bfs'
F='03-visited-state.md'
n=6
edges=[(0,1),(0,2),(1,3),(2,3),(3,0),(3,4),(5,0)]
adj=[[] for _ in range(n)]
for u,v in edges: adj[u].append(v)
cells=[str(i) for i in range(n)]
# trace 1: mark at enqueue
seen=[False]*n; q=deque([0]); seen[0]=True; inserted=1; steps=[]
while q:
    v=q.popleft(); new=[]
    for w in adj[v]:
        if not seen[w]:
            seen[w]=True; q.append(w); inserted+=1; new.append(w)
    steps.append({"at":{"v":v},"vars":{"inserted":inserted,"marked":sum(seen),"queue":",".join(map(str,q))},
      "note":(f"Vertex {v} comes off the queue and adds {','.join(map(str,new))} after marking it." if new else f"Vertex {v} comes off the queue and finds no unmarked neighbor, so nothing is added.")+f" Queue entries so far: {inserted}."})
assert sum(seen)==5 and inserted==5 and not seen[5]
fill(CH,F,block(cells,["v"],steps),"@@TRACE1@@")
# trace 2: mark at dequeue, skip marked on pop
seen=[False]*n; q=deque([0]); inserted=1; steps=[]
while q:
    v=q.popleft()
    if seen[v]:
        steps.append({"at":{"v":v},"vars":{"inserted":inserted,"marked":sum(seen),"queue":",".join(map(str,q))},
          "note":f"Vertex {v} comes off the queue already marked, so this entry is a duplicate and is skipped."})
        continue
    seen[v]=True
    for w in adj[v]: q.append(w); inserted+=1
    steps.append({"at":{"v":v},"vars":{"inserted":inserted,"marked":sum(seen),"queue":",".join(map(str,q))},
      "note":f"Vertex {v} is marked now and every neighbor is added, marked or not. Queue entries so far: {inserted}."})
assert sum(seen)==5 and inserted==7 and len(steps)==7
fill(CH,F,block(cells,["v"],steps),"@@TRACE2@@")
