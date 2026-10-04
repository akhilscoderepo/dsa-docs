from common import *
from collections import deque
CH='21-graph-traversal-models-dfs-and-ordinary-bfs'
F='08-bipartite-coloring.md'
def adjof(n,edges):
    a=[[] for _ in range(n)]
    for u,v in edges: a[u].append(v); a[v].append(u)
    return a
# trace 1: connected, six guests
n=6; edges=[(0,1),(0,2),(1,3),(2,3),(2,5),(3,4)]
adj=adjof(n,edges)
color=[-1]*n; color[0]=0; q=deque([0]); steps=[]
while q:
    u=q.popleft(); new=[]; cmp=[]
    for v in adj[u]:
        if color[v]==-1: color[v]=1-color[u]; q.append(v); new.append(v)
        else:
            assert color[v]!=color[u]; cmp.append(v)
    parts=[]
    if new: parts.append("colors "+", ".join(f"guest {v} with {color[v]}" for v in new))
    if cmp: parts.append("compares "+", ".join(f"guest {v} (colors differ)" for v in cmp))
    steps.append({"at":{"cur":u},"vars":{"queue":",".join(map(str,q)) or "empty","seated":sum(c!=-1 for c in color)},
      "note":f"Guest {u} with color {color[u]} is taken from the queue and "+(" and ".join(parts) if parts else "finds nothing to do")+"."})
assert color==[0,1,1,0,1,0]
fill(CH,F,block(color,["cur"],steps),"@@TRACE1@@")
# trace 2: disconnected with odd ring
n=7; edges=[(0,1),(1,2),(3,4),(4,5),(5,3)]
adj=adjof(n,edges)
color=[-1]*n; steps=[]; starts=0; q=deque(); bad=False
for s in range(n):
    if color[s]!=-1: continue
    starts+=1; color[s]=0; q.append(s)
    steps.append({"at":{"cur":s},"vars":{"searches":starts,"queue":",".join(map(str,q))},"note":f"Guest {s} is uncolored, so search {starts} begins and gives it color 0."}) if False else None
    while q:
        u=q.popleft(); new=[]; clash=None
        for v in adj[u]:
            if color[v]==-1: color[v]=1-color[u]; q.append(v); new.append(v)
            elif color[v]==color[u]: clash=v; break
        if clash is not None:
            steps.append({"at":{"cur":u},"vars":{"searches":starts,"queue":",".join(map(str,q)) or "empty"},
              "note":f"Guest {u} with color {color[u]} meets guest {clash}, which also has color {color[clash]}, so the answer is false."})
            bad=True; break
        steps.append({"at":{"cur":u},"vars":{"searches":starts,"queue":",".join(map(str,q)) or "empty"},
          "note":f"Search {starts}: guest {u} with color {color[u]} is expanded"+(" and colors "+", ".join(f"guest {v} with {color[v]}" for v in new) if new else " with nothing new to color")+"."})
    if bad: break
    if s==2 or s==6: pass
assert bad and starts==2 and color[:3]==[0,1,0] and color[3:6]==[0,1,1]
# add the isolated-guest note honestly: guest 6 is never reached because the run stops; reword accordingly
fill(CH,F,block(color,["cur"],steps),"@@TRACE2@@")
