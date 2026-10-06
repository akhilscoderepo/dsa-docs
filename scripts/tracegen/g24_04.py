from common import *
CH='24-shortest-paths-and-graph-state-modeling'
F='04-constrained-flights.md'
INF=10**9
def s(x): return "none" if x>=INF else x
fl=[[0,1,10],[1,2,10],[2,3,10],[0,2,50]]
cells=[f"{a}>{b} for {w}" for a,b,w in fl]
def passes(k, snapshot):
    best=[INF]*4; best[0]=0; steps=[]
    for p in range(k+1):
        nxt=best[:]
        for i,(a,b,w) in enumerate(fl):
            src_cost=best[a] if snapshot else nxt[a]
            offer=src_cost+w if src_cost<INF else INF
            take=offer<nxt[b]
            if take: nxt[b]=offer
            if src_cost>=INF:
                note=f"The flight from {a} to {b} finds no price at city {a}, so it offers nothing."
            elif take:
                note=f"The flight from {a} to {b} reads {src_cost} at city {a} and offers {offer}, which lowers city {b} to {offer}."
            else:
                note=f"The flight from {a} to {b} reads {src_cost} at city {a} and offers {offer}, but city {b} already holds {nxt[b]}."
            steps.append({"at":{"f":i},"vars":{"pass":p+1,"frozen" if snapshot else "read":s(src_cost),"offer":s(offer),"stored":s(nxt[b])},"note":note})
        best=nxt
    return best,steps
b1,st1=passes(1,True)
assert b1==[0,10,20,60] and len(st1)==8
assert st1[1]["vars"]["frozen"]=="none" and st1[6]["vars"]["stored"]==60
b2,st2=passes(0,False)
assert b2[3]==30 and len(st2)==4 and st2[2]["vars"]["stored"]==30
fill(CH,F,block(cells,["f"],st1),"@@TRACE1@@")
fill(CH,F,block(cells,["f"],st2),"@@TRACE2@@")
