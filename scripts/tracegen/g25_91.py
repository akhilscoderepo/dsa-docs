from common import *
CH='25-advanced-graph-optimization'
F='91-choose-a-method-for-each-graph-goal.md'
def find(p,x):
    while p[x]!=x:
        p[x]=p[p[x]]; x=p[x]
    return x
def groups_str(p,n):
    g={}
    for v in range(n): g.setdefault(find(p,v),[]).append(v)
    return " ".join("{"+",".join(map(str,m))+"}" for m in sorted(g.values()))
# trace 1: Kruskal with union-find, one skip, early stop
pts=[(0,0),(1,3),(3,2),(2,6),(6,5)]; n=len(pts)
E=sorted((abs(pts[i][0]-pts[j][0])+abs(pts[i][1]-pts[j][1]),i,j) for i in range(n) for j in range(i+1,n))
cells=[f"{i}-{j}@{w}" for w,i,j in E]
p=list(range(n)); total=0; groups=n; skips=[]
steps=[{"at":{"edge":-1},"vars":{"groups":groups_str(p,n),"total":0},"note":"Five groups of one site each. No cable is bought."}]
last=None
for k,(w,i,j) in enumerate(E):
    a,b=find(p,i),find(p,j)
    if a==b:
        skips.append(cells[k])
        steps.append({"at":{"edge":k},"vars":{"groups":groups_str(p,n),"total":total},"note":f"Cable {i}-{j}@{w}: sites {i} and {j} share root {a}, so the cable would close a cycle and the loop skips it."})
        continue
    p[a]=b; total+=w; groups-=1
    note=f"Cable {i}-{j}@{w} joins two groups, so the loop buys it." + (f" {groups} groups remain." if groups>1 else "")
    if groups==1:
        note+=f" Only one group remains, so the loop stops and never reads the last {len(E)-k-1} cables."
    steps.append({"at":{"edge":k},"vars":{"groups":groups_str(p,n),"total":total},"note":note})
    if groups==1: break
assert total==16 and skips==["0-2@5","2-3@5"] and len(E)-k-1==4 and cells[k]=="3-4@5"
fill(CH,F,block(cells,["edge"],steps),"@@TRACE1@@")
# trace 2: shortest path tree on the cabling request
n2=4; L=[(0,1,4),(0,2,5),(1,2,2),(2,3,2)]
INF=10**9; dist=[INF]*n2; dist[0]=0; done=[False]*n2; via=[0]*n2; bought=0
D=lambda: ",".join("inf" if x==INF else str(x) for x in dist)
steps=[{"at":{"site":0},"vars":{"dist":D(),"bought":0},"note":"Only site 0 has a distance. Nothing is bought."}]
for _ in range(n2):
    u=min((v for v in range(n2) if not done[v] and dist[v]<INF),key=lambda v:dist[v])
    done[u]=True; bought+=via[u]; ex=""
    for a,b,w in L:
        o=b if a==u else a if b==u else -1
        if o>=0 and not done[o] and dist[u]+w<dist[o]:
            dist[o]=dist[u]+w; via[o]=w
    if u==0: note="Site 0 is final at distance 0. Its links give site 1 the distance 4 and site 2 the distance 5."
    elif u==1: note=f"Site 1 is final at distance 4, and the routine buys the link of cost 4. Route 0-1-2 costs 6, which is more than the stored 5, so site 2 keeps 5."
    elif u==2: note=f"Site 2 is final at distance 5, and the routine buys the direct link of cost 5. The cheap link 1-2@2 stays unbought. Site 3 gets distance 7."
    else: note=f"Site 3 is final at distance 7, and the routine buys the link of cost 2. The total is {bought}."
    steps.append({"at":{"site":u},"vars":{"dist":D(),"bought":bought},"note":note})
assert bought==11 and dist==[0,4,5,7]
# Kruskal on the same links
p=list(range(n2)); k=0
for a,b,w in sorted(L,key=lambda e:e[2]):
    x,y=find(p,a),find(p,b)
    if x!=y: p[x]=y; k+=w
assert k==8
fill(CH,F,block(list(range(n2)),["site"],steps),"@@TRACE2@@")
# exercise examples and checks
# reference solutions for the exercise examples
import itertools
def groups_cost(pts,g):
    n=len(pts)
    E=sorted((abs(pts[i][0]-pts[j][0])+abs(pts[i][1]-pts[j][1]),i,j) for i in range(n) for j in range(i+1,n))
    p=list(range(n)); gr=n; t=0
    for w,i,j in E:
        if gr==g: break
        a,b=find(p,i),find(p,j)
        if a==b: continue
        p[a]=b; gr-=1; t+=w
    return t
def bridges_by_size(n,conn,s):
    out=[]
    for k,(a,b) in enumerate(conn):
        adj=[[] for _ in range(n)]
        for q,(x,y) in enumerate(conn):
            if q!=k: adj[x].append(y); adj[y].append(x)
        seen={a}; st=[a]
        while st:
            u=st.pop()
            for v in adj[u]:
                if v not in seen: seen.add(v); st.append(v)
        if b not in seen:
            if len(seen)>=s and n-len(seen)>=s: out.append([min(a,b),max(a,b)])
    return sorted(out)
def city(n,edges,t):
    INF=10**18
    d=[[INF]*n for _ in range(n)]
    for i in range(n): d[i][i]=0
    for a,b,w in edges:
        d[a][b]=min(d[a][b],w); d[b][a]=min(d[b][a],w)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][k]<INF and d[k][j]<INF and d[i][k]+d[k][j]<d[i][j]: d[i][j]=d[i][k]+d[k][j]
    cnt=[sum(1 for j in range(n) if j!=i and d[i][j]<t) for i in range(n)]
    m=min(cnt); return max(i for i in range(n) if cnt[i]==m),cnt
def itin(tickets):
    best=[None]
    m=len(tickets)
    def go(cur,path,used):
        if len(path)==m+1:
            if best[0] is None or path<best[0]: best[0]=path[:]
            return
        for k,(a,b) in enumerate(tickets):
            if not used[k] and a==cur:
                used[k]=True; path.append(b); go(b,path,used); path.pop(); used[k]=False
    go("JFK",["JFK"],[False]*m); return best[0]

P=[[1,1],[3,4],[8,1],[6,6],[2,7]]
assert groups_cost(P,2)==14 and groups_cost(P,5)==0
cn=[[0,1],[1,2],[2,0],[1,3],[3,4],[4,5],[5,3],[3,6],[6,7]]
assert bridges_by_size(8,cn,2)==[[1,3],[3,6]] and bridges_by_size(4,[[0,1],[1,2],[2,3]],2)==[[1,2]]
rd=[[0,1,3],[1,2,1],[1,3,4],[2,3,1]]
assert city(4,rd,5)[0]==3 and city(4,rd,3)[0]==0
assert itin([["JFK","SFO"],["JFK","ATL"],["SFO","ATL"],["ATL","JFK"],["ATL","SFO"]])==["JFK","ATL","JFK","SFO","ATL","SFO"]
assert itin([["JFK","AAA"],["AAA","JFK"],["JFK","AAA"],["AAA","BBB"]])==["JFK","AAA","JFK","AAA","BBB"]
