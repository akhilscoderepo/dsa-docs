from common import *
CH='02-matrices-and-2d-arrays'; F='03-direction-state.md'
DR=[0,1,0,-1]; DC=[1,0,-1,0]; NAME=["right","down","left","up"]
def run(R,C):
    g=[[0]*C for _ in range(R)]; r=c=d=0; st=[]
    for v in range(1,R*C+1):
        g[r][c]=v; note=f"Write {v} at row {r}, column {c}."
        nr,nc=r+DR[d],c+DC[d]
        if v==R*C:
            note+=" The sheet is full, so the loop stops."
            st.append({"at":{"cur":r*C+c},"vars":{"direction":NAME[d],"value":v,"filled":str(g).replace(' ','')},"note":note}); break
        if not(0<=nr<R and 0<=nc<C) or g[nr][nc]:
            why="outside the sheet" if not(0<=nr<R and 0<=nc<C) else "already filled"
            d=(d+1)%4; nr,nc=r+DR[d],c+DC[d]; note+=f" The next cell is {why}, so the cursor turns to {NAME[d]}."
        else: note+=f" The next cell is free, so the cursor keeps moving {NAME[d]}."
        st.append({"at":{"cur":r*C+c},"vars":{"direction":NAME[d],"value":v,"filled":str(g).replace(' ','')},"note":note})
        r,c=nr,nc
    return g,st
g,st=run(3,3); assert g==[[1,2,3],[8,9,4],[7,6,5]]
fill(CH,F,block(list(range(9)),["cur"],st),"@@TRACE1@@")
g,st=run(2,3); assert g==[[1,2,3],[6,5,4]]
fill(CH,F,block(list(range(6)),["cur"],st),"@@TRACE2@@")
