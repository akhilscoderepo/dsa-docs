from common import *
CH='07-prefix-sums-and-difference-arrays'
g=[[1,2,3],[4,5,6],[7,8,9]]
m=len(g); n=len(g[0])
P=[[0]*(n+1) for _ in range(m+1)]
for r in range(m):
    for c in range(n): P[r+1][c+1]=P[r][c+1]+P[r+1][c]-P[r][c]+g[r][c]
flat=[x for row in P for x in row]
W=n+1
def q(r1,c1,r2,c2,ph):
    a=P[r2+1][c2+1]; b=P[r1][c2+1]; c=P[r2+1][c1]; d=P[r1][c1]
    ia,ib,ic,idd=(r2+1)*W+c2+1,r1*W+c2+1,(r2+1)*W+c1,r1*W+c1
    st=[{"at":{"whole":-1,"above":-1,"left":-1,"corner":-1},"vars":{"query":f"({r1},{c1}) to ({r2},{c2})"},"note":f"The prefix matrix is ready. The query reads four entries, and the pointers will mark them in turn."},
        {"at":{"whole":ia,"above":-1,"left":-1,"corner":-1},"vars":{"total":str(a)},"note":f"Start with whole = P[{r2+1}][{c2+1}] = {a}, the sum from the top-left cell to the bottom-right corner."},
        {"at":{"whole":ia,"above":ib,"left":-1,"corner":-1},"vars":{"total":f"{a} - {b} = {a-b}"},"note":f"Subtract above = P[{r1}][{c2+1}] = {b}, the rows over the rectangle."},
        {"at":{"whole":ia,"above":ib,"left":ic,"corner":-1},"vars":{"total":f"{a-b} - {c} = {a-b-c}"},"note":f"Subtract left = P[{r2+1}][{c1}] = {c}, the columns to its left."},
        {"at":{"whole":ia,"above":ib,"left":ic,"corner":idd},"vars":{"total":f"{a-b-c} + {d} = {a-b-c+d}"},"note":f"Add back the corner P[{r1}][{c1}] = {d}, which both subtractions removed."}]
    fill(CH,'09-two-dimensional-prefix.md',block(flat,["whole","above","left","corner"],st),ph); return a-b-c+d
assert q(1,1,2,2,"@@TRACE1@@")==28
assert q(1,1,1,1,"@@TRACE2@@")==5
