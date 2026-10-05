from common import *
CH='07-prefix-sums-and-difference-arrays'
def run(m,n,ups,ph):
    D=[[0]*(n+1) for _ in range(m+1)]
    for r1,c1,r2,c2,v in ups:
        D[r1][c1]+=v; D[r1][c2+1]-=v; D[r2+1][c1]-=v; D[r2+1][c2+1]+=v
    W=n+1; flat=[x for row in D for x in row]
    A=[[0]*n for _ in range(m)]
    st=[{"at":{"i":-1},"vars":{},"note":"The corner deltas are written. The pass visits the cells of the grid in row order."}]
    for r in range(m):
        for c in range(n):
            up=A[r-1][c] if r else 0; lf=A[r][c-1] if c else 0; dg=A[r-1][c-1] if r and c else 0
            A[r][c]=D[r][c]+up+lf-dg
            st.append({"at":{"i":r*W+c},"vars":{"cell":f"({r},{c})","D":str(D[r][c]),"up":str(up),"left":str(lf),"diag":str(dg),"value":str(A[r][c])},"note":f"Value = {D[r][c]} + {up} + {lf} - {dg} = {A[r][c]} for the cell ({r},{c})."})
    fill(CH,'10-two-dimensional-difference.md',block(flat,["i"],st),ph); return A
assert run(3,3,[(0,0,1,1,1),(1,1,2,2,1)],"@@TRACE1@@")==[[1,1,0],[1,2,1],[0,1,1]]
assert run(2,2,[(0,0,1,1,3)],"@@TRACE2@@")==[[3,3],[3,3]]
