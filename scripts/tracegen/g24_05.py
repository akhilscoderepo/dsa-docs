from common import *
from collections import deque
CH='24-shortest-paths-and-graph-state-modeling'
F='05-alternating-colors.md'
nm=lambda c:'red' if c==0 else 'blue'
lab=lambda v,c:f"{v}{'r' if c==0 else 'b'}"
# trace 1: pair contract, states in dequeue order
n=6
red=[[0,1],[1,2],[3,4],[2,3]]; blue=[[0,1],[2,0],[4,5],[3,3]]
edges=[[a,b,0] for a,b in red]+[[a,b,1] for a,b in blue]
dist={}; q=deque()
for a,b,c in edges:
    if a==0 and (b,c) not in dist: dist[(b,c)]=1; q.append((b,c))
first_layer=list(q)
order=[]; info=[]
while q:
    v,c=q.popleft(); order.append((v,c)); added=[]
    for a,b,col in edges:
        if a==v and col!=c and (b,col) not in dist:
            dist[(b,col)]=dist[(v,c)]+1; q.append((b,col)); added.append((b,col))
    info.append(((v,c),dist[(v,c)],len(q),added))
res=[[dist.get((v,0),-1),dist.get((v,1),-1)] for v in range(n)]
assert res==[[-1,3],[1,1],[2,-1],[-1,-1],[-1,-1],[-1,-1]],res
steps=[]
for i,((v,c),d,w,added) in enumerate(info):
    if added: note=f"State {lab(v,c)} is expanded at {d} section"+("s" if d!=1 else "")+f"; only {nm(1-c)} sections may leave it, and they add "+", ".join(lab(*s) for s in added)+"."
    else: note=f"State {lab(v,c)} is expanded at {d} section"+("s" if d!=1 else "")+f"; no {nm(1-c)} section leaves node {v} to an unreached state."
    steps.append({"at":{"cur":i},"vars":{"dist":d,"waiting":w,"added":len(added)},"note":note})
assert [lab(*s) for s in first_layer]==['1r','1b']
fill(CH,F,block([lab(*s) for s,_,_,_ in info],["cur"],steps),"@@TRACE1@@")
# trace 2: both start colors seeded, cells are nodes
n2=3
e2=[[0,0,0],[0,1,0],[0,1,1],[1,1,1],[1,2,0],[2,0,1]]
d2={(0,0):0,(0,1):0}; q=deque([(0,0),(0,1)]); steps=[]; cells=[0,1,2]
while q:
    v,c=q.popleft(); added=[]
    for a,b,col in e2:
        if a==v and col!=c and (b,col) not in d2:
            d2[(b,col)]=d2[(v,c)]+1; q.append((b,col)); added.append((b,col))
    note=f"State {lab(v,c)} is expanded at {d2[(v,c)]} section"+("s" if d2[(v,c)]!=1 else "")+"; "+("it adds "+", ".join(lab(*s) for s in added)+"." if added else "nothing new can be reached from it.")
    steps.append({"at":{"node":v},"vars":{"state":lab(v,c),"dist":d2[(v,c)],"waiting":len(q)},"note":note})
best=[min(d2[(v,c)] for c in(0,1) if (v,c) in d2) for v in range(n2)]
assert best==[0,1,2],best
fill(CH,F,block(cells,["node"],steps),"@@TRACE2@@")
print(order,res,[ (lab(*k),v) for k,v in d2.items()])
