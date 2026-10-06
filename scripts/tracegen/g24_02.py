import heapq
from common import *
CH='24-shortest-paths-and-graph-state-modeling'
INF=float('inf')
def sim(n,edges,src,ph=None,tick=False):
    adj=[[] for _ in range(n)]
    for u,v,w in edges: adj[u].append((v,w))
    dist=[INF]*n; dist[src]=0; heap=[(0,src)]; st=[]
    pushes=1; stale=0; ties=0; scans=0
    D=lambda: ",".join("-" if x==INF else str(x) for x in dist)
    H=lambda: " ".join(f"{d}:{x}" for d,x in sorted(heap)) or "empty"
    def snap(u,v,note): st.append({"at":{"u":u,"v":v},"vars":{"dist":D(),"heap":H()},"note":note})
    if ph: snap(-1,-1,f"The heap holds the single entry for source {src} with distance 0.")
    while heap:
        d,u=heapq.heappop(heap)
        if d!=dist[u]:
            stale+=1
            if ph: snap(u,-1,f"The method pops the entry {d}:{u}. The stored distance of {u} is {dist[u]}, so the entry is outdated and the method skips it.")
            continue
        if ph: snap(u,-1,f"The method pops the entry {d}:{u}. It equals the stored distance, so the method expands vertex {u}.")
        for v,w in adj[u]:
            scans+=1; nd=d+w
            if nd<dist[v]:
                dist[v]=nd; heapq.heappush(heap,(nd,v)); pushes+=1
                if ph: snap(u,v,f"The edge from {u} to {v} offers {nd}, which beats the stored value, so the method stores it and pushes {nd}:{v}.")
            else:
                if nd==dist[v]: ties+=1
                if ph: snap(u,v,f"The edge from {u} to {v} offers {nd}, which does not beat {dist[v]}, so the method pushes nothing.")
    if ph: fill(CH,'02-stale-heap-entries.md',block(list(range(n)),["u","v"],st),ph)
    return dist,pushes,stale,ties,scans
E1=[(0,1,7),(0,2,2),(2,1,3),(1,3,1),(2,3,9),(3,4,2)]
d,p,s,t,sc=sim(5,E1,0,"@@TRACE1@@"); assert d==[0,5,2,6,8] and s==2 and p==7
E2=[(0,1,2),(0,2,2),(1,3,2),(2,3,2),(3,4,1)]
d,p,s,t,sc=sim(5,E2,0,"@@TRACE2@@"); assert d==[0,2,2,4,5] and t==1 and s==0
