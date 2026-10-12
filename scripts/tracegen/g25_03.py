from common import *
import heapq
CH='25-advanced-graph-optimization'
F='03-prim.md'
def adj(n,edges):
    g=[[] for _ in range(n)]
    for a,b,w in edges: g[a].append((b,w)); g[b].append((a,w))
    return g
def kruskal(n,edges):
    p=list(range(n))
    def f(x):
        while p[x]!=x: p[x]=p[p[x]]; x=p[x]
        return x
    t=0
    for a,b,w in sorted(edges,key=lambda e:e[2]):
        if f(a)!=f(b): p[f(a)]=f(b); t+=w
    return t
# trace 1: lazy Prim with stale entries
n1=6; e1=[(0,1,4),(0,2,3),(1,2,1),(1,3,2),(2,3,4),(2,4,5),(3,4,6),(4,5,3),(3,5,7)]
g=adj(n1,e1); inT=[False]*n1; h=[(0,0)]; cells=[]; steps=[]; total=0
while h:
    w,v=heapq.heappop(h)
    cells.append(f"{v}@{w}")
    if inT[v]:
        steps.append({"at":{"pop":len(cells)-1},"vars":{"w":w,"heap":len(h),"total":total},"note":f"The heap returns {v}@{w} as its smallest entry, yet vertex {v} joined earlier through a lighter edge, so the method discards this stale entry and the total stays {total}."}); continue
    inT[v]=True; total+=w; pushed=[]
    for u,x in g[v]:
        if not inT[u]: heapq.heappush(h,(x,u)); pushed.append(f"{u}@{x}")
    steps.append({"at":{"pop":len(cells)-1},"vars":{"w":w,"heap":len(h),"total":total},
      "note":f"The cheapest crossing edge has weight {w}, so vertex {v} joins and the total becomes {total}. "+(("Its edges to outside vertices put "+", ".join(pushed)+" into the heap.") if pushed else "No outside vertex remains next to it, so nothing enters the heap.")})
assert total==kruskal(n1,e1)==14 and all(inT)
assert sum('stale' in s['note'] for s in steps)==4
fill(CH,F,block(cells,["pop"],steps),"@@TRACE1@@")
print(cells,total)
# trace 2: false friend, heap key is the distance from vertex 0 (Dijkstra key)
n2=6; e2=[(0,1,5),(0,2,6),(0,3,7),(0,4,8),(0,5,9),(1,2,2),(2,3,2),(3,4,2),(4,5,2)]
g=adj(n2,e2); mst=kruskal(n2,e2); assert mst==13
dist=[10**9]*n2; dist[0]=0; inT=[False]*n2; h=[(0,0,0)]; cells=[]; steps=[]; total=0
while h:
    k,v,w=heapq.heappop(h)
    if inT[v]: continue
    inT[v]=True; total+=w; cells.append(f"{v}@{k}")
    for u,x in g[v]:
        if not inT[u] and k+x<dist[u]:
            dist[u]=k+x; heapq.heappush(h,(dist[u],u,x))
    steps.append({"at":{"pop":len(cells)-1},"vars":{"key":k,"edge":w,"total":total},
      "note":f"Key {k} is the smallest distance from vertex 0, so vertex {v} is taken next, and the edge that attaches it weighs {w}. The running tree weight grows to {total}."})
assert total==35 and mst==13
steps[-1]["note"]+=f" The minimum spanning tree weighs {mst}, so this tree is {total-mst} too heavy."
fill(CH,F,block(cells,["pop"],steps),"@@TRACE2@@")
print(cells,total,mst)
