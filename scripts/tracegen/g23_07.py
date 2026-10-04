from common import *
CH='23-directed-graphs-and-union-find'
F='07-kruskal-foundations.md'
def leader(p,x):
    while p[x]!=x: x=p[x]
    return x
def kruskal(n,routes):
    order=sorted(routes,key=lambda r:r[2])  # stable
    p=list(range(n)); got=[]; seen=0
    for r in order:
        if len(got)==n-1: break
        seen+=1
        a,b=leader(p,r[0]),leader(p,r[1])
        if a==b: continue
        p[a]=b; got.append(r)
    return got,seen
# example checks for the exercises
g,_=kruskal(4,[[0,1,5],[1,2,3],[0,2,4],[2,3,6]]); assert g==[[1,2,3],[0,2,4],[2,3,6]]
g,_=kruskal(5,[[0,1,2],[2,3,2],[1,2,2],[3,4,1],[0,4,2],[1,3,9]]); assert g==[[3,4,1],[0,1,2],[2,3,2],[1,2,2]]
g,s=kruskal(4,[[0,1,1],[1,2,2],[2,3,3],[0,3,4],[0,2,5]]); assert (sum(r[2] for r in g),s)==(6,3)
g,s=kruskal(5,[[0,1,1],[1,2,2],[0,2,3],[3,4,4],[2,3,6],[1,4,8]]); assert (sum(r[2] for r in g),s)==(13,5)
g,s=kruskal(4,[[0,1,2],[1,2,3],[0,2,1]]); assert len(g)<3
g,s=kruskal(5,[[0,1,2*10**9],[1,2,2*10**9],[2,3,2*10**9],[3,4,2*10**9]]); assert sum(r[2] for r in g)==8*10**9
def mc(pts):
    n=len(pts); e=[[i,j,abs(pts[i][0]-pts[j][0])+abs(pts[i][1]-pts[j][1])] for i in range(n) for j in range(i+1,n)]
    g,_=kruskal(n,e); return sum(r[2] for r in g)
assert mc([[0,0],[1,1],[1,0],[-1,1]])==4, mc([[0,0],[1,1],[1,0],[-1,1]])
assert mc([[3,12],[-2,5],[-4,1]])==18, mc([[3,12],[-2,5],[-4,1]])
# trace 1
n=6
routes=[[0,1,4],[0,2,5],[1,2,3],[1,3,9],[2,3,6],[3,4,2],[4,5,7],[3,5,8],[2,4,10]]
order=sorted(routes,key=lambda r:r[2])
p=list(range(n)); taken=0; total=0; parts=n; steps=[]
for i,(a,b,w) in enumerate(order):
    ra,rb=leader(p,a),leader(p,b)
    if ra==rb:
        steps.append({"at":{"i":i},"vars":{"weight":w,"laid":0,"taken":taken,"total":total,"parts":parts},
          "note":f"Villages {a} and {b} already share a group, so the quote of {w} is skipped and nothing is paid."})
    else:
        p[ra]=rb; taken+=1; total+=w; parts-=1
        steps.append({"at":{"i":i},"vars":{"weight":w,"laid":1,"taken":taken,"total":total,"parts":parts},
          "note":f"Villages {a} and {b} lie in different groups, so the pipe of {w} is laid; {parts} group"+("s" if parts!=1 else "")+" remain."})
    if taken==n-1:
        steps[-1]["note"]+=" Five pipes are laid, so the sweep stops with the remaining quotes unread."; break
assert taken==5 and len(steps)==6 and steps[3]["vars"]["laid"]==0 and total==2+3+4+6+7==22
assert total==sum(r[2] for r in kruskal(n,routes)[0])
fill(CH,F,block([f"{a}-{b}:{w}" for a,b,w in order],["i"],steps),"@@TRACE1@@")
# trace 2
n=5
routes=[[0,1,1],[1,2,2],[0,2,3],[3,4,4],[2,3,6],[1,3,9]]
order=sorted(routes,key=lambda r:r[2])
def parts_of(es):
    q=list(range(n)); c=n
    for a,b,_ in es:
        x,y=leader(q,a),leader(q,b)
        if x!=y: q[x]=y; c-=1
    return c
pk=list(range(n)); taken=0; steps=[]
for i,(a,b,w) in enumerate(order):
    blind=order[:min(i+1,n-1)]
    ra,rb=leader(pk,a),leader(pk,b)
    if ra!=rb and taken<n-1: pk[ra]=rb; taken+=1; verdict=f"The sweep lays it."
    else: verdict="The sweep skips it." if taken<n-1 else "The sweep has stopped."
    bp=parts_of(blind); sp=n-taken
    steps.append({"at":{"i":i},"vars":{"blindPicked":len(blind),"blindParts":bp,"sweepTaken":taken,"sweepParts":sp},
      "note":f"Quote {a}-{b} of {w}: the blind rule has picked {len(blind)} and leaves {bp} group"+("s" if bp!=1 else "")+f". {verdict}"})
assert steps[2]["vars"]["sweepTaken"]==2 and steps[3]["vars"]["blindParts"]==2
assert steps[-1]["vars"]["sweepParts"]==1 and steps[-1]["vars"]["blindParts"]==2
fill(CH,F,block([f"{a}-{b}:{w}" for a,b,w in order],["i"],steps),"@@TRACE2@@")
print("ok")
