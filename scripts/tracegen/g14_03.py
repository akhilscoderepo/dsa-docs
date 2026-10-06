from common import *
CH='14-linked-lists'; F='03-partial-and-k-group-reversal.md'
vals=[1,2,3,4,5]
# Trace 1: reverse nodes 2,3,4 (indexes 1..3), pred=0
nxt={0:1,1:2,2:3,3:4,4:None}
def seq(h=0):
    out=[];i=h
    while i is not None and len(out)<10: out.append(str(vals[i])); i=nxt[i]
    return ",".join(out)
pred=0; first=1; prev=None; curr=1; st=[]
def at(): return {"pred":pred,"prev":-1 if prev is None else prev,"curr":len(vals) if curr is None else curr}
st.append({"at":at(),"vars":{"chain":seq()},"note":"Start: pred is the node 1, and the group is the nodes 2, 3 and 4. The look-ahead found three nodes, so the reversal may begin."})
for _ in range(3):
    saved=nxt[curr]; v=vals[curr]
    nxt[curr]=prev; prev=curr; curr=saved
    st.append({"at":at(),"vars":{"chain":seq()},"note":f"The node {v} moves across: saved keeps the rest, the node is redirected at the reversed part, and prev takes the node {v}."})
# The chain var during moves is shown from head; after reconnect it is whole
nxt[first]=curr
st.append({"at":at(),"vars":{"chain":seq()},"note":"first.next = curr links the old group head, the node 2, to the node 5."})
nxt[pred]=prev
st.append({"at":at(),"vars":{"chain":seq()},"note":"pred.next = prev links the node 1 to the node 4. The list reads 1,4,3,2,5."})
assert seq()=="1,4,3,2,5"
fill(CH,F,block(vals,["pred","prev","curr"],st),"@@TRACE1@@")
# Trace 2: k=2 groups
order=[1,2,3,4,5]; k=2; st=[]
def ch(o): return ",".join(map(str,o))
pred=-1; first=0
st.append({"at":{"pred":-1,"first":0},"vars":{"chain":ch(order)},"note":"Start: no group is reversed yet, and the first group begins at the node 1. The look-ahead reads two nodes, so the group is complete."})
cur=list(order)
for g in range(2):
    s=g*2
    cur[s:s+2]=cur[s:s+2][::-1]
    p=vals.index(order[s]); nf=s+2
    st.append({"at":{"pred":p,"first":nf},"vars":{"chain":ch(cur)},"note":f"The group {order[s]},{order[s+1]} is reversed and its tail is the node {order[s]}. The next group starts at the node {order[nf]}."+(" The look-ahead from there finds two nodes." if g==0 else " The look-ahead from there reads the node 5 and then reaches the end.")})
st.append({"at":{"pred":2,"first":4},"vars":{"chain":ch(cur)},"note":"The look-ahead counted one node, which is fewer than k, so the method stops with no write. The node 5 stays in place."})
assert ch(cur)=="2,1,4,3,5"
fill(CH,F,block(vals,["pred","first"],st),"@@TRACE2@@")
