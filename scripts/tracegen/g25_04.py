from common import *
CH='25-advanced-graph-optimization'
F='04-kruskal.md'
def kruskal(n,edges):
    s=sorted(edges,key=lambda e:e[2]); p=list(range(n)); sz=[1]*n
    def find(x):
        while p[x]!=x:
            p[x]=p[p[x]]; x=p[x]
        return x
    b=0; t=0
    for e in s:
        if b==n-1: break
        a,c=find(e[0]),find(e[1])
        if a==c: continue
        if sz[a]<sz[c]: a,c=c,a
        p[c]=a; sz[a]+=sz[c]; t+=e[2]; b+=1
    return t if b==n-1 else -1
# trace 1: equal roots skip, stop at n-1
n1=7; e1=[(0,1,4),(0,2,3),(1,2,2),(1,3,5),(2,3,5),(3,4,2),(4,5,3),(3,5,6),(5,6,1),(4,6,7),(2,6,9)]
s=sorted(e1,key=lambda e:e[2])
p=list(range(n1)); sz=[1]*n1
def find(x):
    while p[x]!=x:
        p[x]=p[p[x]]; x=p[x]
    return x
cells=[f"{u}-{v}@{w}" for u,v,w in s]
steps=[{"at":{"i":-1},"vars":{"bought":0,"total":0,"ru":-1,"rv":-1},"note":"Start: 7 groups of one vertex each. The loop needs 6 purchases."}]
b=0;t=0;skipped=0
for i,(u,v,w) in enumerate(s):
    ru,rv=find(u),find(v)
    if ru==rv:
        skipped+=1
        steps.append({"at":{"i":i},"vars":{"bought":b,"total":t,"ru":ru,"rv":rv},"note":f"Edge {u}-{v} has equal roots {ru} and {rv}, so it would close a cycle and the method skips it."})
        continue
    shown=(ru,rv)
    if sz[ru]<sz[rv]: ru,rv=rv,ru
    p[rv]=ru; sz[ru]+=sz[rv]; b+=1; t+=w
    note=f"Edge {u}-{v} joins the roots {shown[0]} and {shown[1]}, so the method buys it for {w}."
    if b==n1-1: note+=" That is purchase 6, so the loop stops and the last "+str(len(s)-i-1)+" edges are never examined."
    steps.append({"at":{"i":i},"vars":{"bought":b,"total":t,"ru":shown[0],"rv":shown[1]},"note":note})
    if b==n1-1: break
assert t==16 and b==6 and skipped==1 and t==kruskal(n1,e1)
assert len(s)-i-1==4
fill(CH,F,block(cells,["i"],steps),"@@TRACE1@@")
# trace 2: touched rule against the group rule
n2=6; e2=[(0,1,1),(2,3,1),(4,5,2),(1,2,3),(3,4,3),(0,5,6),(2,5,4),(1,4,5)]
s=sorted(e2,key=lambda e:e[2])
p=list(range(n2)); sz=[1]*n2
touched=[False]*n2; nv=0; nt=0; kb=0; kt=0
cells=[f"{u}-{v}@{w}" for u,v,w in s]
steps=[{"at":{"i":-1},"vars":{"naive":0,"kruskal":0,"gap":0},"note":"Start: nothing is bought by either rule."}]
for i,(u,v,w) in enumerate(s):
    nbuy = not (touched[u] and touched[v])
    if nbuy: touched[u]=touched[v]=True; nv+=1; nt+=w
    kbuy=False
    if kb<n2-1:
        ru,rv=find(u),find(v)
        if ru!=rv:
            kbuy=True
            if sz[ru]<sz[rv]: ru,rv=rv,ru
            p[rv]=ru; sz[ru]+=sz[rv]; kb+=1; kt+=w
        state="the group rule "+("buys it" if kbuy else "skips it")
    else:
        state="the group rule has already stopped"
    nstate="the touched rule "+("buys" if nbuy else "skips")+" the edge"
    steps.append({"at":{"i":i},"vars":{"naive":nv,"kruskal":kb,"gap":kb-nv},"note":f"Edge {u}-{v}: {nstate}, and {state}."})
assert (nv,nt,kb,kt)==(3,4,5,10), (nv,nt,kb,kt)
assert kt==kruskal(n2,e2)
fill(CH,F,block(cells,["i"],steps),"@@TRACE2@@")
print("ok")
