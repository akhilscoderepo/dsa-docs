from common import *
CH='02-matrices-and-2d-arrays'; F='04-neighbor-enumeration.md'
D4=[(-1,0),(1,0),(0,-1),(0,1)]
D8=[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
def run(R,C,r,c,dirs):
    cnt=0; st=[]
    for dr,dc in dirs:
        nr,nc=r+dr,c+dc; ok=0<=nr<R and 0<=nc<C
        if ok: cnt+=1
        st.append({"at":{"center":r*C+c,"cand":nr*C+nc if ok else -1},"vars":{"offset":f"({dr},{dc})","candidate":f"({nr},{nc})","count":cnt},
          "note":f"Offset ({dr},{dc}) reaches row {nr}, column {nc}. "+("It lies inside the board, so the count becomes "+str(cnt)+"." if ok else f"It lies outside the board, so the count stays {cnt}.")})
    return st,cnt
st,n=run(3,3,0,0,D8); assert n==3
fill(CH,F,block(list(range(9)),["center","cand"],st),"@@TRACE1@@")
st,n=run(3,3,1,0,D4); assert n==3
fill(CH,F,block(list(range(9)),["center","cand"],st),"@@TRACE2@@")
