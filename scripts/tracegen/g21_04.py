from common import *
CH='21-graph-traversal-models-dfs-and-ordinary-bfs'; F='04-components.md'
def fmt(xs): return "["+",".join(map(str,xs))+"]"
def run(n,edges,ph,notes):
    adj=[[] for _ in range(n)]
    for a,b in edges: adj[a].append(b); adj[b].append(a)
    vis=[False]*n; count=0; st=[]
    def dfs(v):
        vis[v]=True; s=1
        for w in adj[v]:
            if not vis[w]: s+=dfs(w)
        return s
    sizes=[]
    for s0 in range(n):
        if vis[s0]:
            size=0; note=notes['skip'](s0)
        else:
            count+=1; size=dfs(s0); sizes.append(size); note=notes['new'](s0,count,size)
        st.append({"at":{"start":s0},"vars":{"count":count,"size":size if size else "-","marked":fmt([i for i in range(n) if vis[i]])},"note":note})
    fill(CH,F,block(list(range(n)),["start"],st),ph); return count,sizes
import itertools
T1={'skip':lambda s:[f"Vertex {s} is already marked, so the loop moves on without a search.",f"The loop reaches vertex {s}, finds it marked and skips it.",f"Vertex {s} belongs to an earlier component, so no new search starts."][s%3],
    'new':lambda s,c,z:[f"Vertex {s} is unmarked, so the loop starts a search and counts component {c}. The search marks {z} vertices.",f"The loop finds vertex {s} unmarked and opens component {c}, and the search reaches {z} vertices.",f"Vertex {s} has no mark, so component {c} begins here and the search marks {z} vertices."][c%3]}
assert run(6,[[0,1],[1,2],[3,4]],"@@TRACE1@@",T1)==(3,[3,2,1])
T2={'skip':lambda s:f"Vertex {s} already carries a mark from an earlier search, so the loop does not start another.",
    'new':lambda s,c,z:f"The loop reaches unmarked vertex {s}, so it counts component {c}, and the search marks {z} vertices."}
assert run(7,[[0,6],[2,6],[1,4],[4,5],[5,1]],"@@TRACE2@@",T2)==(3,[3,3,1])
