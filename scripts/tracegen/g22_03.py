from common import *
CH='22-bfs-variations'
F='03-bidirectional-frontiers.md'

def run(n, edges, s, t, expect):
    adj=[[] for _ in range(n)]
    for a,b in edges: adj[a].append(b); adj[b].append(a)
    for l in adj: l.sort()
    fw=[-1]*n; fp=[-1]*n; fw[s]=0; fp[t]=0
    lw=[s]; lp=[t]; steps=[]; ans=None
    while lw and lp and ans is None:
        gw = len(lw) <= len(lp)
        layer, mine, other = (lw, fw, fp) if gw else (lp, fp, fw)
        fresh=[]
        for cur in layer:
            found=None; added=[]
            for nx in adj[cur]:
                if other[nx]>=0:
                    found=nx; ans=mine[cur]+1+other[nx]; break
                if mine[nx]>=0: continue
                mine[nx]=mine[cur]+1; fresh.append(nx); added.append(nx)
            side='west' if gw else 'pump'
            reached=lambda a: sum(1 for x in a if x>=0)
            if found is not None:
                note=(f"Chamber {cur} is expanded for the {side} side, and its neighbour {found} is already in the other table at distance {other[found]}, "
                      f"so the answer is {mine[cur]} + 1 + {other[found]} = {ans}.")
            else:
                note=(f"Chamber {cur} is expanded for the {side} side, and it reaches "+
                      (f"{len(added)} new chamber"+("s" if len(added)!=1 else "")+f" ({','.join(map(str,added))})." if added else "no new chamber."))
            steps.append({"at":{"cur":cur},"vars":{"side":"W" if gw else "P","west_reached":reached(fw),"pump_reached":reached(fp),"answer":ans if ans is not None else "none"},"note":note})
            if found is not None: break
        if ans is None:
            if gw: lw=fresh
            else: lp=fresh
    assert ans==expect, (ans,expect)
    return steps

# independent check with plain BFS
from collections import deque
def bfs(n,edges,s,t):
    adj=[[] for _ in range(n)]
    for a,b in edges: adj[a].append(b); adj[b].append(a)
    d=[-1]*n; d[s]=0; q=deque([s])
    while q:
        u=q.popleft()
        for v in adj[u]:
            if d[v]<0: d[v]=d[u]+1; q.append(v)
    return d[t]
e1=[(0,1),(0,2),(0,3),(1,4),(2,4),(3,5),(4,6),(5,6),(6,7)]
e2=[(0,1),(1,2),(2,3),(0,4)]
assert bfs(8,e1,0,7)==4 and bfs(5,e2,0,3)==3
s1=run(8,e1,0,7,4)
assert [x["vars"]["side"] for x in s1]==["W","P","P","P"]
fill(CH,F,block(list(range(8)),["cur"],s1),"@@TRACE1@@")
s2=run(5,e2,0,3,3)
assert [x["vars"]["side"] for x in s2]==['W','P','P']
print([x["vars"]["side"] for x in s2])
fill(CH,F,block(list(range(5)),["cur"],s2),"@@TRACE2@@")
