from common import *
from collections import deque
CH='22-bfs-variations'; F='01-multi-source-bfs.md'
def qs(q): return "-".join(map(str,q)) if q else "empty"
# Trace 1: two sources on a graph with a branch.
n=7; edges=[(0,1),(1,2),(2,3),(3,4),(4,5),(2,6)]; src=[0,5]
adj=[[] for _ in range(n)]
for a,b in edges: adj[a].append(b); adj[b].append(a)
dist=[-1]*n; q=deque()
for s in src: dist[s]=0; q.append(s)
st=[]
while q:
    cur=q.popleft(); new=[]
    for nx in adj[cur]:
        if dist[nx]==-1: dist[nx]=dist[cur]+1; q.append(nx); new.append(nx)
    note=(f"The search takes vertex {cur} from the queue and discovers "+", ".join(map(str,new))+f" at distance {dist[cur]+1}.") if new else f"The search takes vertex {cur} from the queue and finds no undiscovered neighbor."
    st.append({"at":{"cur":cur},"vars":{"distance":",".join(map(str,dist)),"queue":qs(list(q))},"note":note})
assert dist==[0,1,2,2,1,0,3]
fill(CH,F,block(list(range(n)),["cur"],st),"@@TRACE1@@")
# Trace 2: grid 3x3 row by row, one rotten source.
g=[2,1,1,1,1,0,0,1,1]; R=C=3
dist=[-1]*9; q=deque([0]); dist[0]=0; st=[]
while q:
    cur=q.popleft(); r,c=divmod(cur,C); new=[]
    for dr,dc in((1,0),(-1,0),(0,1),(0,-1)):
        a,b=r+dr,c+dc
        if 0<=a<R and 0<=b<C and g[a*C+b]==1 and dist[a*C+b]==-1:
            dist[a*C+b]=dist[cur]+1; q.append(a*C+b); new.append(a*C+b)
    note=(f"The search takes cell {cur} from the queue and discovers cell"+("s " if len(new)>1 else " ")+" and ".join(map(str,new))+f" at distance {dist[cur]+1}.") if new else f"The search takes cell {cur} from the queue and finds no fresh neighbor."
    st.append({"at":{"cur":cur},"vars":{"distance":",".join(map(str,dist)),"queue":qs(list(q))},"note":note})
assert max(dist)==4 and dist[8]==4 and dist[5]==-1 and dist[6]==-1
fill(CH,F,block(g,["cur"],st),"@@TRACE2@@")
