from common import *
CH='02-matrices-and-2d-arrays'; F='05-matrix-rotation.md'
m=[[1,2,3],[4,5,6],[7,8,9]]; n=3
def S(m): return str(m).replace(' ','')
st=[]; st.append({"at":{"a":-1,"b":-1},"vars":{"matrix":S(m)},"note":"Start of the transpose pass. Only cells above the main diagonal are visited."})
for r in range(n):
    for c in range(r+1,n):
        m[r][c],m[c][r]=m[c][r],m[r][c]
        st.append({"at":{"a":r*n+c,"b":c*n+r},"vars":{"matrix":S(m)},"note":f"Swap row {r}, column {c} with row {c}, column {r}. The cells that lie on the main diagonal are never touched."})
assert m==[[1,4,7],[2,5,8],[3,6,9]]
fill(CH,F,block(list(range(9)),["a","b"],st),"@@TRACE1@@")
st=[{"at":{"a":-1,"b":-1},"vars":{"matrix":S(m)},"note":"Start of the reversal pass, on the transposed matrix."}]
for r in range(n):
    lo,hi=0,n-1
    while lo<hi:
        m[r][lo],m[r][hi]=m[r][hi],m[r][lo]
        st.append({"at":{"a":r*n+lo,"b":r*n+hi},"vars":{"matrix":S(m)},"note":f"Row {r} swaps its first and last cells. The middle cell of the row is its own mirror and stays."})
        lo+=1; hi-=1
assert m==[[7,4,1],[8,5,2],[9,6,3]]
fill(CH,F,block(list(range(9)),["a","b"],st),"@@TRACE2@@")
