from common import *
CH='26-dynamic-programming-foundations'
F='06-objective-types.md'
INF=10**9
def run(n,broken,jumps):
    reach=[0]*(n+1); ways=[0]*(n+1); fewest=[INF]*(n+1)
    reach[0]=1; ways[0]=1; fewest[0]=0
    cells=[f"c{c}" + (" x" if broken[c] else "") for c in range(n+1)]
    steps=[{"at":{"c":0},"vars":{"reach":1,"ways":1,"fewest":0},"note":"Cell 0 receives the base values: reachable, one way and zero jumps."}]
    for c in range(1,n+1):
        if broken[c]:
            note=f"Cell {c} is broken, so it keeps the sentinel values: not reachable, no ways and no jump count."
        else:
            preds=[c-j for j in jumps if c-j>=0]
            for p in preds:
                if reach[p]: reach[c]=1
                ways[c]+=ways[p]
                if fewest[p]!=INF: fewest[c]=min(fewest[c],fewest[p]+1)
            ps=", ".join(str(p) for p in preds)
            if reach[c]:
                note=f"Cell {c} is entered from cells {ps}. Adding their counts gives {ways[c]}, and the best predecessor gives {fewest[c]} jumps."
            else:
                note=f"Cell {c} is entered from cells {ps}, and none of them is reachable, so the entries stay at the sentinel values."
        steps.append({"at":{"c":c},"vars":{"reach":reach[c],"ways":ways[c],"fewest":-1 if fewest[c]==INF else fewest[c]},"note":note})
    return cells,steps,reach,ways,fewest
def brute(n,broken,jumps,pos=0):
    if pos==n: return (1,1,0)
    r=0;w=0;f=INF
    for j in jumps:
        q=pos+j
        if q>n or broken[q]: continue
        a,b,c=brute(n,broken,jumps,q)
        r|=a;w+=b
        if c!=INF: f=min(f,c+1)
    return (r,w,f)
b=[False]*10; b[4]=True
cells,steps,reach,ways,fewest=run(9,b,[1,3,4])
assert brute(9,b,[1,3,4])==(1,16,3) and (reach[9],ways[9],fewest[9])==(1,16,3) and ways[6]==5
fill(CH,F,block(cells,["c"],steps),"@@TRACE1@@")
b=[False]*7; b[3]=b[4]=True
cells,steps,reach,ways,fewest=run(6,b,[1,2])
assert brute(6,b,[1,2])==(0,0,INF) and (reach[6],ways[6],fewest[6])==(0,0,INF)
fill(CH,F,block(cells,["c"],steps),"@@TRACE2@@")
print("ok")
