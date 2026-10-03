from common import *
CH='14-linked-lists'
F='07-intersection.md'
def sim(cells,nextA,nextB,hA,hB):
    pa,pb=hA,hB;steps=[];k=0
    steps.append((k,pa,pb))
    while pa!=pb:
        pa = hB if pa==-1 else nextA[pa]
        pb = hA if pb==-1 else nextB[pb]
        k+=1
        steps.append((k,pa,pb))
    return steps
# trace 1: A: 0->1->5->6 ; B: 2->3->4->5->6
cells=[4,1,6,1,9,8,2]
nxt={0:1,1:5,5:6,6:-1,2:3,3:4,4:5}
nA=lambda i:nxt[i]
s=sim(cells,nxt,nxt,0,2)
st=[]
for k,pa,pb in s:
    va=cells[pa] if pa!=-1 else None;vb=cells[pb] if pb!=-1 else None
    if k==0: note="Pointer pa starts at the head of the first list, holding 4, and pb at the head of the second list, holding 6. They are different nodes."
    else:
        note=f"Round {k}: pa is "+("past the end" if pa==-1 else f"on the node holding {va}")+" and pb is "+("past the end" if pb==-1 else f"on the node holding {vb}")+"."
        if pa==-1: note+=" pa has just left the first list and will restart at the head of the second."
        if pb==-1: note+=" pb has just left the second list and will restart at the head of the first."
        if pa==pb: note+=" They are the same node, so this is the first shared node."
    st.append({"at":{"pa":pa,"pb":pb},"vars":{"rounds":k},"note":note})
assert s[-1][1]==5 and s[-1][0]==8
fill(CH,F,block(cells,["pa","pb"],st),"@@TRACE1@@")
cells2=[1,2,3]
nxt2={0:1,1:-1,2:-1}
s=sim(cells2,nxt2,nxt2,0,2)
st=[]
for k,pa,pb in s:
    if k==0: note="Pointer pa starts on the node holding 1 and pb on the node holding 3."
    else:
        note=f"Round {k}: pa is "+("past the end" if pa==-1 else f"on the node holding {cells2[pa]}")+" and pb is "+("past the end" if pb==-1 else f"on the node holding {cells2[pb]}")+"."
        if pa==pb==-1: note+=" Both are past the end together, so the lists share no node."
    st.append({"at":{"pa":pa,"pb":pb},"vars":{"rounds":k},"note":note})
assert s[-1][0]==4 and s[-1][1]==-1
fill(CH,F,block(cells2,["pa","pb"],st),"@@TRACE2@@")
