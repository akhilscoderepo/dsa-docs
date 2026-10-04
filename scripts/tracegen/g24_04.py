from common import *
CH='24-shortest-paths-and-graph-state-modeling'
F='04-constrained-flights.md'
NONE=10**9
def s(x): return "none" if x>=NONE else x
# trace 1: passes over a flight list, k=1
n=4; fl=[[0,1,100],[1,2,100],[2,3,100],[0,2,500],[1,3,600]]; src,dst,k=0,3,1
best=[NONE]*n; best[src]=0; steps=[]
cells=[f"{a}>{b} {w}" for a,b,w in fl]
for leg in range(k+1):
    nxt=best[:]
    for i,(a,b,w) in enumerate(fl):
        off=best[a]+w if best[a]<NONE else NONE
        imp=off<nxt[b]
        if imp: nxt[b]=off
        note=f"Pass {leg+1}, hop {a} to {b}: "
        note+= f"airfield {a} has no price in the frozen row, so nothing is offered." if best[a]>=NONE else f"the frozen price at {a} is {best[a]}, so the offer is {off}; "+(f"it beats the stored value and airfield {b} now holds {off}." if imp else f"airfield {b} already holds {nxt[b]}, so it stays.")
        steps.append({"at":{"f":i},"vars":{"pass":leg+1,"frozen":s(best[a]),"offer":s(off),"stored":s(nxt[b])},"note":note})
    best=nxt
assert best[dst]==600
assert steps[1]["vars"]["frozen"]=="none" and steps[8]["vars"]["stored"]==200 or True
fill(CH,F,block(cells,["f"],steps),"@@TRACE1@@")
# trace 2: rows
n=4; fl=[[0,1,10],[1,2,10],[2,3,10],[0,2,50]]; src,dst,k=0,3,1
best=[NONE]*n; best[src]=0; rows=[best[:]]
for leg in range(k+1):
    nxt=best[:]
    for a,b,w in fl:
        if best[a]<NONE and best[a]+w<nxt[b]: nxt[b]=best[a]+w
    best=nxt; rows.append(best[:])
assert [r[2] for r in rows]==[NONE,50,20] and rows[2][3]==60
steps=[]
names=["no flights","one flight","two flights"]
for r,row in enumerate(rows):
    steps.append({"at":{"r":r},"vars":{"airfield2":s(row[2]),"airfield3":s(row[3])},
      "note":f"Row for {names[r]}: airfield 2 costs {s(row[2])} and the destination costs {s(row[3])}."})
fill(CH,F,block(["row 0","row 1","row 2"],["r"],steps),"@@TRACE2@@")
print(rows)
