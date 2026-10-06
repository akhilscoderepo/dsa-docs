from common import *
CH='14-linked-lists'; F='05-dummy-heads.md'
# Trace 1: remove all 7s from 7,7,3,7,4 with dummy (cell 0 = dummy)
cells=[0,7,7,3,7,4]; nxt={0:1,1:2,2:3,3:4,4:5,5:-1}
def seq():
    out=[];i=nxt[0]
    while i!=-1: out.append(cells[i]); i=nxt[i]
    return ",".join(map(str,out)) or "empty"
prev=0; st=[]
def at(): return {"prev":prev,"curr":nxt[prev]}
st.append({"at":at(),"vars":{"result":seq()},"note":"Start: prev is the dummy node, and curr is the first real node, 7."})
while nxt[prev]!=-1:
    c=nxt[prev]
    if cells[c]==7:
        nxt[prev]=nxt[c]
        st.append({"at":at(),"vars":{"result":seq()},"note":f"The node {cells[c]} matches, so prev.next skips it. prev stays where it is."})
    else:
        prev=c
        st.append({"at":at(),"vars":{"result":seq()},"note":f"The node {cells[c]} does not match, so prev moves onto it."})
assert seq()=="3,4"
fill(CH,F,block(cells,["prev","curr"],st),"@@TRACE1@@")
# Trace 2: merge 2,5 and 1,6 behind a dummy tail
cells=[0,2,5,1,6]; A=[1,2]; B=[3,4]
a=1;b=3;tail=0; out=[]; st=[]
nx={1:2,2:-1,3:4,4:-1}
def snap(note): st.append({"at":{"a":a,"b":b,"tail":tail},"vars":{"result":",".join(map(str,out)) or "empty"},"note":note})
snap("Start: tail is the dummy node, and the result is empty.")
while a!=-1 and b!=-1:
    if cells[b]<cells[a]: src=b; b=nx[b]
    else: src=a; a=nx[a]
    out.append(cells[src]); tail=src
    snap(f"The smaller head is the node {cells[src]}. tail.next attaches it with the same write the first node needed.")
rest=[]
while a!=-1: rest.append(cells[a]); a=nx[a]
while b!=-1: rest.append(cells[b]); b=nx[b]
out+=rest
snap(f"One list is empty. One write attaches the leftover {','.join(map(str,rest))}, and the method returns dummy.next.")
assert out==[1,2,5,6]
fill(CH,F,block(cells,["a","b","tail"],st),"@@TRACE2@@")
