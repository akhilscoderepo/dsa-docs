from common import *
CH='14-linked-lists'; F='07-intersection.md'
def walk(cells,nxtA,nxtB,hA,hB,ph,note_shared):
    pa=hA; pb=hB; st=[]
    def at(): return {"pa":pa,"pb":pb}
    def desc(p): return "null" if p==-1 else f"the node {cells[p]}"
    st.append({"at":at(),"vars":{"steps":0},"note":"Start: pa holds the head of the first list and pb holds the head of the second list."})
    k=0
    while pa!=pb:
        npa = hB if pa==-1 else nxtA[pa]
        npb = hA if pb==-1 else nxtB[pb]
        sa = " from null to the head of the second list" if pa==-1 else ""
        sb = " from null to the head of the first list" if pb==-1 else ""
        pa,pb=npa,npb; k+=1
        st.append({"at":at(),"vars":{"steps":k},"note":f"Both move one node. pa holds {desc(pa)}{sa}, and pb holds {desc(pb)}{sb}."})
        assert k<40
    st[-1]["note"]+= " The references are equal, "+note_shared
    return st,pa,k
# Trace 1: A=4,1,8,4,5 ; B=5,6,1,8,4,5 sharing 8,4,5. cells idx: 0:4 1:1 2:8 3:4 4:5 | 5:5 6:6 7:1
cells=[4,1,8,4,5,5,6,1]
nxtA={0:1,1:2,2:3,3:4,4:-1}
nxtB={5:6,6:7,7:2,2:3,3:4,4:-1}
nxt={**nxtA,**nxtB}
st,p,k=walk(cells,nxt,nxt,0,5,1,"so the walkers stand on the first shared node.")
assert p==2 and k==9
fill(CH,F,block(cells,["pa","pb"],st),"@@TRACE1@@")
# Trace 2: A=2,6,4 ; B=1,5 no share. cells: 0:2 1:6 2:4 3:1 4:5
cells=[2,6,4,1,5]; nxt={0:1,1:2,2:-1,3:4,4:-1}
st,p,k=walk(cells,nxt,nxt,0,3,2,"and both are null, so no node is shared.")
assert p==-1 and k==6, k
fill(CH,F,block(cells,["pa","pb"],st),"@@TRACE2@@")
