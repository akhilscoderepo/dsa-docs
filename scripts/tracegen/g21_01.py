from common import *
CH='21-graph-traversal-models-dfs-and-ordinary-bfs'
F='01-graph-representation.md'
# trace 1: undirected filing
edges=[(0,1),(1,2),(1,3)]
adj=[[] for _ in range(4)]; steps=[]; total=0
for i,(u,v) in enumerate(edges):
    adj[u].append(v); adj[v].append(u); total+=2
    steps.append({"at":{"e":i},"vars":{"total":total,"pile_u":",".join(map(str,adj[u])),"pile_v":",".join(map(str,adj[v]))},
      "note":f"The slip {u}-{v} is filed twice: vertex {v} joins the pile of {u} and vertex {u} joins the pile of {v}, so {total} entries are held in all."})
assert adj==[[1],[0,2,3],[1],[1]] and total==2*len(edges)
fill(CH,F,block(["0-1","1-2","1-3"],["e"],steps),"@@TRACE1@@")
# trace 2: directed matrix
edges=[(0,1),(2,1),(1,3)]
has=[[0]*4 for _ in range(4)]; steps=[]; ones=0
for i,(u,v) in enumerate(edges):
    has[u][v]=1; ones+=1
    steps.append({"at":{"e":i},"vars":{"ones":ones,"row_u":"".join(map(str,has[u]))},
      "note":f"The one-way slip {u}>{v} sets only the cell in row {u} and column {v}, so row {u} now reads {''.join(map(str,has[u]))} and {ones} cells are true."})
assert sum(map(sum,has))==3 and sum(has[3])==0
fill(CH,F,block(["0>1","2>1","1>3"],["e"],steps),"@@TRACE2@@")
