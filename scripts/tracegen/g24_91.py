import heapq
from common import *
CH='24-shortest-paths-and-graph-state-modeling'
INF=10**9
def fmt(h): return " ".join(f"({a},{b})" if len(t:=(a,b))==2 else "" for a,b in sorted(h)) or "empty"
def delay_trace(n,edges,src,ph):
    adj=[[] for _ in range(n)]
    for a,b,w in edges: adj[a].append((b,w))
    dist=[INF]*n; dist[src]=0; heap=[(0,src)]; st=[]
    D=lambda: ",".join("inf" if x==INF else str(x) for x in dist)
    def snap(node,note): st.append({"at":{"node":node},"vars":{"dist":D(),"heap":fmt(heap)},"note":note})
    snap(src,f"Only the source has a distance. The heap starts with the entry (0,{src}).")
    while heap:
        d,u=heapq.heappop(heap)
        if d>dist[u]:
            snap(u,f"Entry ({d},{u}) comes out, yet dist[{u}] already holds {dist[u]}. The entry is stale and the loop drops it."); continue
        for v,w in adj[u]:
            if d+w<dist[v]:
                dist[v]=d+w; heapq.heappush(heap,(d+w,v))
        snap(u,f"Node {u} is final at distance {d}, and its links are read.")
    fill(CH,'91-shortest-paths-with-a-heap.md',block(list(range(n)),["node"],st),ph)
    return dist
def flights_trace(n,fl,src,dst,k,ph):
    adj=[[] for _ in range(n)]
    for a,b,p in fl: adj[a].append((b,p))
    best={(src,0):0}; heap=[(0,0,src)]; st=[]; ans=None
    H=lambda: " ".join(f"({c},{u},{e})" for c,e,u in sorted(heap)) or "empty"
    def snap(node,note): st.append({"at":{"city":node},"vars":{"heap":H()},"note":note})
    snap(src,f"The heap starts with (0,{src},0), read as cost 0, city {src}, no flight used yet.")
    while heap:
        c,e,u=heapq.heappop(heap)
        if c>best.get((u,e),INF):
            snap(u,f"Entry ({c},{u},{e}) costs more than best for that state, so the loop discards it."); continue
        if u==dst:
            ans=(c,e-1); snap(u,f"City {u} is the destination. Its first current entry gives price {c} with {e-1} stop, and the search ends."); break
        if e==k+1:
            snap(u,f"Entry ({c},{u},{e}) has spent all {k+1} allowed flights, so no flight leaves it."); continue
        for v,p in adj[u]:
            if c+p<best.get((v,e+1),INF):
                best[(v,e+1)]=c+p; heapq.heappush(heap,(c+p,e+1,v))
        snap(u,f"Entry ({c},{u},{e}) is current. Each flight from city {u} adds an entry with {e+1} flights used when it beats the stored price.")
    fill(CH,'91-shortest-paths-with-a-heap.md',block(list(range(n)),["city"],st),ph)
    return ans
d=delay_trace(4,[(0,1,4),(0,2,1),(2,1,2),(1,3,1)],0,"@@TRACE1@@"); assert d==[0,3,1,4]
a=flights_trace(4,[(0,1,1),(1,2,1),(0,2,5),(2,3,1)],0,3,1,"@@TRACE2@@"); assert a==(6,1)
