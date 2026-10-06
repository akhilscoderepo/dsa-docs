from common import *
CH='14-linked-lists'; F='10-multilevel-flattening.md'
def mk(cells,nxt,prv):
    def fwd(h):
        out=[];i=h
        while i!=-1 and len(out)<20: out.append(str(cells[i])); i=nxt[i]
        return ",".join(out)
    def bwd(t):
        out=[];i=t
        while i!=-1 and len(out)<20: out.append(str(cells[i])); i=prv[i]
        return ",".join(out)
    return fwd,bwd
# Trace 1: cells 1,2,3 | 7,8 ; indexes 0,1,2,3,4
cells=[1,2,3,7,8]
nxt={0:1,1:2,2:-1,3:4,4:-1}; prv={0:-1,1:0,2:1,3:-1,4:3}
fwd,bwd=mk(cells,nxt,prv)
parent=1; tail=-1; succ=-1; st=[]
def snap(note,show=True):
    st.append({"at":{"parent":parent,"tail":tail,"succ":succ},"vars":{"forward":fwd(0),"backward":bwd(2)},"note":note})
snap("Start: the main list reads 1,2,3. The node 2 has the child chain 7,8, whose links are kept apart from the main list.")
succ=nxt[parent]
snap("succ copies parent.next, which is the node 3. This happens before any write.")
tail=3
while nxt[tail]!=-1: tail=nxt[tail]
snap("The walk along the child chain stops on the node 8, the child tail.")
child=3
nxt[parent]=child; prv[child]=parent
snap("parent.next now points at the node 7, and the node 7 points back at the node 2. The main list is cut after the node 8: forward reads 1,2,7,8 and the node 3 is held only by succ.")
nxt[tail]=succ; prv[succ]=tail
snap("tail.next points at the node 3, and the node 3 points back at the node 8. Both directions now agree.")
assert fwd(0)=="1,2,7,8,3" and bwd(2)=="3,8,7,2,1"
fill(CH,F,block(cells,["parent","tail","succ"],st),"@@TRACE1@@")
# Trace 2: main 1,2,3 ; child of 2: 7,8,9 ; child of 8: 11,12. idx: 0,1,2 | 3,4,5 | 6,7
cells=[1,2,3,7,8,9,11,12]
nxt={0:1,1:2,2:-1,3:4,4:5,5:-1,6:7,7:-1}; prv={0:-1,1:0,2:1,3:-1,4:3,5:4,6:-1,7:6}
fwd,bwd=mk(cells,nxt,prv)
st=[]
def snap2(curr,note,last):
    st.append({"at":{"curr":curr,"tail":-1 if False else last},"vars":{"forward":fwd(0)},"note":note})
def splice(p):
    child=cells.index(0) if False else None
    return None
children={1:3,4:6}
curr=0
st.append({"at":{"curr":0,"tail":-1},"vars":{"forward":fwd(0)},"note":"Start: the main list reads 1,2,3. The nodes 2 and 8 each have a child chain."})
order=[]
while curr!=-1:
    if curr in children:
        child=children.pop(curr); succ=nxt[curr]
        tail=child
        while nxt[tail]!=-1: tail=nxt[tail]
        nxt[curr]=child; prv[child]=curr
        nxt[tail]=succ
        if succ!=-1: prv[succ]=tail
        st.append({"at":{"curr":curr,"tail":tail},"vars":{"forward":fwd(0)},"note":f"The node {cells[curr]} has a child chain, so it is spliced in front of the node {cells[succ] if succ!=-1 else 'null'}. The child tail is the node {cells[tail]}."})
    curr=nxt[curr]
assert fwd(0)=="1,2,7,8,11,12,9,3", fwd(0)
st.append({"at":{"curr":-1,"tail":7},"vars":{"forward":fwd(0)},"note":"The walk ends at null. Every child chain is spliced, and the list reads 1,2,7,8,11,12,9,3."})
fill(CH,F,block(cells,["curr","tail"],st),"@@TRACE2@@")
