from common import *
CH='21-graph-traversal-models-dfs-and-ordinary-bfs'
F='04-components.md'
def run(n, edges):
    adj=[[] for _ in range(n)]
    for u,v in edges: adj[u].append(v); adj[v].append(u)
    seen=[False]*n; sizes=[]; steps=[]; marked=0
    for s in range(n):
        if seen[s]:
            steps.append((s,len(sizes),marked,0,False)); continue
        size=0; st=[s]; seen[s]=True
        while st:
            v=st.pop(); size+=1
            for w in adj[v]:
                if not seen[w]: seen[w]=True; st.append(w)
        marked+=size; sizes.append(size)
        steps.append((s,len(sizes),marked,size,True))
    return sizes,steps
# trace 1
sizes,raw=run(7,[(0,1),(1,2),(3,4)])
assert len(sizes)==4 and sum(sizes)==7
steps=[]
for s,c,m,size,new in raw:
    note=(f"Vertex {s} is unmarked, so a new search starts here, reaches {size} vertices, and the tally becomes {c}." if new
          else f"Vertex {s} is already marked by an earlier search, so the loop skips it and the tally stays {c}.")
    steps.append({"at":{"s":s},"vars":{"components":c,"seen":m},"note":note})
fill(CH,F,block([str(i) for i in range(7)],["s"],steps),"@@TRACE1@@")
# trace 2
sizes,raw=run(6,[(0,3),(3,5),(1,4)])
assert sizes==[3,2,1] and sum(sizes)==6
steps=[]
for s,c,m,size,new in raw:
    note=(f"Vertex {s} is unmarked, so its search marks {size} vertices and {size} is added to the sizes." if new
          else f"Vertex {s} is already marked, so no search runs and the size is 0.")
    steps.append({"at":{"s":s},"vars":{"size":size,"sizes":",".join(map(str,sizes[:c]))},"note":note})
fill(CH,F,block([str(i) for i in range(6)],["s"],steps),"@@TRACE2@@")
