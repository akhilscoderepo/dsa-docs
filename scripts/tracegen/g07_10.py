from common import *
CH='07-prefix-sums-and-difference-arrays'
F='10-two-dimensional-difference.md'
R=C=4; v=5; r1,c1,r2,c2=1,1,2,2; W=C+1
diff=[[0]*W for _ in range(R+1)]
writes=[(r1,c1,v,"start corner"),(r1,c2+1,-v,"end along the columns"),(r2+1,c1,-v,"end along the rows"),(r2+1,c2+1,v,"overlap repair")]
st=[]
for r,c,d,name in writes:
    diff[r][c]+=d
    st.append({"at":{"w":r*W+c},"vars":{"row":r,"col":c,"delta":d},"note":f"Write {d:+d} at row {r}, column {c}, the {name}."})
assert writes[3][0]==3 and writes[3][1]==3
flat=[str(x) for row in diff for x in row]
fill(CH,F,block(flat,["w"],st),"@@TRACE1@@")
out=[[0]*C for _ in range(R)]; st=[]
for r in range(R):
    for c in range(C):
        a=out[r-1][c] if r>0 else 0; l=out[r][c-1] if c>0 else 0; d=out[r-1][c-1] if r>0 and c>0 else 0
        out[r][c]=diff[r][c]+a+l-d
        st.append({"at":{"w":r*W+c},"vars":{"delta":diff[r][c],"above":a,"left":l,"diagonal":d,"total":out[r][c]},"note":f"Tile ({r}, {c}): {diff[r][c]} + {a} above + {l} left - {d} diagonal = {out[r][c]}."})
assert out==[[0,0,0,0],[0,5,5,0],[0,5,5,0],[0,0,0,0]] and st[7]["vars"]["delta"]==-5 and st[7]["vars"]["total"]==0
fill(CH,F,block(flat,["w"],st),"@@TRACE2@@")
