from common import *
CH='23-directed-graphs-and-union-find'
F='02-dfs-topological-state.md'
def adj(n,edges):
    a=[[] for _ in range(n)]
    for u,v in edges: a[u].append(v)
    for r in a: r.sort()
    return a
def walk(n,edges):
    a=adj(n,edges); col=[0]*n; steps=[]; post=[]; st={'loop':False}
    def snap(room,note):
        steps.append({"at":{"room":room},"vars":{"open":col.count(1),"listed":len(post)},"note":note})
    def visit(u):
        col[u]=1; snap(u,f"Room {u} turns gray: the walk enters it.")
        for v in a[u]:
            if col[v]==1:
                st['loop']=True
                snap(u,f"The door from {u} to {v} leads to gray room {v}, so the gray corridor plus this door is a circle; no order exists.")
                return
            if col[v]==2:
                snap(u,f"The door from {u} to {v} leads to black room {v}, already finished by another branch; it is accepted and ignored.")
            else:
                visit(v)
                if st['loop']: return
        col[u]=2; post.append(u)
        snap(u,f"Room {u} turns black and is listed in slot {n-len(post)}.")
    for r in range(n):
        if col[r]==0 and not st['loop']: visit(r)
    return steps,post,st['loop']
s1,p1,l1=walk(6,[[0,1],[0,2],[1,3],[2,3],[2,4],[3,5],[4,3]])
assert not l1 and p1==[5,3,1,4,2,0], p1
order=p1[::-1]; pos={v:i for i,v in enumerate(order)}
for u,v in [[0,1],[0,2],[1,3],[2,3],[2,4],[3,5],[4,3]]: assert pos[u]<pos[v]
s1[-1]['note']+=f" The tour is {order}."
fill(CH,F,block(list(range(6)),["room"],s1),"@@TRACE1@@")
s2,p2,l2=walk(5,[[0,1],[1,2],[2,3],[3,1],[0,4]])
assert l2 and p2==[] and len(s2)==5, (l2,p2,len(s2))
s2[-1]['note']+=" The answer is the empty list."
fill(CH,F,block(list(range(5)),["room"],s2),"@@TRACE2@@")
print(order,len(s1),len(s2))
