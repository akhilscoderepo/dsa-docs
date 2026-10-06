from common import *
CH='21-graph-traversal-models-dfs-and-ordinary-bfs'; F='02-graph-cloning.md'
def run(adj,ph,notes_enter,notes_reuse):
    n=len(adj); clones=[]; st=[]
    def snap(): return ",".join(map(str,clones)) or "-"
    def dfs(u):
        clones.append(u)
        st.append({"at":{"cur":u,"next":-1},"vars":{"clones":snap(),"count":len(clones)},"note":notes_enter(u)})
        for v in adj[u]:
            if v in clones:
                st.append({"at":{"cur":u,"next":v},"vars":{"clones":snap(),"count":len(clones)},"note":notes_reuse(u,v)})
            else: dfs(v)
    dfs(0); fill(CH,F,block(list(range(n)),["cur","next"],st),ph); return clones
en1={0:"Node 0 enters the map with a new clone, and the walk follows its only reference.",1:"Node 1 gets its clone, and its reference leads to node 2.",2:"Node 2 gets its clone and lists nodes 0 and 3.",3:"Node 3 is new, so it gets the fourth clone and has no references to follow."}
r1=lambda u,v:f"Node {v} already has a clone, so node {u} points its clone at it and the walk goes no deeper."
c=run([[1],[2],[0,3],[]],"@@TRACE1@@",lambda u:en1[u],r1)
assert sorted(c)==[0,1,2,3] and len(c)==4
en2={0:"Node 0 enters the map first and lists nodes 1 and 2.",1:"Node 1 gets a clone and lists node 3.",3:"Node 3 is discovered through node 1 and stored with its clone.",2:"Node 2 gets a clone after the branch through node 1 is finished."}
r2=lambda u,v:f"Node 2 lists node {v}, which the map already holds, so the existing clone is reused and no fifth clone appears."
c=run([[1,2],[3],[3],[]],"@@TRACE2@@",lambda u:en2[u],r2)
assert len(c)==4 and c==[0,1,3,2]
