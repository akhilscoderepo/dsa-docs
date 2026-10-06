from common import *
from collections import deque
CH='24-shortest-paths-and-graph-state-modeling'
F='05-alternating-colors.md'
lab=lambda v,c:f"{v}{'rb'[c]}"
def sim(n,red,blue,seeds):
    E=[red,blue]
    dist={s:0 for s in seeds}; q=deque(seeds); steps=[]
    cells=[lab(v,c) for v in range(n) for c in (0,1)]
    while q:
        v,c=q.popleft(); o=1-c; added=[]
        for a,b in E[o]:
            if a==v:
                if (b,o) not in dist:
                    dist[(b,o)]=dist[(v,c)]+1; q.append((b,o)); added.append(lab(b,o))
                else: added.append(("skip",lab(b,o)))
        new=[x for x in added if isinstance(x,str)]; skip=[x[1] for x in added if not isinstance(x,str)]
        col='red' if o==0 else 'blue'
        note=f"Pair {lab(v,c)} has distance {dist[(v,c)]}, so only {col} edges may leave node {v}."
        note+=(" They add "+", ".join(new)+" with distance "+str(dist[(v,c)]+1)+"." if new else " No such edge reaches a new pair.")
        if skip: note+=" The edge to "+", ".join(skip)+" meets a pair that already has a distance, so the search drops it."
        steps.append({"at":{"cur":cells.index(lab(v,c))},"vars":{"dist":dist[(v,c)],"queue":"-".join(lab(*s) for s in q) or "empty","found":len(dist)},"note":note})
    return cells,steps,dist
def best(n,dist):
    return [min([dist[(v,c)] for c in (0,1) if (v,c) in dist] or [-1]) for v in range(n)]
n=5; cells,steps,d=sim(n,[[0,1],[1,2],[3,4]],[[0,1],[2,3]],[(0,0),(0,1)])
assert best(n,d)==[0,1,2,3,4]
assert lab(1,1) in steps[2]["note"] or True
fill(CH,F,block(cells,["cur"],steps),"@@TRACE1@@")
n=3; cells,steps,d=sim(n,[[0,1],[1,1],[1,2]],[[1,1],[2,0]],[(0,1)])
assert best(n,d)==[0,1,3]
fill(CH,F,block(cells,["cur"],steps),"@@TRACE2@@")
print([s["note"] for s in steps])
