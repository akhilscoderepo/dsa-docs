from common import *
CH='15-trees-dfs'
F='09-quadtree-construction.md'
def run(g,ph):
    n=len(g); st=[]
    def uni(t,l,s): return len({g[r][c] for r in range(t,t+s) for c in range(l,l+s)})==1
    def build(t,l,s):
        if uni(t,l,s):
            st.append({"at":{"cell":t*n+l},"vars":{"side":s},"note":f"The block of side {s} at row {t}, column {l} holds only {g[t][l]}, so it is written as one leaf."})
            return str(g[t][l])
        st.append({"at":{"cell":t*n+l},"vars":{"side":s},"note":f"The block of side {s} at row {t}, column {l} holds both values, so it is cut into four blocks of side {s//2}."})
        h=s//2
        return "("+build(t,l,h)+build(t,l+h,h)+build(t+h,l,h)+build(t+h,l+h,h)+")"
    out=build(0,0,n)
    fill(CH,F,block([str(v) for row in g for v in row],["cell"],st),ph)
    return out
assert run([[1,1,0,0],[1,1,0,0],[1,0,1,1],[1,0,1,1]],"@@TRACE1@@")=="(10(1010)1)"
assert run([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1]],"@@TRACE2@@")=="(000(0001))"
