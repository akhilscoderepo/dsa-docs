from common import *
CH='14-linked-lists'
F='06-cycle-entry.md'
vals=[7,3,5,2,6,8];n=6;pos=1
nx=lambda i: i+1 if i<n-1 else pos
slow=fast=0
steps=[{"at":{"slow":0,"fast":0,"probe":-1},"vars":{"phase":"chase"},"note":"Both pointers start at the first signpost, which holds 7."}]
t=0
while True:
    slow=nx(slow);fast=nx(nx(fast));t+=1
    meet=slow==fast
    steps.append({"at":{"slow":slow,"fast":fast,"probe":-1},"vars":{"phase":"chase","round":t},"note":f"After round {t} slow stands at the signpost holding {vals[slow]} and fast at the one holding {vals[fast]}."+(" They are the same signpost, so a loop exists." if meet else "")})
    if meet: break
probe=0
steps.append({"at":{"slow":slow,"fast":fast,"probe":0},"vars":{"phase":"find the entry"},"note":"A third pointer is placed at the first signpost, while slow stays at the meeting point. From now on both move one signpost at a time."})
while probe!=slow:
    probe=nx(probe);slow=nx(slow)
    steps.append({"at":{"slow":slow,"fast":fast,"probe":probe},"vars":{"phase":"find the entry"},"note":f"Both advance one signpost. The probe is at the signpost holding {vals[probe]} and slow at the one holding {vals[slow]}."+(" They coincide, and this signpost is where the loop begins." if probe==slow else "")})
assert probe==1
fill(CH,F,block(vals,["slow","fast","probe"],steps),"@@TRACE1@@")
v2=[4,9];n=2;pos=0
nx=lambda i: i+1 if i<n-1 else pos
slow=fast=0;st=[{"at":{"slow":0,"fast":0},"vars":{"rounds":0},"note":"Both pointers start at the first node, and the second node points back to the first."}]
r=0
while True:
    slow=nx(slow);fast=nx(nx(fast));r+=1
    st.append({"at":{"slow":slow,"fast":fast},"vars":{"rounds":r},"note":f"Round {r}: slow is on the node holding {v2[slow]} and fast is on the node holding {v2[fast]}."+(" They are the same node, so there is a cycle." if slow==fast else " They differ, so the chase continues.")})
    if slow==fast: break
assert r==2
fill(CH,F,block(v2,["slow","fast"],st),"@@TRACE2@@")
