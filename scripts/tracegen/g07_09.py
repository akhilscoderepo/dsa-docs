from common import *
CH='07-prefix-sums-and-difference-arrays'
F='09-two-dimensional-prefix.md'
m=[[1,2,3],[4,5,6]]; R,C=2,3
P=[[0]*(C+1) for _ in range(R+1)]; st=[]
for r in range(R):
    for c in range(C):
        up=P[r][c+1]; left=P[r+1][c]; diag=P[r][c]
        P[r+1][c+1]=m[r][c]+up+left-diag
        st.append({"at":{"w":(r+1)*(C+1)+c+1},"vars":{"cell":m[r][c],"above":up,"left":left,"diagonal":diag,"entry":P[r+1][c+1]},"note":f"The cell is {m[r][c]}. Entry = {m[r][c]} + {up} above + {left} left - {diag} diagonal = {P[r+1][c+1]}."})
assert P==[[0,0,0,0],[0,1,3,6],[0,5,12,21]] and st[4]["vars"]["cell"]==5 and st[4]["vars"]["entry"]==12
flat=[str(x) for row in P for x in row]
fill(CH,F,block(flat,["w"],st),"@@TRACE1@@")
r1,c1,r2,c2=1,1,1,2
W=C+1
corners=[("bottom-right",r2+1,c2+1,"+"),("top",r1,c2+1,"-"),("left",r2+1,c1,"-"),("overlap",r1,c1,"+")]
st=[]; total=0
for name,r,c,sg in corners:
    v=P[r][c]; total+= v if sg=="+" else -v
    st.append({"at":{"read":r*W+c},"vars":{"corner":name,"value":v,"runningTotal":total},"note":f"Read the {name} entry, which holds {v}, and {'add' if sg=='+' else 'subtract'} it. The running total is {total}."})
assert total==11==5+6 and st[3]["vars"]["value"]==1
fill(CH,F,block(flat,["read"],st),"@@TRACE2@@")
