from common import *
import heapq, itertools
CH='25-advanced-graph-optimization'
F='08-mst-decisions.md'
INF=10**9
def mst_brute(n,E):
    # smallest total over every subset of n-1 offices-connecting cables
    best=None
    for sub in itertools.combinations(E,n-1):
        p=list(range(n))
        def f(x):
            while p[x]!=x: x=p[x]
            return x
        ok=True
        for a,b,c in sub:
            ra,rb=f(a),f(b)
            if ra==rb: ok=False;break
            p[ra]=rb
        if ok:
            t=sum(c for _,_,c in sub)
            if best is None or t<best: best=t
    return best
# trace 1: dense Prim, cut = joined offices versus the rest
n1=6; e1=[(0,1,4),(0,2,3),(1,2,1),(1,3,2),(2,3,4),(3,4,2),(4,5,6),(3,5,5)]
w={}
for a,b,c in e1: w[(a,b)]=w[(b,a)]=c
best=[INF]*n1; par=[-1]*n1; inn=[False]*n1; best[0]=0; tot=0; cells=[]; steps=[]
for k in range(n1):
    u=min((v for v in range(n1) if not inn[v]),key=lambda v:(best[v],v))
    inn[u]=True; tot+=best[u]; cells.append(f"{u}@{best[u]}")
    imp=[]
    for v in range(n1):
        if not inn[v] and (u,v) in w and w[(u,v)]<best[v]:
            best[v]=w[(u,v)]; par[v]=u; imp.append(f"{v} to {best[v]}")
    if k==0: head="Office 0 starts the tree at no cost"
    else: head=f"Office {u} joins through office {par[u]} at weight {best[u]}, the lightest edge leaving the tree"
    steps.append({"at":{"add":k},"vars":{"weight":best[u],"total":tot,"improved":len(imp)},
      "note":head+"; "+(("it lowers the best weight of "+", ".join(imp)+".") if imp else "it lowers no best weight.")+f" The total is {tot}."})
assert tot==13 and tot==mst_brute(n1,e1)
assert [c.split('@')[0] for c in cells]==['0','2','1','3','4','5']
assert [s['vars']['improved'] for s in steps]==[2,2,1,2,0,0]
fill(CH,F,block(cells,["add"],steps),"@@TRACE1@@")
print(cells,tot)
# trace 2: false friend, the shortest-path tree from office 0
n2=5; e2=[(0,1,5),(0,2,5),(1,2,1),(2,3,2),(3,4,1),(0,4,9)]
g=[[] for _ in range(n2)]
for a,b,c in e2: g[a].append((b,c)); g[b].append((a,c))
d=[INF]*n2; d[0]=0; pw=[0]*n2; par=[-1]*n2; h=[(0,0)]; done=[False]*n2; tot=0; cells=[]; steps=[]
while h:
    x,u=heapq.heappop(h)
    if done[u]: continue
    done[u]=True; tot+=pw[u]; cells.append(f"{u}@{x}")
    k=len(cells)-1
    if k==0: note="Office 0 is the hub and costs nothing."
    else: note=f"Office {u} is reached at distance {x} through office {par[u]}, and its last cable weighs {pw[u]}. The cable total is {tot}."
    steps.append({"at":{"settle":k},"vars":{"distance":x,"cable":pw[u],"total":tot},"note":note})
    for v,c in g[u]:
        if x+c<d[v]: d[v]=x+c; par[v]=u; pw[v]=c; heapq.heappush(h,(d[v],v))
mst=mst_brute(n2,e2)
assert tot==13 and mst==9 and [c.split('@')[0] for c in cells]==['0','1','2','3','4']
steps[-1]["note"]+=f" The cheapest tree for these cables totals {mst}, so the shortest-path tree overpays by {tot-mst}."
fill(CH,F,block(cells,["settle"],steps),"@@TRACE2@@")
print(cells,tot,mst)
