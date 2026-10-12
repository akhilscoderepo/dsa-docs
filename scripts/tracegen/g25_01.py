from common import *
CH='25-advanced-graph-optimization'
F='01-bellman-ford.md'
INF=float('inf')
def show(d):
    return "[" + ", ".join("unknown" if x==INF else str(x) for x in d) + "]"
def run(n,edges,src,passes):
    """Run snapshot passes; return cells and steps for the trace block."""
    d=[INF]*n; d[src]=0
    cells=["start"]; steps=[{"at":{"pass":0},"vars":{"improved":0,"reached":1},"note":f"Before pass 1, the table holds only the source fee: {show(d)}."}]
    hist=[list(d)]
    for p in range(1,passes+1):
        prev=list(d); imp=0
        for u,v,w in edges:
            if prev[u]!=INF and prev[u]+w<d[v]:
                d[v]=prev[u]+w; imp+=1
        cells.append(f"pass {p}")
        phr=["Pass {p} reads the start values and improves {imp} entr{y}; the table now reads {s}.","Reading the previous table, pass {p} writes {imp} cheaper entr{y}, giving {s}.","In pass {p}, {imp} entr{y} drop below the stored value, leaving {s}.","Pass {p} still finds {imp} cheaper entr{y}, and the table becomes {s}.","Pass {p} produces {imp} further change{z}, so the table is {s}."][(p-1)%5]
        note=phr.format(p=p,imp=imp,y="y" if imp==1 else "ies",z="" if imp==1 else "s",s=show(d)) if imp else f"Pass {p} finds nothing cheaper, so the table stays {show(d)} and the method stops."
        steps.append({"at":{"pass":p},"vars":{"improved":imp,"reached":sum(1 for x in d if x!=INF)},"note":note})
        hist.append(list(d))
    return cells,steps,d,hist
def oracle(n,edges,src):
    d=[INF]*n; d[src]=0
    for _ in range(n):
        for u,v,w in edges:
            if d[u]!=INF and d[u]+w<d[v]: d[v]=d[u]+w
    return d
# trace 1
e1=[(0,1,6),(0,2,5),(0,3,5),(1,4,-1),(2,1,-2),(2,4,1),(3,2,-2),(3,5,-1)]
cells,steps,d,hist=run(6,e1,0,5)
assert d==[0,1,3,5,0,4]==oracle(6,e1,0)
assert [s['vars']['improved'] for s in steps]==[0,3,4,2,1,0]
assert hist[1]==[0,6,5,5,INF,INF] and hist[2]==[0,3,3,5,5,4] and hist[3]==[0,1,3,5,2,4] and hist[4]==[0,1,3,5,0,4]
fill(CH,F,block(cells,["pass"],steps),"@@TRACE1@@")
# trace 2: negative cycle reachable
e2=[(0,1,2),(1,2,-3),(2,1,1),(2,3,4)]
cells,steps,d,hist=run(4,e2,0,4)
for s in steps: s['vars']['limit']=3
assert [s['vars']['improved'] for s in steps]==[0,1,1,2,1]
assert hist[1]==[0,2,INF,INF] and hist[2]==[0,2,-1,INF] and hist[3]==[0,0,-1,3] and hist[4]==[0,0,-3,3]
steps[4]['note']+=" This pass is the extra one, so a negative cycle is reachable."
fill(CH,F,block(cells,["pass"],steps),"@@TRACE2@@")
print("ok")
