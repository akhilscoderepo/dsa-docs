from common import *
CH='06-binary-search'
M=[[2,4,6,8],[11,13,15,17],[20,22,24,26]]
flat=[v for r in M for v in r]; cols=4
lo,hi=0,11; t=15
st=[{"at":{"lo":0,"hi":11,"mid":-1},"vars":{"target":"15"},"note":"Start with the virtual indexes 0 to 11."}]
while lo<=hi:
    mid=lo+(hi-lo)//2; v=M[mid//cols][mid%cols]; assert v==flat[mid]
    r,c=mid//cols,mid%cols
    if v==t:
        st.append({"at":{"lo":lo,"hi":hi,"mid":mid},"vars":{"row":str(r),"col":str(c),"value":str(v)},"note":f"Index {mid} is row {r}, column {c}, and holds {v}, which equals the target, so the search returns true."}); break
    if v<t: lo=mid+1; n=f"Index {mid} is row {r}, column {c}, and holds {v}, which is below 15, so lo becomes {lo}."
    else: hi=mid-1; n=f"Index {mid} is row {r}, column {c}, and holds {v}, which is above 15, so hi becomes {hi}."
    st.append({"at":{"lo":lo,"hi":hi,"mid":mid},"vars":{"row":str(r),"col":str(c),"value":str(v)},"note":n})
fill(CH,'92-sorted-matrix.md',block(flat,["lo","hi","mid"],st),"@@TRACE1@@")
G=[[1,4,7,11],[2,5,8,12],[3,6,9,16],[10,13,14,17]]; flat=[v for r in G for v in r]; t=13
row,col=0,3; st=[{"at":{"cell":3},"vars":{"target":"13","row":"0","col":"3"},"note":"Start at the top-right cell, row 0 and column 3."}]
found=False
while row<4 and col>=0:
    v=G[row][col]
    if v==t:
        st.append({"at":{"cell":row*4+col},"vars":{"row":str(row),"col":str(col),"value":str(v)},"note":f"The value {v} equals the target, so the walk returns true."}); found=True; break
    if v>t: col-=1; n=f"The value {v} is above 13, so the column below it is too large and the walk moves left."
    else: row+=1; n=f"The value {v} is below 13, so the rest of its row to the left is too small and the walk moves down."
    st.append({"at":{"cell":row*4+col if (row<4 and col>=0) else -1},"vars":{"row":str(row),"col":str(col),"value":str(v)},"note":n})
assert found
fill(CH,'92-sorted-matrix.md',block(flat,["cell"],st),"@@TRACE2@@")
