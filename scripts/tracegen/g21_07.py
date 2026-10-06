from common import *
from collections import deque
CH='21-graph-traversal-models-dfs-and-ordinary-bfs'; F='07-unweighted-shortest-paths.md'
def run(n,edges,ph):
    adj=[[] for _ in range(n)]
    for u,v in edges: adj[u].append(v); adj[v].append(u)
    dist=[-1]*n; dist[0]=0; q=deque([0]); st=[]; k=0
    while q:
        cur=q.popleft(); new=[]
        for x in adj[cur]:
            if dist[x]<0: dist[x]=dist[cur]+1; q.append(x); new.append(x)
        if new: note="The search takes vertex %d from the queue and discovers %s, each at distance %d."%(cur,", ".join(map(str,new)),dist[cur]+1)
        else: note=["Vertex %d comes off the queue, but all its neighbors are visited already, so nothing changes.","The queue gives vertex %d, and it has no undiscovered neighbor to add.","After taking vertex %d, the search finds nothing new to enqueue."][k%3]%cur
        k+=1
        st.append({"at":{"cur":cur},"vars":{"distance":",".join(map(str,dist)),"queue":"-".join(map(str,q)) or "empty"},"note":note})
    fill(CH,F,block(list(range(n)),["cur"],st),ph); return dist
assert run(6,[[0,1],[0,2],[1,3],[2,3],[3,4],[4,5]],"@@TRACE1@@")==[0,1,1,2,3,4]
assert run(6,[[0,1],[1,2],[0,2],[2,3],[4,5]],"@@TRACE2@@")==[0,1,1,2,-1,-1]
