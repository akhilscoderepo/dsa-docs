from common import *
CH='14-linked-lists'; F='01-node-invariants.md'
# Trace 1: count nodes of 4,7,9
vals=[4,7,9]; steps=[]
n=0
steps.append({"at":{"curr":0},"vars":{"n":0},"note":"curr starts at the head, the node 4. The count is 0."})
for i,v in enumerate(vals):
    n+=1
    nxt=i+1
    note=f"The walk counts the node {v}, so n becomes {n}. Then curr moves to " + (f"the node {vals[nxt]}." if nxt<len(vals) else "null, which ends the loop.")
    steps.append({"at":{"curr":nxt},"vars":{"n":n},"note":note})
assert n==3
fill(CH,F,block(vals,["curr"],steps),"@@TRACE1@@")
# Trace 2: insert 5 after node 7. storage order: 4,7,9,5 ; links as dict
cells=[4,7,9,5]
nxt={0:1,1:2,2:None,3:None}
def chain(h=0):
    out=[];i=h
    while i is not None and len(out)<10: out.append(str(cells[i])); i=nxt[i]
    return ",".join(out)
st=[]
def snap(node,new,saved,note,extra=None):
    v={"chain":chain(),"saved":"-" if saved is None else cells[saved]}
    st.append({"at":{"node":node,"new":new},"vars":v,"note":note})
snap(1,-1,None,"Start: the list reads 4,7,9. The pointer node marks the node 7, and no new node exists yet.")
saved=nxt[1]
snap(1,-1,saved,"saved copies node.next, which is the node 9. The node 9 now has two references, node.next and saved.")
assert chain()=="4,7,9"
nxt[3]=saved
snap(1,3,saved,"The new node 5 is built with its next field set to saved. The list still reads 4,7,9 from the head, and the node 5 is not linked yet.")
nxt[1]=3
snap(1,3,saved,"node.next now points to the new node. The list reads 4,7,5,9, and every old node is still reachable.")
assert chain()=="4,7,5,9"
fill(CH,F,block(cells,["node","new"],st),"@@TRACE2@@")
