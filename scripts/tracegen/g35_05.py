from common import *
CH='35-advanced-search-sampling-and-geometric-state'; N='05-rejection-sampling.md'
def circle(pairs,ph):
    st=[]; pts=[]
    for k,(u,v) in enumerate(pairs):
        x=round(2*u-1,10); y=round(2*v-1,10); r2=round(x*x+y*y,10); ok=r2<=1
        pts.append(f"({x}, {y})")
        n=f"Draws {u} and {v} give the point ({x}, {y}) with squared distance {r2}. "+("It is at most 1, so the point is accepted and returned." if ok else "It is above 1, so the point is rejected.")
        st.append({"at":{"trial":k},"vars":{"u":u,"v":v,"x":x,"y":y,"r2":r2,"verdict":"accept" if ok else "reject"},"note":n})
    assert ok and not any(round((2*u-1)**2+(2*v-1)**2,10)<=1 for u,v in pairs[:-1])
    fill(CH,N,block(pts,["trial"],st),ph)
def rand10(pairs,ph,final):
    st=[]; cells=[]
    for k,(a,b) in enumerate(pairs):
        idx=(a-1)*7+b; ok=idx<=40; cells.append(f"{a},{b}")
        n=f"Rolls {a} and {b} give index {idx}. "+(f"The index is at most 40, so it is accepted and the result is {1+(idx-1)%10}." if ok else "The index is above 40, so the pair is rejected.")
        st.append({"at":{"trial":k},"vars":{"a":a,"b":b,"index":idx,"verdict":"accept" if ok else "reject"},"note":n})
        if ok: assert 1+(idx-1)%10==final
    assert ok; fill(CH,N,block(cells,["trial"],st),ph)
circle([(0.1,0.9),(0.9,0.1),(0.6,0.3)],"@@TRACE1@@")
rand10([(6,6),(7,3),(2,5)],"@@TRACE2@@",2)
