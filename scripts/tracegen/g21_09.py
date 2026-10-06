from common import *
CH='21-graph-traversal-models-dfs-and-ordinary-bfs'; F='09-cycle-detection.md'
def und(n,edges,ph):
    adj=[[] for _ in range(n)]
    for a,b in edges: adj[a].append(b); adj[b].append(a)
    vis=[False]*n; st=[]; found=[False]
    def vs(): return "".join('1' if x else '0' for x in vis)
    def walk(u,par):
        vis[u]=True
        st.append({"at":{"cur":u},"vars":{"parent":par,"visited":vs()},"note":f"The search enters vertex {u} and marks it as visited."})
        for v in adj[u]:
            if v==par:
                st.append({"at":{"cur":u},"vars":{"parent":par,"visited":vs()},"note":f"Neighbor {v} is the parent of vertex {u}, so the search skips the edge it just used."}); continue
            if vis[v]:
                st.append({"at":{"cur":u},"vars":{"parent":par,"visited":vs()},"note":f"Neighbor {v} is marked and is not the parent, so the edge {u}-{v} closes a cycle."}); found[0]=True; return True
            if walk(v,u): return True
        return False
    for s in range(n):
        if not vis[s] and walk(s,-1): break
    fill(CH,F,block(list(range(n)),["cur"],st),ph); return found[0]
def dire(n,edges,ph):
    adj=[[] for _ in range(n)]
    for a,b in edges: adj[a].append(b)
    state=[0]*n; st=[]; found=[False]
    def ss(): return "".join(map(str,state))
    def walk(u):
        state[u]=1
        st.append({"at":{"cur":u},"vars":{"state":ss()},"note":f"Vertex {u} becomes visiting because its call is now open."})
        for v in adj[u]:
            if state[v]==1:
                st.append({"at":{"cur":u},"vars":{"state":ss()},"note":f"The edge from {u} reaches vertex {v}, which is visiting, so the route returns to itself and a cycle exists."}); found[0]=True; return True
            if state[v]==2:
                st.append({"at":{"cur":u},"vars":{"state":ss()},"note":f"The edge from {u} reaches vertex {v}, which is finished, so the search ignores it."}); continue
            if walk(v): return True
        state[u]=2
        st.append({"at":{"cur":u},"vars":{"state":ss()},"note":f"Every neighbor of vertex {u} is processed, so the vertex becomes finished."})
        return False
    for s in range(n):
        if state[s]==0 and walk(s): break
    fill(CH,F,block(list(range(n)),["cur"],st),ph); return found[0]
assert und(5,[(0,1),(1,2),(2,3),(3,1),(3,4)],"@@TRACE1@@")==True
assert dire(5,[(0,1),(1,2),(0,2),(0,3),(3,4),(4,3)],"@@TRACE2@@")==True
