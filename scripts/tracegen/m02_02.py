from common import *
CH='02-matrices-and-2d-arrays'; F='02-structured-traversal.md'
def run(g):
    R=len(g); C=len(g[0]); flat=[x for row in g for x in row]; st=[]; ok=True
    st.append({"at":{"cell":0,"pred":-1},"vars":{"r":0,"c":0,"verdict":"pending"},"note":"Cell 0 is in row 0, so it has no predecessor and is skipped. All of row 0 and column 0 are skipped the same way."})
    for r in range(1,R):
        for c in range(1,C):
            i=r*C+c; p=(r-1)*C+c-1; eq=g[r][c]==g[r-1][c-1]
            n=f"Row {r}, column {c} holds {g[r][c]}. Its predecessor holds {g[r-1][c-1]}, so "+("they match." if eq else "they differ and the check stops with false.")
            st.append({"at":{"cell":i,"pred":p},"vars":{"r":r,"c":c,"verdict":"pending" if eq else "false"},"note":n})
            if not eq: return flat,st,False
    st.append({"at":{"cell":R*C,"pred":-1},"vars":{"verdict":"true"},"note":"Every cell with a predecessor matched it, so the result is true."})
    return flat,st,True
g=[[3,5,1],[2,3,5],[9,2,3]]; f,st,v=run(g); assert v
fill(CH,F,block(f,["cell","pred"],st),"@@TRACE1@@")
g=[[1,2,4],[5,1,2],[9,5,7]]; f,st,v=run(g); assert not v
fill(CH,F,block(f,["cell","pred"],st),"@@TRACE2@@")
