from common import *
import sys
sys.setrecursionlimit(10000)
CH='25-advanced-graph-optimization'
F='07-low-links.md'
def adjl(n,edges):
    g=[[] for _ in range(n)]
    for i,(a,b) in enumerate(edges): g[a].append((b,i)); g[b].append((a,i))
    return g
def truth_bridges(n,edges):
    """Brute force: an edge is a bridge when its removal disconnects its endpoints."""
    out=set()
    for i,(a,b) in enumerate(edges):
        seen={a}; st=[a]
        while st:
            x=st.pop()
            for y,j in adjl(n,edges)[x]:
                if j!=i and y not in seen: seen.add(y); st.append(y)
        if b not in seen: out.add((min(a,b),max(a,b)))
    return out
def run(n,edges,by_vertex):
    """DFS from vertex 0. by_vertex=True skips the parent vertex (the hazard), else the parent edge id."""
    g=adjl(n,edges); disc=[-1]*n; low=[0]*n; order=[]; steps=[]; flagged=[]; tr=truth_bridges(n,edges)
    def snap(u,note):
        steps.append({"at":{"at":disc[u]},"vars":{"disc":disc[u],"low":low[u],"flagged":len(flagged)},"note":note})
    def go(u,pe,pv):
        disc[u]=low[u]=len(order); order.append(u)
        snap(u,f"Vertex {u} is discovered at time {disc[u]}, so disc and low both start at {disc[u]}.")
        for v,i in g[u]:
            if (by_vertex and v==pv) or (not by_vertex and i==pe): continue
            if disc[v]==-1:
                go(v,i,u)
                old=low[u]; low[u]=min(low[u],low[v])
                bad=low[v]>disc[u]
                if bad: flagged.append((min(u,v),max(u,v)))
                note=f"Child {v} returns with low {low[v]}. Vertex {u} has disc {disc[u]}, and {low[v]} "+("exceeds" if bad else "does not exceed")+f" {disc[u]}, so edge {u}-{v} "+("is a bridge" if bad else "is not a bridge")+"."
                if bad and (min(u,v),max(u,v)) not in tr: note+=" The edge has a twin cable, so this answer is wrong."
                snap(u,note)
            elif disc[v]<disc[u]:
                old=low[u]; low[u]=min(low[u],disc[v])
                snap(u,f"Vertex {u} sees the back edge to vertex {v} with disc {disc[v]}, so low becomes {low[u]}.")
    go(0,-1,-1)
    return order,steps,set(flagged),tr,low,disc
# trace 1: two bridges, correct rule
n1=7; e1=[(0,1),(1,2),(2,0),(2,3),(3,4),(4,5),(5,3),(5,6)]
order,steps,fl,tr,low,disc=run(n1,e1,False)
assert order==[0,1,2,3,4,5,6] and fl==tr=={(2,3),(5,6)}
assert low==[0,0,0,3,3,3,6], low
assert len(steps)==15, len(steps)
fill(CH,F,block([f"v{v}" for v in order],["at"],steps),"@@TRACE1@@")
print(steps[-1],low)
# trace 2: skipping the parent vertex flags a bridge that is not one
n2=4; e2=[(0,1),(1,2),(1,2),(2,3)]
order,steps,fl,tr,low,disc=run(n2,e2,True)
assert tr=={(0,1),(2,3)} and fl=={(0,1),(1,2),(2,3)}
good=run(n2,e2,False)
assert good[2]==tr
assert good[4]==[0,1,1,3]
assert len(steps)==7, len(steps)
fill(CH,F,block([f"v{v}" for v in order],["at"],steps),"@@TRACE2@@")
print(order,low,steps)
