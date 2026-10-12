from common import *
CH='25-advanced-graph-optimization'
F='05-hierholzer-trails.md'
def run(n,links,start):
    adj=[[] for _ in range(n)]
    for a,b in links: adj[a].append(b)
    cur=[0]*n; stack=[start]; out=[]; used=0; m=len(links)
    cells=[]; steps=[]
    while stack:
        v=stack[-1]
        if cur[v]<len(adj[v]):
            w=adj[v][cur[v]]; cur[v]+=1; used+=1; stack.append(w)
            cells.append(f"take {w}")
            note=f"The method consumes the link {v} to {w} and pushes vertex {w}."
        else:
            out.append(v); stack.pop()
            cells.append(f"emit {v}")
            note=f"Vertex {v} has no unused link, so the method pops it and appends it to the output."+(f" Vertex {stack[-1]} is on top now." if stack else " The stack is empty.")
        steps.append({"at":{"ev":len(cells)-1},"vars":{"stack":len(stack),"unused":m-used,"emitted":len(out)},"note":note})
    assert len(out)==m+1
    return cells,steps,out[::-1],out
# trace 1
c,s,res,out=run(4,[(0,1),(1,2),(2,0),(1,3),(3,1)],0)
assert out==[0,2,1,3,1,0] and res==[0,1,3,1,2,0], (out,res)
assert len(c)==11
s[3]['note']+=" The first loop has ended at the start, and one vertex below still owns links."
s[4]['note']+=" Vertex 1 still owns the link 1 to 3."
fill(CH,F,block(c,["ev"],s),"@@TRACE1@@")
print(c,res)
# trace 2
c,s,res,out=run(4,[(0,1),(0,2),(2,3),(3,0)],0)
assert out==[1,0,3,2,0] and res==[0,2,3,0,1], (out,res)
s[1]['note']+=" The walk would print only 0, 1 here, and this vertex lands last after the reversal."
fill(CH,F,block(c,["ev"],s),"@@TRACE2@@")
print(c,res)
