from common import *
CH='10-intervals'
F='04-two-list-intersection.md'
A=[[0,2],[5,10],[13,23],[24,25]]; B=[[1,5],[8,12],[15,24],[25,26]]
cells=[f"{a}-{b}" for a,b in A+B]
i=j=0; out=[]; st=[]; touch=[]
while i<len(A) and j<len(B):
    lo=max(A[i][0],B[j][0]); hi=min(A[i][1],B[j][1])
    if lo<=hi:
        out.append([lo,hi]); note=f"The pair {A[i][0]} to {A[i][1]} and {B[j][0]} to {B[j][1]} shares the stretch {lo} to {hi}, "
        if lo==hi: touch.append((i,j,lo,len(out)))
    else:
        note=f"The pair {A[i][0]} to {A[i][1]} and {B[j][0]} to {B[j][1]} shares nothing, "
    adv='first' if A[i][1]<B[j][1] else 'second'
    note+=f"and the {adv} range leaves because its end is smaller."
    st.append({"at":{"i":i,"j":4+j},"vars":{"lo":lo,"hi":hi,"found":len(out)},"note":note})
    if A[i][1]<B[j][1]: i+=1
    else: j+=1
assert out==[[1,2],[5,5],[8,10],[15,23],[24,24],[25,25]]
assert "shares the stretch 1 to 2" in st[0]["note"]
fill(CH,F,block(cells,["i","j"],st),"@@TRACE1@@")
# trace 2: only touching moments
st2=[]
for (ii,jj,v,n) in touch:
    st2.append({"at":{"i":ii,"j":4+jj},"vars":{"lo":v,"hi":v,"found":n},"note":f"The pair {A[ii][0]} to {A[ii][1]} and {B[jj][0]} to {B[jj][1]} meets at the single value {v}, and the closed test accepts it because the larger start does not pass the smaller end."})
assert [t[2] for t in touch]==[5,24,25] and "5 to 10 and 1 to 5" in st2[0]["note"]
fill(CH,F,block(cells,["i","j"],st2),"@@TRACE2@@")
