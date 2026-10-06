from common import *
CH='14-linked-lists'; F='09-fixed-gap-kth-from-end.md'
# Trace 1: 1..5, k=2 (no dummy)
vals=[1,2,3,4,5]; n=5; k=2
lead=0; trail=0
def pos(p): return -1 if p>=n else p
st=[{"at":{"lead":0,"trail":0},"vars":{"gap":0},"note":"Start: lead and trail both hold the node 1, so the gap is 0."}]
for i in range(k):
    lead+=1
    st.append({"at":{"lead":pos(lead),"trail":trail},"vars":{"gap":lead-trail},"note":f"Only lead moves, to the node {vals[lead]}. The gap is {lead-trail}."})
while lead<n:
    lead+=1; trail+=1
    ld="null" if lead>=n else f"the node {vals[lead]}"
    st.append({"at":{"lead":pos(lead),"trail":trail},"vars":{"gap":lead-trail},"note":f"Both move one node. lead holds {ld}, and trail holds the node {vals[trail]}. The gap is still {lead-trail}."})
assert vals[trail]==4
fill(CH,F,block(vals,["lead","trail"],st),"@@TRACE1@@")
# Trace 2: dummy,1,2,3 ; k=3; cells idx0 dummy
cells=[0,1,2,3]; n=4
lead=1; trail=0
def pos2(p): return -1 if p>=n else p
st=[{"at":{"lead":1,"trail":0},"vars":{"gap":1},"note":"Start: trail holds the dummy node and lead holds the head, the node 1."}]
for i in range(3):
    lead+=1
    ld="null" if lead>=n else f"the node {cells[lead]}"
    st.append({"at":{"lead":pos2(lead),"trail":trail},"vars":{"gap":lead-trail},"note":f"Only lead moves, to {ld}."})
assert lead>=n
st.append({"at":{"lead":-1,"trail":0},"vars":{"gap":lead-trail},"note":"lead is null, so the second loop makes no move. trail still holds the dummy node, the predecessor of the head."})
fill(CH,F,block(cells,["lead","trail"],st),"@@TRACE2@@")
