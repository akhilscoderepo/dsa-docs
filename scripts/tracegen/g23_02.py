import sys
from common import *
CH='23-directed-graphs-and-union-find'
def run(n,edges,ph):
    adj=[[] for _ in range(n)]
    for a,b in edges: adj[a].append(b)
    color=[0]*n; post=[]; st=[]; found=[None]
    sys.setrecursionlimit(10000)
    C=lambda: "".join("WGB"[c] for c in color)
    P=lambda: "-".join(map(str,post)) if post else "empty"
    def snap(cur,note): st.append({"at":{"cur":cur},"vars":{"colors":C(),"post":P()},"note":note})
    def visit(u):
        color[u]=1; snap(u,f"The search enters vertex {u} and turns it gray.")
        for v in adj[u]:
            if color[v]==1:
                snap(u,f"The edge from {u} to {v} reaches a gray vertex, so it closes a cycle and the method reports the pair {u} and {v}."); found[0]=(u,v); return True
            if color[v]==2:
                snap(u,f"The edge from {u} to {v} reaches a black vertex, so the search skips it."); continue
            if visit(v): return True
        color[u]=2; post.append(u); snap(u,f"All edges of vertex {u} are scanned, so it turns black and joins the postorder.")
        return False
    cyc=False
    for v in range(n):
        if color[v]==0 and visit(v): cyc=True; break
    fill(CH,'02-dfs-topological-state.md',block(list(range(n)),["cur"],st),ph)
    return cyc,list(reversed(post)),found[0]
c,o,f=run(5,[(0,1),(0,2),(1,3),(2,3),(4,2)],"@@TRACE1@@"); assert not c and o==[4,0,2,1,3]
c,o,f=run(4,[(0,1),(1,2),(2,3),(3,1)],"@@TRACE2@@"); assert c and f==(3,1)
