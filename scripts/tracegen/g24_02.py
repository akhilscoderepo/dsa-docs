from common import *
import heapq
CH='24-shortest-paths-and-graph-state-modeling'
F='02-stale-heap-entries.md'
INF=float('inf')
def run(n,edges,k,log=None):
    adj=[[] for _ in range(n)]
    for a,b,w in edges: adj[a].append((b,w))
    dist=[INF]*n; dist[k]=0; h=[(0,k)]; pushes=1; stale=0; exam=0; pops=[]
    while h:
        d,u=heapq.heappop(h)
        st = d!=dist[u]
        pops.append((u,d,st,len(h)))
        if st: stale+=1; continue
        for v,w in adj[u]:
            exam+=1
            if d+w<dist[v]:
                dist[v]=d+w; heapq.heappush(h,(d+w,v)); pushes+=1
    return dist,pops,stale,pushes,exam
def delay(dist): return -1 if INF in dist else max(dist)
def build(n,edges,k):
    adj=[[] for _ in range(n)]
    for a,b,w in edges: adj[a].append((b,w))
    cur=[INF]*n; cur[k]=0; h=[(0,k)]; steps=[]; cells=[]; skipped=0
    while h:
        d,u=heapq.heappop(h); i=len(steps); cells.append(f"{u}@{d}")
        st=d!=cur[u]; added=[]
        if st: skipped+=1
        else:
            for v,w in adj[u]:
                if d+w<cur[v]: cur[v]=d+w; heapq.heappush(h,(d+w,v)); added.append(f"{v}@{d+w}")
        if st: note=f"Slip {u}@{d} comes off the tray, but the board shows depot {u} at {cur[u]}, so it is skipped without reading its roads."
        else: note=f"Slip {u}@{d} matches the board and is expanded; "+(f"it writes {', '.join(added)}." if added else "no neighbor improves.")
        steps.append({"at":{"cur":i},"vars":{"board":cur[u],"skipped":skipped,"tray":len(h)},"note":note})
    return cells,steps,cur,skipped
E1=[[0,1,7],[0,2,2],[2,1,3],[1,3,1],[2,3,9],[3,4,2]]
c1,s1,d1,k1=build(5,E1,0)
assert d1==[0,5,2,6,8] and k1==2 and delay(d1)==8
E2=[[0,1,4],[0,2,1],[0,3,1],[2,3,0],[2,1,3],[3,1,0],[1,4,2],[3,4,5]]
c2,s2,d2,k2=build(6,E2,0)
print(c1,d1,k1);print(c2,d2,k2, delay(d2))
assert d2[5]==INF and d2[:5]==[0,1,1,1,3] and k2==2
fill(CH,F,block(c1,["cur"],s1),"@@TRACE1@@")
fill(CH,F,block(c2,["cur"],s2),"@@TRACE2@@")
