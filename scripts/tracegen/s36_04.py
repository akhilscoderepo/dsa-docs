from common import *
from collections import deque
CH='36-stateful-containers-and-histories'; F='04-split-containers.md'
def seq(L,R): return ",".join(map(str,list(L)+list(R)))
def ok(L,R): return len(L)==(len(L)+len(R))//2
# Trace 1: build with rebalance moves; cells hold the final sequence.
L=deque(); R=deque(); st=[]
st.append({"at":{"b":0},"vars":{"seq":"","left":0,"right":0},"note":"Both halves are empty, so the boundary b is 0."})
def snap(note): st.append({"at":{"b":len(L)},"vars":{"seq":seq(L,R),"left":len(L),"right":len(R)},"note":note})
def fix():
    if len(L)>len(R):
        x=L.pop(); R.appendleft(x); snap(f"The left half is longer, so {x} moves from the end of the left half to the front of the right half.")
    elif len(R)>len(L)+1:
        x=R.popleft(); L.append(x); snap(f"The right half is two elements longer, so {x} moves from the front of the right half to the end of the left half.")
    assert ok(L,R)
for name,v in [("pushBack",10),("pushBack",20),("pushFront",5),("pushMiddle",15),("pushMiddle",25)]:
    if name=="pushBack": R.append(v)
    elif name=="pushFront": L.appendleft(v)
    else: L.append(v)
    snap(f"{name}({v}) inserts {v}; the sequence is now {seq(L,R)}.")
    fix()
final=list(L)+list(R); assert final==[5,15,25,10,20]
fill(CH,F,block([str(x) for x in final],["b"],st),"@@TRACE1@@")
# Trace 2: removals from 1..6.
L=deque([1,2,3]); R=deque([4,5,6]); st=[]; got=[]
orac=[1,2,3,4,5,6]; want=[]
st.append({"at":{"b":3},"vars":{"seq":seq(L,R),"left":3,"right":3},"note":"Start: left half 1,2,3 and right half 4,5,6, so the boundary b is 3."})
def fix2():
    if len(L)>len(R): R.appendleft(L.pop()); return True
    if len(R)>len(L)+1: L.append(R.popleft()); return True
    return False
for name in ["popFront","popFront","popMiddle","popBack","popMiddle","popMiddle"]:
    n=len(L)+len(R)
    if name=="popFront": v=L.popleft() if L else R.popleft(); want.append(orac.pop(0))
    elif name=="popBack": v=R.pop(); want.append(orac.pop())
    else: v=L.pop() if len(L)==len(R) else R.popleft(); want.append(orac.pop((n-1)//2))
    assert v==want[-1]; got.append(v)
    s1=seq(L,R); moved=fix2(); assert ok(L,R) and seq(L,R)==",".join(map(str,orac))
    extra=" The sizes now differ by two, so one element crosses the boundary." if moved else " The sizes already satisfy the rule."
    st.append({"at":{"b":len(L)},"vars":{"seq":seq(L,R),"left":len(L),"right":len(R)},"note":f"{name} returns {v}.{extra}"})
assert got==[1,2,4,6,3,5]
fill(CH,F,block(["1","2","3","4","5","6"],["b"],st),"@@TRACE2@@")
