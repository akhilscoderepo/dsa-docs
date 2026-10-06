from common import *
CH='14-linked-lists'; F='06-cycle-entry.md'
def mk(vals,pos):
    n=len(vals); nxt={i:(i+1 if i+1<n else (pos if pos>=0 else -1)) for i in range(n)}
    return nxt
# Trace 1: 3,2,0,-4 with last -> index 1
vals=[3,2,0,-4]; nxt=mk(vals,1)
s=f=0; moved=0; st=[{"at":{"slow":0,"fast":0},"vars":{"moved":0},"note":"Start: both pointers hold the node 3."}]
while True:
    s=nxt[s]; f=nxt[nxt[f]]; moved+=1
    if s==f:
        st.append({"at":{"slow":s,"fast":f},"vars":{"moved":moved},"note":f"slow moves 1 and fast moves 2. Both hold the node {vals[s]}, so the references are equal and a cycle exists."}); break
    st.append({"at":{"slow":s,"fast":f},"vars":{"moved":moved},"note":f"slow moves 1 and fast moves 2. slow holds the node {vals[s]} and fast holds the node {vals[f]}."})
    assert moved<20
meet1=s
fill(CH,F,block(vals,["slow","fast"],st),"@@TRACE1@@")
# Trace 2: 1..6, 6->3 (index 2)
vals=[1,2,3,4,5,6]; nxt=mk(vals,2)
s=f=0
while True:
    s=nxt[s]; f=nxt[nxt[f]]
    if s==f: break
meet=s; walker=0
st=[{"at":{"meet":meet,"walker":0},"vars":{"steps":0},"note":f"Start: meet holds the node {vals[meet]}, found by the first phase, and walker holds the head, the node 1."}]
k=0
while walker!=meet:
    walker=nxt[walker]; meet=nxt[meet]; k+=1
    eq=" Both hold the same node, so this node is the cycle entry." if walker==meet else ""
    st.append({"at":{"meet":meet,"walker":walker},"vars":{"steps":k},"note":f"Both move one node. walker holds the node {vals[walker]} and meet holds the node {vals[meet]}."+eq})
assert vals[walker]==3 and k==2
fill(CH,F,block(vals,["meet","walker"],st),"@@TRACE2@@")
