from common import *
CH='21-graph-traversal-models-dfs-and-ordinary-bfs'; F='01-graph-representation.md'
def show(adj): return " ".join(f"{v}:{adj[v]}".replace(" ","") for v in range(len(adj)))
def run(n,edges,directed,ph,notes):
    adj=[[] for _ in range(n)]; st=[]
    for k,(a,b) in enumerate(edges):
        adj[a].append(b)
        if not directed: adj[b].append(a)
        st.append({"at":{"from":a,"to":b},"vars":{"edge":f"[{a},{b}]","adj":show(adj)},"note":notes[k]})
    fill(CH,F,block(list(range(n)),["from","to"],st),ph); return adj
a=run(5,[[0,1],[0,2],[1,3],[3,4]],False,"@@TRACE1@@",[
 "The edge [0,1] adds 1 to the list of vertex 0 and 0 to the list of vertex 1.",
 "The edge [0,2] gives vertex 0 a second neighbor and gives vertex 2 its first.",
 "The edge [1,3] extends the list of vertex 1 and starts the list of vertex 3.",
 "The edge [3,4] makes vertex 3 hold 1 and 4, which answers the opening question."])
assert a==[[1,2],[0,3],[0],[1,4],[3]] and sum(map(len,a))==8
d=run(5,[[2,3],[0,1],[2,1],[3,2]],True,"@@TRACE2@@",[
 "The directed edge [2,3] writes 3 into the list of vertex 2 only.",
 "The directed edge [0,1] writes 1 into the list of vertex 0 and leaves vertex 1 untouched.",
 "The edge [2,1] appends 1 after 3 in the list of vertex 2.",
 "The edge [3,2] gives vertex 3 a neighbor; vertex 4 still has an empty list because no edge mentions it."])
assert d==[[1],[],[3,1],[2],[]]
