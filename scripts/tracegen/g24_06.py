import sys
from collections import deque
from common import *
CH='24-shortest-paths-and-graph-state-modeling'
INF=10**9
def run(n,edges,ph,dry=False):
    adj=[[] for _ in range(n)]
    for a,b,w in edges: adj[a].append((b,w))
    dist=[INF]*n; dist[0]=0
    dq=deque([(0,0)]); st=[]
    D=lambda: " ".join("inf" if x==INF else str(x) for x in dist)
    Q=lambda: " ".join(f"{v}:{d}" for v,d in dq) if dq else "empty"
    def snap(cur,note): st.append({"at":{"cur":cur},"vars":{"dist":D(),"deque":Q()},"note":note})
    snap(0,"The deque holds the start vertex 0 with distance 0.")
    while dq:
        u,d=dq.popleft()
        if d>dist[u]:
            snap(u,f"The entry for vertex {u} carries distance {d}, but the best known distance is {dist[u]}, so the search skips it."); continue
        snap(u,f"The search takes vertex {u} with distance {d} from the front and scans its edges.")
        for v,w in adj[u]:
            nd=d+w
            if nd<dist[v]:
                dist[v]=nd
                if w==0: dq.appendleft((v,nd)); where="front"
                else: dq.append((v,nd)); where="back"
                snap(u,f"The edge from {u} to {v} costs {w} and gives distance {nd}, which is an improvement, so the search pushes vertex {v} at the {where}.")
            else:
                snap(u,f"The edge from {u} to {v} costs {w} and gives distance {nd}, which does not beat {dist[v]}, so the search discards it.")
    fill(CH,'06-zero-one-bfs.md',block(list(range(n)),["cur"],st),ph) if not dry else print(len(st),[ (i+1,s['note']) for i,s in enumerate(st)])
    return dist
dry = len(sys.argv)>1
d=run(5,[(0,1,1),(0,2,0),(2,3,0),(3,1,0),(1,4,1)],"@@TRACE1@@",dry); assert d==[0,0,0,0,1]
d=run(4,[(0,1,1),(0,2,1),(1,2,0),(2,1,0),(2,3,1)],"@@TRACE2@@",dry); assert d==[0,1,1,2]
