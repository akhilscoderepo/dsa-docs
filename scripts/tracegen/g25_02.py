from common import *
CH='25-advanced-graph-optimization'
F='02-floyd-warshall.md'
INF=float('inf')
def table(n,edges):
    d=[[INF]*n for _ in range(n)]
    for i in range(n): d[i][i]=0
    for u,v,w in edges: d[u][v]=min(d[u][v],w)
    return d
def truth_by_paths(n,edges):
    # independent oracle: Bellman style repeated passes from every source
    out=[]
    for s in range(n):
        d=[INF]*n; d[s]=0
        for _ in range(n):
            for u,v,w in edges:
                if d[u]+w<d[v]: d[v]=d[u]+w
        out.append(d)
    return out
def known(d): return sum(1 for i in range(len(d)) for j in range(len(d)) if i!=j and d[i][j]<INF)
# trace 1: correct loop order, one cell per intermediate
n1=5; e1=[(0,1,4),(0,2,1),(2,1,2),(1,3,1),(2,3,5),(3,4,3),(4,0,2)]
d=table(n1,e1); cells=[]; steps=[]
for k in range(n1):
    lowered=[]
    for i in range(n1):
        for j in range(n1):
            if d[i][k]+d[k][j]<d[i][j]:
                d[i][j]=d[i][k]+d[k][j]; lowered.append((i,j))
    cells.append(f"k={k}")
    if lowered:
        i,j=lowered[0]
        note=f"Intermediate {k} lowers {len(lowered)} {'pair' if len(lowered)==1 else 'pairs'}; the first is {i} to {j}, now {d[i][j]}."
    else:
        note=f"Intermediate {k} lowers no pair, because no route through it beats a stored distance."
    steps.append({"at":{"k":k},"vars":{"lowered":len(lowered),"known":known(d)},"note":note})
assert d==truth_by_paths(n1,e1)
print(cells,steps,d)
fill(CH,F,block(cells,["k"],steps),"@@TRACE1@@")
# trace 2: loop order with the intermediate innermost, one pass
n2=5; e2=[(0,1,2),(1,2,2),(2,3,3),(3,4,6),(4,0,5)]
truth=truth_by_paths(n2,e2)
d=table(n2,e2); cells=[]; steps=[]; total=0
for i in range(n2):
    for j in range(n2):
        for k in range(n2):
            if d[i][k]+d[k][j]<d[i][j]: d[i][j]=d[i][k]+d[k][j]
    wrong=[j for j in range(n2) if d[i][j]!=truth[i][j]]
    total+=len(wrong)
    cells.append(f"row {i}")
    note=f"Row {i} ends with {len(wrong)} wrong {'entry' if len(wrong)==1 else 'entries'}."
    if wrong:
        j=wrong[0]
        note+=f" For example {i} to {j} holds {'no route' if d[i][j]==INF else d[i][j]}, but the cheapest route costs {truth[i][j]}."
    steps.append({"at":{"i":i},"vars":{"wrong":len(wrong),"total":total},"note":note})
print(cells,steps,total)
fill(CH,F,block(cells,["i"],steps),"@@TRACE2@@")
