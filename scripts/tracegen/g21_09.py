from common import *
CH='21-graph-traversal-models-dfs-and-ordinary-bfs'
F='09-cycle-detection.md'

def closure_cycle(n, edges):
    r=[[False]*n for _ in range(n)]
    for a,b in edges: r[a][b]=True
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if r[i][k] and r[k][j]: r[i][j]=True
    return any(r[i][i] for i in range(n))

# trace 1: directed, no cycle
n=5; E=[(0,1),(0,2),(1,3),(2,3),(3,4)]
out=[[b for a,b in E if a==v] for v in range(n)]
mark=[0]*n; steps=[]; found=False
def snap(): return " ".join(map(str,mark))
def enter(v, via):
    global found
    mark[v]=1
    steps.append({"at":{"cur":v},"vars":{"marks":snap()},"note":f"Card {v} is entered"+(f" from card {via}" if via is not None else " as a start")+" and marked 1."})
    for w in out[v]:
        if mark[w]==1:
            found=True; return
        if mark[w]==0:
            enter(w,v)
        else:
            steps.append({"at":{"cur":v},"vars":{"marks":snap()},"note":f"Card {v} looks at card {w}, which is marked 2, so the edge is harmless and is not followed."})
    mark[v]=2
    steps.append({"at":{"cur":v},"vars":{"marks":snap()},"note":f"Card {v} has no more needs, so it leaves the route and is marked 2."})
for s in range(n):
    if mark[s]==0: enter(s,None)
assert not found and not closure_cycle(n,E) and mark==[2]*n
assert any("marked 2, so the edge is harmless" in s["note"] for s in steps)
fill(CH,F,block(list(range(n)),["cur"],steps),"@@TRACE1@@")

# trace 2: undirected, cycle
n=5; U=[(0,1),(1,2),(2,3),(3,1),(3,4)]
adj=[[] for _ in range(n)]
for i,(a,b) in enumerate(U):
    adj[a].append((b,i)); adj[b].append((a,i))
seen=[False]*n; route=[]; steps=[]; res=[None]
def reach(v, frm):
    seen[v]=True; route.append(v)
    steps.append({"at":{"cur":v},"vars":{"route":">".join(map(str,route)),"arrived_by":frm},"note":f"Vertex {v} is entered"+(f" by edge {frm}" if frm>=0 else " as a start")+"."})
    for w,i in adj[v]:
        if i==frm:
            steps.append({"at":{"cur":v},"vars":{"route":">".join(map(str,route)),"arrived_by":frm},"note":f"Edge {i} to vertex {w} is the edge the walk arrived by, so it is skipped."})
            continue
        if seen[w]:
            steps.append({"at":{"cur":v},"vars":{"route":">".join(map(str,route)),"arrived_by":frm},"note":f"Edge {i} reaches vertex {w}, already on the route, so the answer is true."})
            res[0]=True; return True
        if reach(w,i): return True
    route.pop(); return False
r=reach(0,-1)
# independent check: cycle iff edges > n - components
cl=[[i==j for j in range(n)] for i in range(n)]
for a,b in U: cl[a][b]=cl[b][a]=True
for k in range(n):
    for i in range(n):
        for j in range(n):
            if cl[i][k] and cl[k][j]: cl[i][j]=True
comps=len({tuple(row) for row in cl})
assert r is True and len(U)>n-comps and not seen[4]
fill(CH,F,block(list(range(n)),["cur"],steps),"@@TRACE2@@")
