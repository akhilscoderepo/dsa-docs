from common import *
CH='35-advanced-search-sampling-and-geometric-state'; N='91-randomized-sampling-state.md'
def wres(recs,draws,ph,final):
    held=None; total=0; di=iter(draws); st=[]
    cells=[f"{n}:{w}" for n,w,_ in recs]
    for t,(n,w,ok) in enumerate(recs):
        if not ok:
            st.append({"at":{"t":t},"vars":{"total":total,"held":held,"draw":"none"},"note":f"Record {n} does not qualify, so total and the held item stay as they are."}); continue
        total+=w
        if held is None: held=n; st.append({"at":{"t":t},"vars":{"total":total,"held":held,"draw":"none"},"note":f"Record {n} is the first eligible record. It becomes the held item without a draw, and total is {total}."}); continue
        d=next(di)
        if d<w: held=n; note=f"Total becomes {total}. The draw from bound {total} is {d}, which is below the weight {w}, so {n} replaces the held item."
        else: note=f"Total becomes {total}. The draw from bound {total} is {d}, which is not below the weight {w}, so the held item stays."
        st.append({"at":{"t":t},"vars":{"total":total,"held":held,"draw":d},"note":note})
    assert held==final; fill(CH,N,block(cells,["t"],st),ph)
def ring(inner,outer,pairs,ph):
    ratio=(inner/outer)**2; st=[]; cells=[]
    for k,(u,v) in enumerate(pairs):
        x=round(2*u-1,10); y=round(2*v-1,10); r2=round(x*x+y*y,10)
        ok=ratio<=r2<=1; cells.append(f"({x}, {y})")
        why="It is accepted and returned after scaling by 2." if ok else ("It lies inside the hole, below 0.25, so it is rejected." if r2<ratio else "It lies outside the outer circle, above 1, so it is rejected.")
        st.append({"at":{"trial":k},"vars":{"x":x,"y":y,"r2":r2,"verdict":"accept" if ok else "reject"},"note":f"Draws {u} and {v} give the unit point ({x}, {y}) with squared distance {r2}. {why}"})
    assert ok; fill(CH,N,block(cells,["trial"],st),ph)
wres([("A",3,True),("B",2,False),("C",1,True),("D",4,True),("E",2,True)],[3,2,7],"@@TRACE1@@","D")
ring(1,2,[(0.55,0.45),(0.05,0.95),(0.9,0.5)],"@@TRACE2@@")
