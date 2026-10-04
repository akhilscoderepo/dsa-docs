import os
from common import *
CH='23-directed-graphs-and-union-find'
F='06-dynamic-connectivity.md'
DRY=os.environ.get('DRY')
def put(trace,ph):
    if not DRY: fill(CH,F,trace,ph)

class UF:
    def __init__(s,n): s.p=list(range(n)); s.sz=[1]*n; s.comps=n; s.hops=0
    def find(s,x):
        while s.p[x]!=x:
            s.p[x]=s.p[s.p[x]]; x=s.p[x]; s.hops+=1
        return x
    def union(s,a,b):
        ra,rb=s.find(a),s.find(b)
        if ra==rb: return False,ra,rb
        if s.sz[ra]<s.sz[rb]: ra,rb=rb,ra
        s.p[rb]=ra; s.sz[ra]+=s.sz[rb]; s.comps-=1
        return True,ra,rb

# trace 1
n=8
ops=[('L',0,1),('L',2,3),('Q',1,2),('L',1,3),('Q',0,2),('L',3,0),('L',6,7),('Q',5,6),('L',5,6),('Q',5,7)]
u=UF(n); steps=[]; ref=[]
adj=[set() for _ in range(n)]
def reach(a,b):
    seen={a}; st=[a]
    while st:
        x=st.pop()
        for y in adj[x]:
            if y not in seen: seen.add(y); st.append(y)
    return b in seen
for i,(k,a,b) in enumerate(ops):
    ra,rb=u.find(a),u.find(b)
    if k=='L':
        merged,_,_=u.union(a,b); adj[a].add(b); adj[b].add(a)
        res=1 if merged else 0
        note=(f"Line {a}-{b} is laid. Their labels {ra} and {rb} differ, so the groups fuse and {u.comps} remain." if merged
              else f"Line {a}-{b} is laid, but both houses already carry label {ra}, so the group count stays {u.comps}.")
    else:
        res=1 if ra==rb else 0
        assert bool(res)==reach(a,b)
        note=(f"Houses {a} and {b} both carry label {ra}, so the operator answers yes." if res
              else f"Houses {a} and {b} carry labels {ra} and {rb}, so the operator answers no.")
    steps.append({"at":{"i":i},"vars":{"ra":ra,"rb":rb,"groups":u.comps,"result":res},"note":note})
print([ (s['vars'],s['note']) for s in steps])
assert u.comps==3 and u.find(0)==u.find(3) and u.find(5)==u.find(7) and u.find(4)==4
put(block([f"{k} {a}-{b}" for k,a,b in ops],["i"],steps),"@@TRACE1@@")

# trace 2: path laid in order, query far ends
n=9
ops=[]
for i in range(n-1): ops+= [('L',i,i+1),('Q',0,i+1)]
adj=[[] for _ in range(n)]; u=UF(n); dfs=0; steps=[]
def dfs_touch(a,b):
    seen={a}; st=[a]; t=0
    while st:
        x=st.pop(); t+=1
        if x==b: return True,t
        for y in adj[x]:
            if y not in seen: seen.add(y); st.append(y)
    return False,t
for i,(k,a,b) in enumerate(ops):
    if k=='L':
        adj[a].append(b); adj[b].append(a); u.union(a,b)
        note=f"Line {a}-{b} is laid. Union-find does its finds; the DFS side stores the line and does no work yet."
    else:
        ok,t=dfs_touch(a,b); dfs+=t
        r=u.find(a)==u.find(b); assert ok==r==True
        note=f"The query {a} to {b} is asked. A fresh DFS touches {t} houses, and the running DFS total is {dfs}."
    steps.append({"at":{"i":i},"vars":{"dfsWork":dfs,"ufWork":u.hops},"note":note})
print(dfs,u.hops)
put(block([f"{k} {a}-{b}" for k,a,b in ops],["i"],steps),"@@TRACE2@@")
