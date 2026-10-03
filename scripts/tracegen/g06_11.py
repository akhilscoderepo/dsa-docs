from common import *
CH='06-binary-search'
F='11-matrix-search.md'
m=[[1,3,5,7],[10,11,16,20],[23,30,34,60]]; cols=4; target=16
flat=[v for r in m for v in r]
lo,hi=0,11; st=[]
while lo<=hi:
    mid=(lo+hi)//2; r,c=divmod(mid,cols); v=m[r][c]
    if v==target:
        st.append({"at":{"lo":lo,"hi":hi,"mid":mid},"vars":{"row":r,"col":c,"value":v},"note":f"Position {mid} is row {r}, column {c}, and its label is {v}, which is the part, so the answer is yes."}); break
    if v<target:
        st.append({"at":{"lo":lo,"hi":hi,"mid":mid},"vars":{"row":r,"col":c,"value":v},"note":f"Position {mid} is row {r}, column {c}, and its label is {v}, smaller than {target}, so lo moves to {mid+1}."}); lo=mid+1
    else:
        st.append({"at":{"lo":lo,"hi":hi,"mid":mid},"vars":{"row":r,"col":c,"value":v},"note":f"Position {mid} is row {r}, column {c}, and its label is {v}, larger than {target}, so hi moves to {mid-1}."}); hi=mid-1
assert len(st)==3 and "23" in st[1]["note"] and "larger" in st[1]["note"]
fill(CH,F,block([str(x) for x in flat],["lo","hi","mid"],st),"@@TRACE1@@")
g=[[1,4,7],[2,5,8],[3,6,9]]; target=6
flat=[v for r in g for v in r]
r,c=0,2; st=[]
while r<3 and c>=0:
    v=g[r][c]; pos=r*3+c
    if v==target:
        st.append({"at":{"read":pos},"vars":{"row":r,"col":c,"value":v},"note":f"The cell at row {r}, column {c} holds {v}, which is the part, so the answer is yes."}); break
    if v>target:
        st.append({"at":{"read":pos},"vars":{"row":r,"col":c,"value":v},"note":f"The cell at row {r}, column {c} holds {v}, larger than {target}, so its column below is discarded and the walk moves left."}); c-=1
    else:
        st.append({"at":{"read":pos},"vars":{"row":r,"col":c,"value":v},"note":f"The cell at row {r}, column {c} holds {v}, smaller than {target}, so the rest of its shelf to the left is discarded and the walk moves down."}); r+=1
assert len(st)==4 and "4, smaller" in st[1]["note"] and "moves down" in st[1]["note"]
fill(CH,F,block([str(x) for x in flat],["read"],st),"@@TRACE2@@")
