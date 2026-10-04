from common import *
from collections import deque
CH='23-directed-graphs-and-union-find'
F='01-kahn-topological-order.md'
def kahn(n, edges, expect_len):
    indeg=[0]*n; adj=[[] for _ in range(n)]
    for a,b in edges: adj[a].append(b); indeg[b]+=1
    q=deque(v for v in range(n) if indeg[v]==0)
    order=[]; steps=[]
    while q:
        cur=q.popleft(); idx=len(order); order.append(cur)
        added=[]
        for nx in adj[cur]:
            indeg[nx]-=1
            if indeg[nx]==0: q.append(nx); added.append(nx)
        note=f"Box {cur} is removed and written to the list."
        note+=(" It frees box "+", ".join(map(str,added))+"." if added else " It frees no new box.")
        steps.append({"at":{"cur":idx},"vars":{"indegree":" ".join(map(str,indeg)),"queue":" ".join(map(str,q)) or "empty"},"note":note})
    assert len(order)==expect_len, order
    return order, indeg, steps
# trace 1
e1=[(0,2),(1,2),(2,3),(2,4),(3,5),(4,5)]
o1,_,s1=kahn(7,e1,7)
assert o1==[0,1,6,2,3,4,5]
fill(CH,F,block(o1,["cur"],s1),"@@TRACE1@@")
# trace 2
e2=[(0,1),(1,2),(2,3),(3,1),(0,4),(4,5)]
o2,ind2,s2=kahn(6,e2,3)
assert o2==[0,4,5] and ind2[1:4]==[1,1,1]
s2.append({"at":{"cur":len(o2)},"vars":{"indegree":" ".join(map(str,ind2)),"queue":"empty"},"note":"The queue is empty with only 3 of 6 boxes written. Boxes 1, 2 and 3 still have indegree 1, so they form the stuck set and the answer is empty."})
fill(CH,F,block(o2,["cur"],s2),"@@TRACE2@@")
print(o1,o2)
# example checks
def indeg(n,E):
    r=[0]*n
    for a,b in E: r[b]+=1
    return r
assert indeg(5,[[0,1],[0,2],[3,2],[1,2],[0,1]])==[0,2,3,0,0]
assert indeg(4,[[2,2],[1,3]])==[0,0,1,1]
def kc(n,P):
    E=[(b,a) for a,b in P]; o,_,_=None,None,None
    indg=indeg(n,E); adj=[[] for _ in range(n)]
    for a,b in E: adj[a].append(b)
    q=deque(v for v in range(n) if indg[v]==0); order=[]
    while q:
        c=q.popleft(); order.append(c)
        for x in adj[c]:
            indg[x]-=1
            if indg[x]==0:q.append(x)
    return order
assert len(kc(4,[[1,0],[2,1],[3,2]]))==4
assert len(kc(5,[[1,0],[2,1],[1,2],[3,2],[4,3]]))==1
assert kc(5,[[1,3],[4,1]])==[0,2,3,1,4]
assert kc(4,[[1,0],[2,1],[1,2],[3,0]])==[0,3]
def rounds(n,E):
    indg=indeg(n,E); adj=[[] for _ in range(n)]
    for a,b in E: adj[a].append(b)
    cur=[v for v in range(n) if indg[v]==0]; r=0; done=0
    while cur:
        r+=1; done+=len(cur); nxt=[]
        for c in cur:
            for x in adj[c]:
                indg[x]-=1
                if indg[x]==0: nxt.append(x)
        cur=nxt
    return r if done==n else -1
assert rounds(6,[[0,1],[2,1],[1,3]])==3
assert rounds(4,[[1,2],[2,1]])==-1
