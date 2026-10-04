from common import *
CH='02-matrices-and-2d-arrays'; F='07-spiral-boundaries.md'
def run(m, ph):
    R,C=len(m),len(m[0]); out=[]
    top,bottom,left,right=0,R-1,0,C-1
    def V(): return {"top":top,"bottom":bottom,"left":left,"right":right,"out":len(out)}
    st=[{"at":{"p":-1},"vars":V(),"note":"Start of the walk. The four edges enclose the whole matrix and nothing is emitted."}]
    cell=lambda r,c:r*C+c
    last=-1
    def emit(r,c,why):
        nonlocal last
        out.append(m[r][c]); last=cell(r,c)
        st.append({"at":{"p":last},"vars":V(),"note":why})
    while top<=bottom and left<=right:
        for c in range(left,right+1): emit(top,c,f"Top pass emits the value {m[top][c]} from row {top}, column {c}.")
        top+=1
        for r in range(top,bottom+1): emit(r,right,f"Right pass emits the value {m[r][right]} from row {r}, column {right}.")
        right-=1
        if top<=bottom:
            for c in range(right,left-1,-1): emit(bottom,c,f"Bottom pass emits the value {m[bottom][c]} from row {bottom}, column {c}.")
            bottom-=1
        else: st.append({"at":{"p":last},"vars":V(),"note":"The bottom edge is now above the top edge, so the guard skips the bottom pass."})
        if left<=right:
            for r in range(bottom,top-1,-1): emit(r,left,f"Left pass emits the value {m[r][left]} from row {r}, column {left}.")
            left+=1
        else: st.append({"at":{"p":last},"vars":V(),"note":"The right edge is now before the left edge, so the guard skips the left pass."})
    return out,st
m=[[1,2,3,4],[5,6,7,8],[9,10,11,12]]
o,st=run(m,1); assert o==[1,2,3,4,8,12,11,10,9,5,6,7]
fill(CH,F,block(list(range(12)),["p"],st),"@@TRACE1@@")
m=[[1],[2],[3]]
o,st=run(m,2); assert o==[1,2,3]
fill(CH,F,block(list(range(3)),["p"],st),"@@TRACE2@@")
