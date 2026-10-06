from common import *
CH='21-graph-traversal-models-dfs-and-ordinary-bfs'; F='06-path-enumeration.md'
def run(n,edges,target,ph):
    adj=[[] for _ in range(n)]
    for u,v in edges: adj[u].append(v)
    st=[]; path=[]; found=[]
    def snap(cur,note): st.append({"at":{"cur":cur},"vars":{"path":"-".join(map(str,path)) or "empty","found":len(found)},"note":note})
    def go(cur,parent):
        path.append(cur)
        if cur==target:
            found.append(list(path))
            snap(cur,f"The call reaches target {cur}, so the search stores a copy of the working path and counts path number {len(found)}.")
        elif not adj[cur]:
            snap(cur,f"Vertex {cur} has no outgoing edge and is not the target, so the call stores nothing and returns.")
        else:
            snap(cur,f"The search enters vertex {cur} and appends it, so the working path now ends with {cur}.")
            for nx in adj[cur]: go(nx,cur)
        path.pop()
        snap(parent,"The call removes its vertex and control returns to vertex %d." % parent if parent>=0 else "The source call removes itself, so the working path is empty and the search ends.")
    go(0,-1)
    fill(CH,F,block(list(range(n)),["cur"],st),ph); return found
assert run(5,[[0,1],[0,2],[1,3],[2,3],[3,4]],4,"@@TRACE1@@")==[[0,1,3,4],[0,2,3,4]]
assert run(5,[[0,1],[0,2],[1,4],[2,3],[0,4]],4,"@@TRACE2@@")==[[0,1,4],[0,4]]
