from common import *
CH='02-matrices-and-2d-arrays'; F='06-marker-state.md'
m=[[1,2,3,4],[5,0,7,8],[9,10,0,12]]; R,C=3,4
def S(m): return str(m).replace(' ','')
rm=[False]*R; cm=[False]*C
def mk(): return "rows "+"".join('1' if x else '0' for x in rm)+" cols "+"".join('1' if x else '0' for x in cm)
st=[{"at":{"p":-1},"vars":{"marks":mk()},"note":"Start of the observation pass. No marker is set and no cell has been read."}]
for r in range(R):
    for c in range(C):
        if m[r][c]==0:
            rm[r]=True; cm[c]=True
            st.append({"at":{"p":r*C+c},"vars":{"marks":mk()},"note":f"The cell in row {r}, column {c} holds zero. The pass sets the marker of row {r} and the marker of column {c} and changes no cell."})
assert rm==[False,True,True] and cm==[False,True,True,False]
fill(CH,F,block(list(range(12)),["p"],st),"@@TRACE1@@")
st=[{"at":{"a":-1,"b":-1},"vars":{"matrix":S(m)},"note":"Start of the update pass. The markers name rows 1 and 2 and columns 1 and 2."}]
for r in range(R):
    if rm[r]:
        for c in range(C): m[r][c]=0
        st.append({"at":{"a":r*C,"b":r*C+C-1},"vars":{"matrix":S(m)},"note":f"Row {r} is marked, so the pass writes zero into its first and last cell and every cell between them."})
for c in range(C):
    if cm[c]:
        for r in range(R): m[r][c]=0
        st.append({"at":{"a":c,"b":(R-1)*C+c},"vars":{"matrix":S(m)},"note":f"Column {c} is marked, so the pass writes zero from its top cell to its bottom cell. Cells already cleared by a row stay zero."})
assert m==[[1,0,0,4],[0,0,0,0],[0,0,0,0]]
fill(CH,F,block(list(range(12)),["a","b"],st),"@@TRACE2@@")
