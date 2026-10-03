from ll import *
CH='14-linked-lists'
F='03-partial-and-k-group-reversal.md'
vals=[9,4,7,2,8,5,3];k=3
nxt=[1,2,3,4,5,6,None]
head=0;before=None;gs=0
steps=[]
while True:
    probe=gs;c=0
    while probe is not None and c<k: probe=nxt[probe];c+=1
    if c<k:
        steps.append({"at":{"before":before if before is not None else -1,"group":gs},"vars":{"list":chain(vals,nxt,head),"found":c},"note":f"The look-ahead from the node holding {vals[gs]} finds only {c} node(s), fewer than {k}, so the short suffix is left exactly as it is and the loop stops."})
        break
    prev=probe;curr=gs
    for _ in range(k):
        s=nxt[curr];nxt[curr]=prev;prev=curr;curr=s
    if before is None: head=prev
    else: nxt[before]=prev
    steps.append({"at":{"before":before if before is not None else -1,"group":gs},"vars":{"list":chain(vals,nxt,head),"found":k},"note":f"The look-ahead finds {k} nodes after the group starting at the node holding {vals[gs]}, so the group is reversed with its tail pointed at the following node. The list now reads {chain(vals,nxt,head).replace('>',', ')}."})
    before=gs;gs=probe
assert chain(vals,nxt,head)=="7>4>9>5>8>2>3"
fill(CH,F,block(vals,["before","group"],steps),"@@TRACE1@@")
v2=[4,7,1,9]
n2=[1,2,3,None]
b=0;f=1;s=2;a=3
st=[{"at":{"before":0,"first":1,"second":2,"after":3},"vars":{"list":chain(v2,n2,0)},"note":"The pair to swap is the nodes holding 7 and 1. The node holding 4 stands before it and the node holding 9 comes after it."}]
n2[f]=a
st.append({"at":{"before":0,"first":1,"second":2,"after":3},"vars":{"list":chain(v2,n2,0),"second_chain":chain(v2,n2,2)},"note":"The first node of the pair is pointed at the node after the pair, so it no longer depends on the second node for the tail."})
n2[s]=f
st.append({"at":{"before":0,"first":1,"second":2,"after":3},"vars":{"second_chain":chain(v2,n2,2)},"note":"The second node is pointed at the first, so from the second node the order reads 1, 7, 9. The list from the head is still 4, 7, 9 because the node before has not been rewired."})
n2[b]=s
st.append({"at":{"before":0,"first":1,"second":2,"after":3},"vars":{"list":chain(v2,n2,0)},"note":"The node before the pair is pointed at the second node. The list now reads 4, 1, 7, 9 and all four nodes are reachable."})
assert chain(v2,n2,0)=="4>1>7>9"
fill(CH,F,block(v2,["before","first","second","after"],st),"@@TRACE2@@")
