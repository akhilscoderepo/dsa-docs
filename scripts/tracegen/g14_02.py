from ll import *
CH='14-linked-lists'
F='02-reverse.md'
vals=[3,8,2,6]
nxt=[1,2,3,None]
prev=None;cur=0
steps=[{"at":{"prev":-1,"curr":0},"vars":{"reversed":"empty","untouched":chain(vals,nxt,0)},"note":"The reversed prefix is empty and prev is null. The untouched suffix is the whole list, headed by the node holding 3."}]
while cur is not None:
    saved=nxt[cur]
    nxt[cur]=prev
    sv=vals[saved] if saved is not None else None
    prev=cur;cur=saved
    steps.append({"at":{"prev":prev,"curr":cur if cur is not None else 4},"vars":{"reversed":chain(vals,nxt,prev),"untouched":chain(vals,nxt,cur) if cur is not None else "empty"},"note":f"The old successor ({sv if sv is not None else 'null'}) was saved, the node holding {vals[prev]} was pointed at the previous node, and both references moved forward. The reversed prefix now reads {chain(vals,nxt,prev).replace('>',', ')}."})
assert chain(vals,nxt,prev)=="6>2>8>3"
fill(CH,F,block(vals,["prev","curr"],steps),"@@TRACE1@@")
v2=[3,8,2,6,9,1]
n2=[1,2,3,4,5,None]
before=0
prev=None;cur=1
st=[{"at":{"before":0,"prev":-1,"curr":1},"vars":{"whole":chain(v2,n2,0),"segment_tail":"8"},"note":"The node holding 3 sits just before the segment, and the segment starts at the node holding 8. The first node of the segment will become its tail, so it is remembered."}]
tail=1
for k in range(3):
    saved=n2[cur]
    n2[cur]=prev
    prev=cur;cur=saved
    st.append({"at":{"before":0,"prev":prev,"curr":cur},"vars":{"reversed_part":chain(v2,n2,prev),"rest":chain(v2,n2,cur)},"note":f"One more segment node is redirected backward. The reversed part reads {chain(v2,n2,prev).replace('>',', ')} and the rest starts at the node holding {v2[cur]}."})
n2[before]=prev
n2[tail]=cur
st.append({"at":{"before":0,"prev":prev,"curr":cur},"vars":{"whole":chain(v2,n2,0)},"note":"The node before the segment is pointed at the new segment head, and the old segment head, now its tail, is pointed at the node after the segment. The list reads "+chain(v2,n2,0).replace('>',', ')+"."})
assert chain(v2,n2,0)=="3>6>2>8>9>1"
fill(CH,F,block(v2,["before","prev","curr"],st),"@@TRACE2@@")
