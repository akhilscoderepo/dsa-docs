from common import *
import heapq
CH='24-shortest-paths-and-graph-state-modeling'
F='01-dijkstra.md'
INF=float('inf')
def adj(n,edges):
    g=[[] for _ in range(n)]
    for u,v,w in edges: g[u].append((v,w))
    return g
def bellman(n,edges,s):
    d=[INF]*n; d[s]=0
    for _ in range(n):
        for u,v,w in edges:
            if d[u]+w<d[v]: d[v]=d[u]+w
    return d
# trace 1: heap with a stale entry
n1=6; e1=[(0,1,7),(0,2,2),(2,1,3),(2,3,8),(1,4,1),(3,4,2),(4,5,4),(3,5,1)]
g=adj(n1,e1); dist=[INF]*n1; dist[0]=0; h=[(0,0)]; cells=[]; steps=[]
while h:
    d,u=heapq.heappop(h)
    cells.append(f"{u}@{d}")
    if d>dist[u]:
        steps.append({"at":{"pop":len(cells)-1},"vars":{"cost":d,"heap":len(h),"improved":0},"note":f"Entry {u}@{d} is stale, because town {u} is already known to cost {dist[u]}; it is dropped with no work."}); continue
    imp=[]
    for v,w in g[u]:
        if d+w<dist[v]:
            dist[v]=d+w; heapq.heappush(h,(dist[v],v)); imp.append(f"{v} to {dist[v]}")
    steps.append({"at":{"pop":len(cells)-1},"vars":{"cost":d,"heap":len(h),"improved":len(imp)},
      "note":f"Town {u} is taken at cost {d}; "+(("its tolls lower or set "+", ".join(imp)+".") if imp else "none of its tolls beat a known price.")})
assert dist==[0,5,2,10,6,10], dist
assert dist==bellman(n1,e1,0)
assert any('stale' in s['note'] for s in steps)
fill(CH,F,block(cells,["pop"],steps),"@@TRACE1@@")
print(cells,dist)
# trace 2: negative edge, settle-at-pop version
n2=5; e2=[(0,1,4),(0,2,5),(2,1,-5),(1,3,2),(3,4,1)]
g=adj(n2,e2); truth=bellman(n2,e2,0)
dist=[INF]*n2; dist[0]=0; done=[False]*n2; h=[(0,0)]; cells=[]; steps=[]
while h:
    d,u=heapq.heappop(h)
    if done[u]: continue
    done[u]=True; cells.append(f"{u}@{d}")
    skipped=[]
    for v,w in g[u]:
        if done[v]:
            skipped.append(v); continue
        if d+w<dist[v]: dist[v]=d+w; heapq.heappush(h,(dist[v],v))
    bad=d!=truth[u]
    note=f"Town {u} is taken at cost {d}"+(f", but the cheapest real cost is {truth[u]}, so this claim is wrong." if bad else ", which is correct.")
    if skipped: note+=f" Its toll toward {skipped[0]}, already taken, is ignored."
    steps.append({"at":{"pop":len(cells)-1},"vars":{"cost":d,"truth":truth[u],"wrong":int(bad)},"note":note})
assert dist==[0,4,5,6,7] and truth==[0,0,5,2,3]
assert sum(s['vars']['wrong'] for s in steps)==3
fill(CH,F,block(cells,["pop"],steps),"@@TRACE2@@")
print(cells,dist,truth)
